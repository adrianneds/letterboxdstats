from bs4 import BeautifulSoup
import requests
import html5lib
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime
from selenium import webdriver
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import numpy as np

# create soup
def init_soup(url):
    p = requests.get(url)
    soup = BeautifulSoup(p.content, 'lxml')
    return(soup)

# setup and retrieving links
def getUrl(soup):

    # other pages
    pages = soup.find('div', class_='paginate-pages').find_all('a',href=True)
    url_set = ["https://letterboxd.com" + page['href'] for page in pages]

    return(url_set)

# main
def main(username):

    mainUrl = ["https://letterboxd.com/" + username + "/films/diary/"]
    mainSoup = init_soup(mainUrl[0])
    url_set = mainUrl + getUrl(mainSoup)

    data_df = init_dframe()

    for url in url_set:
        data_df = diarStats(data_df, url, username)
    
    print("==================================================================================================================")
    print( username + "'s Letterboxd Diary")
    print(data_df)
    print("==================================================================================================================")

    print("Summary stats")
    # genres = getFilmDetails(data_df)
    # print(genres)
    summ = summary(data_df)
    return summ

def init_dframe():
    # create a data frame
    diary = {
        "id": [],
        "film_name": [],
        "film_rating": [],
        "release_date": [],
        "liked":[],
        "reviewed":[],
        "date":[],
    }
    return(pd.DataFrame(diary))

def getDate(entry):
    # month and year
    datetd = entry.find('td', class_='td-day diary-day center')
    date = (datetd.find('a')['href'])[-11:-1].replace("/","-")
    return date

def getFilmDiaryDetails(entry):
    h3 = entry.find_all('h3', class_='headline-3 prettify')[0]
    filmName = h3.find_all('a')[0].text
    relDate = entry.find('td', class_="td-released center").find('span').text

    film_iden = entry.find('div', class_= 'film-poster')['data-film-slug']
    filmURL = "https://letterboxd.com/film/" + film_iden + "/"
    return [filmName, relDate, filmURL]

def getRating(entry):
    rating = entry.find_all('span', class_="rating")
    rated = rating[0].get("class")
    if len(rated)>1:
        userRating = int(float(rated[1][6:]))/2
    else:
        userRating = pd.NA
    return userRating

def getLikeReview(entry):
    liked = False
    liked_data = entry.find('td', class_='td-like center diary-like').find('span', class_="icon-liked")
    if liked_data is not None:
        liked = "Liked"
    else:
        liked = "Not Liked"

    review = False
    review_data = entry.find('td', class_='td-review').find('a')
    if review_data is not None:
        review = "Reviewed"
    else:
        review = "Not Reviewed"

    return [liked, review]

def getRewatch(entry):
    rewatch_td = entry.find('td', class_='td-rewatch center icon-status-off')
    if rewatch_td is None:
        rewatch = True
    else:
        rewatch = False
    return rewatch

def getId(entry):
    id = entry.find('div', class_='film-poster')['data-film-id']
    return id

def diarStats(diary_df, url, username):
    soup = init_soup(url)
    entries = soup.find_all('tr', class_="diary-entry-row") 
    newRows = [pd.DataFrame([ {'id':getId(li), 'film_name': getFilmDiaryDetails(li)[0], 'film_rating': getRating(li),
                            "release_date": getFilmDiaryDetails(li)[1], "liked":getLikeReview(li)[0],
                            "reviewed":getLikeReview(li)[1], "date": getDate(li), "url": getFilmDiaryDetails(li)[2]} ]) for li in entries]
    diary_page = pd.concat( newRows , ignore_index=True)
    diary_df = pd.concat([diary_df, diary_page], ignore_index=True)
    #genre_df = getFilmDetails(entries)
    diary_df = pd.DataFrame(diary_df)
    return diary_df

# summary stats
def summary(df):

    # create df with no duplicates
    df_unique = df.drop_duplicates('id')
    df_unique = df_unique.reset_index()

    # film details
    fdetails = getFilmDetails(df_unique)
    ratingVsAvgRating = pd.DataFrame({'averageRating':fdetails['averageRating'], 'film_rating':df_unique['film_rating'], 'film_name':df_unique['film_name']})
    ratingVsAvgRating = ratingVsAvgRating[pd.to_numeric(ratingVsAvgRating['film_rating'], errors='coerce').notnull()]
    print(ratingVsAvgRating)

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(ratingVsAvgRating)

    # rating mean, min, max
    ratingLis = [round(df_unique["film_rating"].mean(),2), round(df_unique["film_rating"].max(),2), round(df_unique["film_rating"].min(),2)]
    # rating = {
    # 'rating': [round(df_unique["film_rating"].mean(),2), round(df_unique["film_rating"].max(),2), round(df_unique["film_rating"].min(),2)]
    # }

    # rating_df = pd.DataFrame(rating)
    # print("\nYour average rating is " + str(rating_df.at[0, "rating"]));
    # print("Max: " + str(rating_df.at[1, "rating"]) + "           Min: "+ str(rating_df.at[2, "rating"]))

    # liked counts
    liked_df = df_unique.groupby(['liked']).size()
    liked_df = pd.DataFrame(liked_df)
    liked_df = liked_df.reset_index()
    liked_df.columns = ["Liked","Count"]
    # print("\nYou have liked " + str( round( (liked_df.at[1,"count"]/ liked_df["count"].sum())*100 ,2 ) ) + "% of your watched films")
    # print(liked_df)

    # watch frequency counts
    date_df = pd.DataFrame(df.groupby(['date']).size())
    date_df = date_df.reset_index()
    date_df.columns = ['date', 'count']
    start_date = date_df.head(1)['date'].to_string(header=False, index=False)
    end_date = date_df.tail(1)['date'].to_string(header=False, index=False)
    dates = pd.DataFrame(pd.date_range(start_date, end_date))
    dates.columns = ['date']
    def substr(row):
        row = str(row)[:10]
        return row
    dates = dates.applymap(substr)
    # print(dates)
    date_join_df = dates.merge(date_df, left_on='date', right_on='date', how="outer")
    date_join_df = date_join_df.fillna(0)
    print(date_join_df)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(date_join_df)

    # most , least watches
    max = date_df.loc[date_df['count'].idxmax()]
    min = date_df.loc[date_df['count'].idxmin(skipna=True)]

    most = str(max['date'])
    least = str(min['date'])

    datetime_most = datetime.strptime(most, '%Y-%m-%d').strftime('%b %d %Y')
    datetime_least = datetime.strptime(least, '%Y-%m-%d').strftime('%b %d %Y')

    watch_freq_lis = [datetime_most, datetime_least, str(max['count']), str(min['count'])]

    # reviewed counts
    review_df = pd.DataFrame(df_unique.groupby(['reviewed']).size())
    review_df = review_df.reset_index()
    review_df.columns=["reviewed", "count"]
    print(review_df)
    #print("..and reviewed " + str( round( (review_df.at[1,"count"]/ review_df["count"].sum())*100 ,2 ) ) + "% of your watched films")

    # most rewatched
    most_rewatched_id = df.id.mode()[0]
    print( df.query('id == @most_rewatched_id').iloc[[0]]['film_name'] )

    # filmd_df = getFilmDetails(df_unique)

    # top 5 genres
    genre_counts = fdetails.iloc[:,0].to_list()
    genre_df = pd.DataFrame(flatten2D(genre_counts))
    genre_df = pd.DataFrame(genre_df.groupby([0]).size())
    genre_df.columns = ['count']
    print("========== TOP 5 GENRES ==========")
    gcounts = genre_df.sort_values(by='count', ascending=False).head(5)
    print(gcounts)

    # top 5 directors
    director_counts = fdetails.iloc[:,1].to_list()
    dir_df = pd.DataFrame(flatten2D(director_counts))
    dir_df = pd.DataFrame(dir_df.groupby([0]).size())
    dir_df.columns = ['count']
    print("========== TOP 5 DIRECTORS ==========")
    dcounts = dir_df.sort_values(by='count', ascending=False).head(5)
    dcounts = dcounts.reset_index()
    dcounts.columns = ["Director", "No. of Films Watched"]
    print(dcounts)

    # top 5 actors
    actor_counts = fdetails.iloc[:,2].to_list()
    act_df = pd.DataFrame(flatten2D(actor_counts))
    act_df = pd.DataFrame(act_df.groupby([0]).size())
    act_df.columns = ['count']
    
    print("========== TOP 5 ACTORS ==========")
    acounts = act_df.sort_values(by='count', ascending=False).head(5)
    print(acounts)
    acounts = acounts.reset_index()
    acounts.columns = ["Actor", "No. of Films Watched"]
    print(acounts)

    # average movie rating
    df_unique['ave_rating'] = fdetails['averageRating']
    print(df_unique)

    # output
    output = { 'nofilms': len(df), 'liked': liked_df, 'watch_counts': date_join_df,
              'watch_freq': watch_freq_lis, 'review_counts':review_df,
              'ratingVsAvgRating':ratingVsAvgRating, 'mostDirectors':dcounts, 'mostActors':acounts,
              'userRatings':ratingLis};

    return output

def getMostPopularReview(username):
    url = "https://letterboxd.com/" + username + "/"
    soup = init_soup(url)
    film_details = soup.find_all('div', class_="film-detail-content")
    if (film_details is None):
        return None
    else:
        if (len(film_details) == 2 or len(film_details) == 3):
            return { 'status': 'Recent Review ❤︎ ', 'mostPop': getReview(film_details, 0), 'mostPop2': getReview(film_details, 1) }
        if (len(film_details)== 1):
            return { 'status': 'Popular Review ❤︎ ', 'mostPop': getReview(film_details, 0), 'mostPop2': None} # most recent if no popular reviews
        if (len(film_details) == 4):
            return { 'status': 'Popular Review ❤︎ ', 'mostPop':getReview(film_details, 2), 'mostPop2':getReview(film_details, 3) }
    
def getReview(film_details, index):
    review = film_details[index]
    review = [
        review.find('h2', class_="headline-2").text,   # title
        review.find('div', class_="body-text").find('p').text, # revie.w
        review.find('p', class_='like-link-target')['data-count'] # no of likes
    ]
    return review

def getFilmDetails(df):
    url_list = df.iloc[:,8].to_list()
    executor = ThreadPoolExecutor(50)
    results = executor.map(init_soup, url_list)
    d_list2d = [ {'genres': getGenres(soup), 'directors':getDirector(soup), 'actors':getActors(soup), 'averageRating': getAveRating(soup)} for soup in results ]
    d_df = pd.DataFrame(d_list2d)
    return d_df

def getGenres(soup):
    genres = soup.find('div', id='tab-genres').find('div', class_='text-sluglist capitalize').find_all('a')[:5]
    genresList = [ g.text  for g in genres ]
    return(genresList)

def getDirector(soup):
    directors = soup.find('div', id='tab-crew').find('div', class_='text-sluglist').find_all('a')[:5]
    directorList = [  d.text for d in directors ]
    return directorList

def getActors(soup):
    actors = soup.find('div', class_='cast-list text-sluglist').find_all('a')[:5]
    actorsList = [  a.text for a in actors ]
    return actorsList

def getAveRating(soup):
    aveRating_find = soup.find_all('meta', attrs={'name':'twitter:data2'})
    if(aveRating_find is not None):
        aveRating = float(aveRating_find[0]['content'][:4])
        return aveRating
    else:
        return None

def flatten2D(lis):
    flat_lis = [x for l in lis for x in l]
    return(flat_lis)
    
# print(main("essi_17"))

#print(getMostPopularReview('sberrymilky'))
#print(getMostPopularReview('essi_17'))
from bs4 import BeautifulSoup
import requests
import html5lib
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime

# create soup
def init_soup(url):
    p = requests.get(url)
    soup = BeautifulSoup(p.content, 'html5lib')
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
        data_df = diarStats(data_df, url)
    
    print("==================================================================================================================")
    print( username + "'s Letterboxd Diary")
    print(data_df)
    print("==================================================================================================================")

    print("Summary stats")
    summary(data_df)

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
    date = (datetd.find('a')['href'])[-11:-1]
    return date

def getFilmDetails(entry):
    h3 = entry.find_all('h3', class_='headline-3 prettify')[0]
    filmName = h3.find_all('a')[0].text
    relDate = entry.find('td', class_="td-released center").find('span').text
    return [filmName, relDate]

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
        liked = True
    else:
        liked = False

    review = False
    review_data = entry.find('td', class_='td-review').find('a')
    if review_data is not None:
        review = True
    else:
        review = False

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

def diarStats(diary_df, url):
    soup = init_soup(url)
    entries = soup.find_all('tr', class_="diary-entry-row") 
    newRows = [pd.DataFrame([ {'id':getId(li), 'film_name': getFilmDetails(li)[0], 'film_rating': getRating(li),
                            "release_date": getFilmDetails(li)[1], "liked":getLikeReview(li)[0],
                            "reviewed":getLikeReview(li)[1], "date": getDate(li)} ]) for li in entries]
    diary_page = pd.concat( newRows , ignore_index=True)
    diary_df = pd.concat([diary_df, diary_page], ignore_index=True)
    return diary_df

# summary stats
def summary(df):

    # create df with no duplicates
    df_unique = df.drop_duplicates('id')

    # rating mean, min, max
    rating = {
    'rating': [round(df_unique["film_rating"].mean(),2), round(df_unique["film_rating"].max(),2), round(df_unique["film_rating"].min(),2)]
    }

    rating_df = pd.DataFrame(rating)
    print("\nYour average rating is " + str(rating_df.at[0, "rating"]));
    print("Max: " + str(rating_df.at[1, "rating"]) + "           Min: "+ str(rating_df.at[2, "rating"]))

    # liked counts
    liked_df = df_unique.groupby(['liked']).size()
    liked_df = pd.DataFrame(liked_df)
    liked_df.columns = ['count']
    print("\nYou have liked " + str( round( (liked_df.at[0,"count"]/ liked_df["count"].sum())*100 ,2 ) ) + "% of your watched films")
    # print(liked_df)

    # watch frequency counts
    date_df = pd.DataFrame(df.groupby(['date']).size())
    date_df.columns = ['count']
    print(date_df)

    # reviewed counts
    review_df = pd.DataFrame(df_unique.groupby(['reviewed']).size())
    review_df.columns=["count"]
    print("..and reviewed " + str( round( (review_df.at[1,"count"]/ review_df["count"].sum())*100 ,2 ) ) + "% of your watched films")

    # most rewatched
    most_rewatched_id = df.id.mode()[0]
    print( df.query('id == @most_rewatched_id').iloc[[0]]['film_name'] )

    

main("riannecantos")
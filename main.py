from bs4 import BeautifulSoup
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# create soup
def init_soup(url):
    p = requests.get(url)
    soup = BeautifulSoup(p.content, 'lxml')
    return(soup)

# setup and retrieving links
def getUrl(soup):

    # other pages
    pages = soup.find('div', class_='paginate-pages')
    if pages is None:
        return None
    else:
        pages = pages.find_all('a',href=True)
        url_set = ["https://letterboxd.com" + page['href'] for page in pages]

    return(url_set)

# main
def main(username):

    if (len(username)>0):
        if (username[0] == "@"):
            username = username[1:]

    mainUrl = ["https://letterboxd.com/" + username + "/films/diary/"]
    mainSoup = init_soup(mainUrl[0])
    url_set = getUrl(mainSoup)
    if (url_set is None):
        url_set = mainUrl
    else:
        url_set = mainUrl + url_set

    data_df = init_dframe()

    for url in url_set:
        data_df = diarStats(data_df, url, username)
        if (len(data_df) == 0):
            return data_df
    
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
    print(len(newRows))
    if ( len(newRows) == 0):
        return pd.DataFrame()
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
    ratingVsAvgRating = pd.DataFrame({'Average Rating':fdetails['averageRating'], 'Your Rating':df_unique['film_rating'], 'Film Name':df_unique['film_name']})
    ratingVsAvgRating = ratingVsAvgRating[pd.to_numeric(ratingVsAvgRating['Your Rating'], errors='coerce').notnull()]
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
    sorted_date_df = date_df.sort_values('date', ascending=False).reset_index()
    sorted_count_df = sorted_date_df.sort_values('count', ascending=False).reset_index()

    max = sorted_count_df.loc[0,'count']
    max2 = sorted_count_df.loc[1,'count']

    max_date = sorted_count_df.loc[0,'date']
    max2_date = sorted_count_df.loc[1,'date']

    datetime_max = datetime.strptime(max_date, '%Y-%m-%d').strftime('%b %d %Y')
    datetime_max2 = datetime.strptime(max2_date, '%Y-%m-%d').strftime('%b %d %Y')

    watch_freq_lis = [datetime_max, datetime_max2, str(max), str(max2)]

    # max = sorted_date_df.loc[sorted_date_df['count'].idxmax()]
    # min = sorted_date_df.loc[sorted_date_df['count'].idxmin(skipna=True)]

    # most = str(max['date'])
    # least = str(min['date'])

    # datetime_most = datetime.strptime(most, '%Y-%m-%d').strftime('%b %d %Y')
    # datetime_least = datetime.strptime(least, '%Y-%m-%d').strftime('%b %d %Y')

    # most_count = max['count']
    # least_count = min['count']

    # watch_freq_lis = [datetime_most, datetime_least, str(most_count), str(least_count)]

    # reviewed counts
    review_df = pd.DataFrame(df_unique.groupby(['reviewed']).size())
    review_df = review_df.reset_index()
    review_df.columns=["reviewed", "count"]
    print(review_df)
    #print("..and reviewed " + str( round( (review_df.at[1,"count"]/ review_df["count"].sum())*100 ,2 ) ) + "% of your watched films")

    # most rewatched
    mode = df.id.mode()
    most_rewatched_id = mode[0]
    query = pd.DataFrame(df.query('id == @most_rewatched_id')).reset_index()
    rewatched = str(query.at[0,'film_name'])
    rewatchedYear = query.at[0,'release_date']
    rewatchUrl = query.at[0,'url']
    if (len(rewatched)> 40):
        rewatched = rewatched[:38] + "..."
    rewatchTimes = len(query)
    if(rewatchTimes <= 1):
        rewatchedLis = [ "No rewatches logged!", "N/A", "0x rewatched", "placeholder.png" ]
    else:
        rewatchedLis = [ rewatched, str(rewatchedYear), str(rewatchTimes) +  "x watched", str(getFilmPoster(str(rewatchUrl))) ]

    # filmd_df = getFilmDetails(df_unique)

    # top 5 genres
    genre_counts = fdetails.iloc[:,0].to_list()
    genre_df = pd.DataFrame(flatten2D(genre_counts))
    genre_df = pd.DataFrame(genre_df.groupby([0]).size())
    genre_df.columns = ['count']
    print("========== TOP 5 GENRES ==========")
    gcounts = genre_df.sort_values(by='count', ascending=False).head(5)
    gcounts = gcounts.reset_index()
    gcounts.columns = ["Genre", "No. of Films Watched"]
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

    # achievements
    achievementLis = [False, False, False, False, False]

    if (ratingLis[0] < 3):
        achievementLis[0] = True
    if 'Liked' in liked_df['Liked'].values :
        likedQuery = pd.DataFrame(liked_df.query("Liked == 'Liked'")).reset_index()
        likedPrcnt = ( likedQuery.at[0, "Count"]  / liked_df["Count"].sum())
    else: 
        likedPrcnt = 0;
    print(likedPrcnt)
    if (likedPrcnt >= 0.5):
        achievementLis[1] = True
    if (rewatchTimes >= 5):
        achievementLis[2] = True
    print(review_df['reviewed'].values)
    if 'Reviewed' in review_df['reviewed'].values :
        reviewedQuery = pd.DataFrame(review_df.query("reviewed == 'Reviewed'")).reset_index()
        reviewPrcnt = (reviewedQuery.at[0,"count"]/ review_df["count"].sum())
    else:
        reviewPrcnt = 0;
    print(reviewPrcnt)
    if (reviewPrcnt >= 0.5):
        achievementLis[3] = True 
    if (max >= 5):
        achievementLis[4] = True

    # output
    output = { 'nofilms': len(df), 'liked': liked_df, 'watch_counts': date_join_df,
              'watch_freq': watch_freq_lis, 'review_counts':review_df,
              'ratingVsAvgRating':ratingVsAvgRating, 'mostDirectors':dcounts, 'mostActors':acounts,
              'userRatings':ratingLis, 'genre':gcounts, 'rewatch':rewatchedLis,
               'achievements':achievementLis};

    return output

def getMostPopularReview(username):
    if (username[0]=='@'):
        username = username[1:]
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
    # results = [init_soup(u) for u in url_list]
    d_list2d = [ {'genres': getGenres(soup), 'directors':getDirector(soup), 'actors':getActors(soup), 'averageRating': getAveRating(soup)} for soup in results ]
    d_df = pd.DataFrame(d_list2d)
    return d_df

def getGenres(soup):
    genres_find = soup.find('div', id='tab-genres')
    if (genres_find is not None):
        genres = genres_find.find('div', class_='text-sluglist capitalize').find_all('a')[:5]
        genresList = [ g.text  for g in genres ]
        return(genresList)
    else:
        return [""]

def getDirector(soup):
    directors_find = soup.find('div', id='tab-crew')
    if (directors_find is not None):
        directors = directors_find.find('div', class_='text-sluglist').find_all('a')[:5]
        directorList = [  d.text for d in directors ]
        return directorList
    else:
        return [""]

def getActors(soup):
    actors_find = soup.find('div', class_='cast-list text-sluglist')
    if (actors_find is not None):
        actors = actors_find.find_all('a')[:5]
        actorsList = [  a.text for a in actors ]
        return actorsList
    else:
        return [""]

def getAveRating(soup):
    aveRating_find = soup.find_all('meta', attrs={'name':'twitter:data2'})
    if(len(aveRating_find) > 0):
        aveRating = float(aveRating_find[0]['content'][:4])
        return aveRating
    else:
        return None

def flatten2D(lis):
    flat_lis = [x for l in lis for x in l]
    return(flat_lis)

def getFilmPoster(url):
    soup = init_soup(url)
    posterUrl = soup.find('script', type="application/ld+json").text[27:].split("\"")[0]
    posterUrl = posterUrl.split("?")[0]
    return posterUrl
    
# print(main("sberrymilky"))
# print(main("sdjhdffh"))
# print(getFilmPoster("https://letterboxd.com/film/the-social-network/"))
#print(getMostPopularReview('sberrymilky'))
#print(getMostPopularReview('essi_17'))
# print(main("@pur1n"))
# print(main("essi_17"))
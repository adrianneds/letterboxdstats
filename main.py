from bs4 import BeautifulSoup
import requests
import html5lib
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

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
        data_df = diaryStats(data_df, url)
    
    print("==================================================================================================================")
    print( username + "'s Letterboxd Diary")
    print(data_df)
    print("==================================================================================================================")

    print("Summary stats")
    summary(data_df)
    wf = watchFreq(data_df)
    dfList = [data_df, wf]
    return(dfList)

def init_dframe():
    # create a data frame
    diary = {
        "film_name": [],
        "film_rating": [],
        "release_date": [],
        "liked":[],
        "reviewed":[],
        "month_year":[],
    }
    return(pd.DataFrame(diary))

# diary stats of a single page
def diaryStats(diary_df, url):
    soup = init_soup(url)

    # diary entries
    entries = soup.find_all('tr', class_="diary-entry-row") 

    # iterate through entries
    for i in range(0,len(entries)):

        # month and year
        date_div = entries[i].find('div', class_='date')
        if date_div is not None:
            month_year = date_div.find('strong').text + " " + date_div.find('small').text

        # film name
        h3 = entries[i].find_all('h3', class_='headline-3 prettify')[0]
        filmName = h3.find_all('a')[0].text
        # # print(filmName)

        # film rating
        rating = entries[i].find_all('span', class_="rating")
        rated = rating[0].get("class")
        if len(rated)>1:
            userRating = int(float(rated[1][6:]))/2
        else:
            userRating = pd.NA

        # release date
        relDate = entries[i].find('td', class_="td-released center").find('span').text

        # liked ?
        liked = False
        liked_data = entries[i].find('td', class_='td-like center diary-like').find('span', class_="icon-liked")
        if liked_data is not None:
            liked = True
        else:
            liked = False

        # reviewed ?
        review = False
        review_data = entries[i].find('td', class_='td-review').find('a')
        if review_data is not None:
            review = True
        else:
            review = False

        # add info to data frame
        newRow = {'film_name': filmName, 'film_rating':userRating, 
                "release_date": relDate, "liked":liked, "reviewed":review, "month_year": month_year}
        diary_df = pd.concat([diary_df, pd.DataFrame([newRow])], ignore_index=True)

    return(diary_df)

# summary stats
def summary(df):

    # rating mean, min, max
    rating = {
    'rating': [round(df["film_rating"].mean(),2), round(df["film_rating"].max(),2), round(df["film_rating"].min(),2)]
    }

    rating_df = pd.DataFrame(rating)
    print("\nYour average rating is " + str(rating_df.at[0, "rating"]));
    print("Max: " + str(rating_df.at[1, "rating"]) + "           Min: "+ str(rating_df.at[2, "rating"]))

    # liked counts
    liked_df = df.groupby(['liked']).size()
    liked_df = pd.DataFrame(liked_df)
    liked_df.columns = ['count']
    print("\nYou have liked " + str( round( (liked_df.at[0,"count"]/ liked_df["count"].sum())*100 ,2 ) ) + "% of your watched films")
    # print(liked_df)

    # release date counts
    # print(df.groupby(['release_date']).size().max())

    # reviewed counts
    review_df = pd.DataFrame(df.groupby(['reviewed']).size())
    review_df.columns=["count"]
    print("..and reviewed " + str( round( (review_df.at[1,"count"]/ review_df["count"].sum())*100 ,2 ) ) + "% of your watched films")

def watchFreq(df):
    line_df = pd.DataFrame(df.groupby(['month_year']).count()['film_name'])
    heat_df = line_df
    fig = go.Figure(data=[go.Scatter(  x=line_df.index, y=line_df['film_name'] )])

    heat_df = heat_df.reset_index()
    heat_df[['month', 'year']] = heat_df['month_year'].str.split(' ',expand=True)
    heat_df = heat_df.sort_values(by=['year'], ascending=True)
    print(heat_df)

    # fig2 = px.imshow([  ])

    # figs = [fig, fig2]
    return(fig)

main("riannecantos")
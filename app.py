import seaborn as sns
from faicons import icon_svg
from pathlib import Path
import plotly.express as px
import pandas as pd
from main import *
from shinywidgets import output_widget, render_widget  
import matplotlib as plt
import circlify as circlify
import requests as requests

# Import data from shared.py
from shared import app_dir, df

from shiny import App, reactive, render, ui

www_dir = Path(__file__).parent / "www"
js_file = Path(__file__).parent / "www" / "script.js"

app_ui = ui.div(

    # input field
    ui.div(
        ui.p("Enter your Letterboxd username", class_="input-header"),
        ui.input_text(id="inputuser", label="",value="@useruser"),
        ui.input_action_button("submit", "submit", onClick = "observeDiv()"),
        class_ = "container"
    ),

    ui.div(
    # films logged, watch freq
    ui.div(
        ui.div(
            ui.div(
                # number of films logged
                ui.p("You have logged", class_="nofilms_header"), 
                ui.output_text_verbatim("result"),
                ui.p("films", class_="nofilms_header"),
                class_="nofilms_header_container"
            ),
            ui.div(
                # line graph for watch frequency over time
                output_widget("line1"),
                class_="line-container"
            ),
            class_="data-subcontainer"
        ),
        ui.div(
            # most watches 
            ui.p("Most Watches*", class_="watches-header"),
            ui.div(
                ui.div(
                    ui.div(
                        ui.output_text_verbatim("mostWatchesCount"),
                        class_="green-box"
                    ),
                    ui.p("films", class_="films-label"),
                    class_="watches-count-container"
                ),
                ui.output_text_verbatim("mostWatches"),
                class_="watches-container"
                ),

            # least watches
            ui.p("Least Watches*", class_="watches-header"),
            ui.div(
                ui.div(
                    ui.div(
                        ui.output_text_verbatim("leastWatchesCount"),
                        class_="green-box"
                    ),
                    ui.p("films", class_="films-label"),
                    class_="watches-count-container"
                ),
                ui.output_text_verbatim("leastWatches"),
                class_="watches-container"
                ),

            ui.p("most recent watches > 0", class_="desc"),
            ui.img(src="film.png", id="film-img"),
            class_="data-subcontainer2"
        ),
        class_= "data-container"
    ),

    # rev.iew section
    ui.div(
        ui.div(
            ui.output_text_verbatim("popularReviewHeader1"), 
            ui.output_text_verbatim("popularReview1"),    # contains review
            ui.div(
                ui.output_text_verbatim("userNameReview1"),   
                ui.output_text_verbatim("filmTitleReview1"),
                ui.output_text_verbatim("noLikesReview1"),
                class_="review-details"
            ),
            class_="review-subsection"
        ),
        ui.div(
            ui.output_text_verbatim("popularReviewHeader2"), 
            ui.output_text_verbatim("popularReview2"),   # contains review
            ui.div(
                ui.output_text_verbatim("userNameReview2"),   
                ui.output_text_verbatim("filmTitleReview2"),
                ui.output_text_verbatim("noLikesReview2"),
                class_="review-details"
            ),
            class_="review-subsection"
        ),
        ui.div(
            # outputs pie chart for reviewed/not
            ui.div(
                ui.h1("Films Reviewed ✎", id="films-reviewed-header-text"),
                ui.img(src="speech-bubble.png", id="speech-bubble-icon"),
                class_="films-reviewed-header"
            ),
            output_widget("reviewPie"),
            class_="review-subsection"
        ),
        class_="review-section"
    ),
    
    # average rating, most watched directors/actors, liked % section
    ui.div (
        ui.div(
            ui.div(
                ui.h1("Letterboxd Average Rating vs. Your Rating", class_="rating-section-header"),
                output_widget("ratingScatterplot"),
                class_="rating-plot"
            ),
            ui.div(
                ui.div(
                    ui.h1("Most Watched Directors ►", class_="rating-section-header most"),
                    output_widget("mostDirectors"),
                    class_="most-directors"
                ),
                ui.div(
                    ui.h1("Most Watched Actors ►", class_="rating-section-header most"),
                    output_widget("mostActors"),
                    class_="most-actors"
                ),
                class_="bar-graphs"
            ),
            class_="rating-subsection1"
        ),
        ui.div(
            ui.div(
                ui.h1("minimum rating", class_="rating-section-header"),
                ui.output_text_verbatim("minRating"),
                ui.h1("maximum rating", class_="rating-section-header"),
                ui.output_text_verbatim("maxRating"),
                ui.h1("average rating", class_="rating-section-header"),
                ui.output_text_verbatim("aveRating"),
                class_="minmax-ave-rating"
            ),
            ui.div(
                ui.h1("Films Liked ❤︎", class_="rating-section-header"),
                output_widget("likedPie"),
                class_="films-liked-chart"
            ),
            class_="rating-subsection2"
        ),
        class_="rating-section"
    ),

    # genres and most rewatched
    ui.div(
        ui.div(
            ui.h1("Most Watched Genres ➷", class_="genre-rew-header"),
            output_widget("genreBar"),
            class_="genre-bar"
        ),
        ui.div(
            ui.div(
                ui.h1("Most Rewatched Film ↺", class_="genre-rew-header"),
                ui.output_text_verbatim("rewatchFilm"),
                ui.output_text_verbatim("rewatchYear"),
                ui.img(src = "rewatch.png", id="rewatch-icon"),
                ui.div(
                    ui.output_text_verbatim("rewatchTimes"),
                    class_="rewatch-container"
                ),
                class_="rewatch-info"
            ),
            ui.output_ui("rewatchPoster"),
            class_="rewatch-section"
        ),
        class_="genres-rew-section"
    ),

    ui.div(
        ui.output_text_verbatim("usernameProfile"),
        ui.div(
            ui.div(
                ui.output_ui("achievement1"),
                class_="achievement"
            ),
            ui.div(
                ui.output_ui("achievement2"),
                class_="achievement"
            ),
            ui.div(
                ui.output_ui("achievement3"),
                class_="achievement"
            ),
            ui.div(
                ui.output_ui("achievement4"),
                class_="achievement"
            ),
            ui.div(
                ui.output_ui("achievement5"),
                class_="achievement"
            ),
            class_="profile-grid"
        ),
        ui.h1("github: @adrianneds", id="credits"),
        class_="profile-section"
    ),
    id="content-div",
    ),

    # other properties for main container
    ui.include_js(js_file),
    # ui.tags.script("""
    #     const observer = new MutationObserver(() => {
    #         document.getElementById("content-div").style.display = "block";
    #         document.getElementById("content-div").style.visibility = "visible";
    #         console.log("detect")
    #     });

    #     var config = { attributes: true, childList: true, subtree: true };

    #     function observeDiv() {
    #         console.log("aa")
    #         observer.observe(document.querySelector("#content-div"), config);
    #     }
    #                """),
    ui.tags.style("#content-div { display: none; visibility: hidden; } "),
    ui.tags.style("@font-face { font-family: Akzidenz; src: url(Akzidenz-grotesk-bold.woff); } "
    "@font-face { font-family: AkzidenzLight; src: url(Akzidenz-grotesk-ce-light.woff); }" 
    "@font-face { font-family: CooperItalic; src: url(CooperLtBT-Italic.woff) }"),

    ui.tags.style(".data-container, .rating-section, .profile-section { background-image: url(purp-bg.png); }"),
    ui.include_css(app_dir / "style.css"),
    class_ = "main-container"
)

def server(input, output, session):

    user_stats = reactive.value(None)
    user_reviews = reactive.value(None)

    @reactive.effect
    @reactive.event(input.submit, ignore_none=True)
    def submit():
        username = input.inputuser()
        new_stats = main(username)
        user_stats.set(new_stats)
        new_review = getMostPopularReview(username)
        user_reviews.set(new_review)
        return

    @render.text
    def result():
        new_stats = user_stats.get()
        if (new_stats is None):
            return None
        else:
            return str(new_stats['nofilms'])
    
    @render_widget
    def line1():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            df = new_stats['watch_counts']
            fig = px.line(df, x='date', y='count')
            fig.update_traces(line_color='#fc7f01')
            fig.update_yaxes(title_font_color="white", gridcolor='white')
            fig.update_xaxes(title_font_color="white", gridcolor='white')
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            },font_color="white")
            return fig
    
    @render.text
    def mostWatches():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            return new_stats['watch_freq'][0]
        
    @render.text
    def leastWatches():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            return new_stats['watch_freq'][1]
        
    @render.text
    def mostWatchesCount():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            return new_stats['watch_freq'][2]
        
    @render.text
    def leastWatchesCount():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            return new_stats['watch_freq'][3]
        
    # for reviews
    @render.text
    def popularReviewHeader1():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return str(new_reviews['status'])

    @render.text
    def popularReviewHeader2():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return str(new_reviews['status'])

    @render.text
    def popularReview1():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            r = "\"" + str(new_reviews['mostPop'][1]) + "\""
            if (len(r) >= 60):
                return r[:58] + "..." + "\""
            else:
                return r
        
    @render.text
    def popularReview2():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            r = "\"" + str(new_reviews['mostPop2'][1]) + "\""
            if (len(r) >= 60):
                return r[:58] + "..." + "\""
            else:
                return r
        
    @render.text
    def filmTitleReview1():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return "on " + str(new_reviews['mostPop'][0])
        
    @render.text
    def filmTitleReview2():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return "on " + str(new_reviews['mostPop2'][0])
        
    @render.text
    def noLikesReview1():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return str(new_reviews['mostPop'][2]) + " likes ❤︎ "
        
    @render.text
    def noLikesReview2():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return str(new_reviews['mostPop2'][2]) + " likes ❤︎ "
        
    @render.text
    def userNameReview1():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return "—— @" + str(input.inputuser())
        
    @render.text
    def userNameReview2():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            return "—— @" + str(input.inputuser())
        
    @render_widget
    def reviewPie():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            fig = px.pie(new_stats['review_counts'], values="count", names="reviewed", color="reviewed", 
                         color_discrete_map={'Reviewed':'#fc7f01','Not Reviewed':'#ffbf7f'},
                         width=400, height=400)
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            }, legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="right",
                    x=0.8), margin=dict(t=0, b=0, l=0, r=0.2), )
            return fig
        
    @render_widget
    def ratingScatterplot():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            df = new_stats['ratingVsAvgRating']
            fig = px.strip(df, x='Your Rating', y='Average Rating', color="Your Rating", hover_data=['Film Name'], width=900,height=400,
                             color_discrete_map={ 0:"#d9eee1", 0.5: "#d9eee1", 1: "#bee8cd", 1.5: "#bee8cd",
                                                 2: "#a6e7bd", 2.5: "#a6e7bd", 3: "#7ce5a2", 3.5: "#7ce5a2",
                                                  4: "#48e380", 4.5:"#48e380", 5:'#05de54'})
            fig.update_traces(marker=dict(size=13, line=dict(width=1, color='white')))
            fig.update_traces(jitter=1)
            fig.update_yaxes(title_font_color="white", gridcolor="white")
            fig.update_xaxes(title_font_color="white", gridcolor="white")
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            },font_color="white")
            return fig
        
    @render_widget
    def mostDirectors():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            df = new_stats['mostDirectors']
            fig = px.bar(df, x="No. of Films Watched", y="Director", 
                         orientation='h', color_discrete_sequence=["#40baf1"],
                         width=450, height=400)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            },font_color="white")
            return fig
        
    @render_widget
    def mostActors():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            df = new_stats['mostActors']
            fig = px.bar(df, x="No. of Films Watched", y="Actor",
                         orientation='h', color_discrete_sequence=["#05de54"],
                         width=450, height=400)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            },font_color="white")
            return fig
        
    @render.text
    def minRating():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            min = new_stats['userRatings'][2]
            return str(min) + "★"
        
    @render.text
    def maxRating():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            max = new_stats['userRatings'][1]
            return str(max) + "★"
        
    @render.text
    def aveRating():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            ave = new_stats['userRatings'][0]
            return str(ave) + "★"
        
    @render_widget
    def likedPie():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            df = new_stats['liked']
            fig = px.pie(df, values="Count", names="Liked", color="Liked", 
                color_discrete_map={'Liked':'#fc7f01','Not Liked':'#ffbf7f'},
                width=300, height=300)
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            }, legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="right",
                    x=0.8), margin=dict(t=0, b=0, l=0, r=0.2), font_color="white")
            return fig
        
    @render_widget
    def genreBar():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            df = new_stats['genre']
            fig = px.bar(df, x="No. of Films Watched", y="Genre",
                         orientation='h', color_discrete_sequence=["#fc7f01"],
                         width=550, height=400)
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
        return fig
    
    @render.text
    def rewatchFilm():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            return new_stats['rewatch'][0]
        
    @render.text
    def rewatchYear():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            return new_stats['rewatch'][1]
        
    @render.text
    def rewatchTimes():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            return new_stats['rewatch'][2] + "x watched"
        
    @render.ui
    def rewatchPoster():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            url = str(new_stats['rewatch'][3]).strip()
            #url = requests.get(url)
            #img = {"src": url, "width": "230px", "height": "345px"}  
            return ui.tags.img(src=url, width=230, height=345)
        
    @render.text
    def usernameProfile():
        return str(input.inputuser()) + "'s Watch Profile";

    @render.ui
    def achievement1():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            ac1 = new_stats['achievements'][0]
            if (ac1):
                img = ui.tags.img(src = "achievement1_true.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement2-header, #achievement2-desc { color: #e7e9eb }" )
            else:
                img = ui.tags.img(src = "achievement1_false.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement1-header, #achievement1-desc { color: #585858 }" )
            header = ui.tags.h2("No Hard Feelings", id="achievement1-header")
            desc = ui.tags.p("average rating below 3", id="achievement1-desc")
            info_container = ui.tags.div(header, desc, class_="info-container")
            container = ui.tags.div(img, info_container, styles, class_="achievement-container")
            return container
        
    @render.ui
    def achievement2():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            ac1 = new_stats['achievements'][1]
            if (ac1):
                img = ui.tags.img(src = "achievement2_true.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement2-header, #achievement2-desc { color: #e7e9eb }" )
            else:
                img = ui.tags.img(src = "achievement2_false.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement2-header, #achievement2-desc { color: #585858 }" )
            header = ui.tags.h2("Good Time", id="achievement2-header"),
            desc = ui.tags.p("liked majority of logged films", id="achievement2-desc")
            info_container = ui.tags.div(header, desc, class_="info-container")
            container = ui.tags.div(img, info_container, styles, class_="achievement-container")
            return container

    @render.ui
    def achievement3():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            ac1 = new_stats['achievements'][2]
            if (ac1):
                img = ui.tags.img(src = "achievement3_true.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement3-header, #achievement3-desc { color: #e7e9eb }" )
            else:
                img = ui.tags.img(src = "achievement3_false.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement3-header, #achievement3-desc { color: #585858 }" )
            header = ui.tags.h2("Certified Copy", id="achievement3-header"),
            desc = ui.tags.p("rewatched a film at least 5 times", id="achievement3-desc")
            info_container = ui.tags.div(header, desc, class_="info-container")
            container = ui.tags.div(img, info_container, styles, class_="achievement-container")
            return container

    @render.ui
    def achievement4():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            ac1 = new_stats['achievements'][3]
            if (ac1):
                img = ui.tags.img(src = "achievement4_true.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement4-header, #achievement4-desc { color: #e7e9eb }" )
            else:
                img = ui.tags.img(src = "achievement4_false.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement4-header, #achievement4-desc { color: #585858 }" )
            header = ui.tags.h2("The Social Network", id="achievement4-header"),
            desc = ui.tags.p("reviewed at least 50% of logged films", id="achievement4-desc")
            info_container = ui.tags.div(header, desc, class_="info-container")
            container = ui.tags.div(img, info_container, styles, class_="achievement-container")
            return container
        
    @render.ui
    def achievement5():
        new_stats = user_stats.get()
        if new_stats is None:
            return None
        else:
            ac1 = new_stats['achievements'][4]
            if (ac1):
                img = ui.tags.img(src = "achievement5_true.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement5-header, #achievement5-desc { color:  #e7e9eb }" )
            else:
                img = ui.tags.img(src = "achievement5_false.png", width= 100, height=110, class_="achievement-img")
                styles = ui.tags.style( " #achievement5-header, #achievement5-desc { color: #585858 }" )
            header = ui.tags.h2("After Hours", id="achievement5-header"),
            desc = ui.tags.p("logged at least 5 films in one day", id="achievement5-desc")
            info_container = ui.tags.div(header, desc, class_="info-container")
            container = ui.tags.div(img, info_container, styles, class_="achievement-container")
            return container

app = App(app_ui, server, static_assets=www_dir, debug=False)

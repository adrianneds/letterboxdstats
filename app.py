import seaborn as sns
from faicons import icon_svg
from pathlib import Path
import plotly.express as px
import pandas as pd
from main import *
from shinywidgets import output_widget, render_widget  

# Import data from shared.py
from shared import app_dir, df

from shiny import App, reactive, render, ui

www_dir = Path(__file__).parent / "www"

app_ui = ui.div(

    # input field
    ui.div(
        ui.p("Enter your Letterboxd username", class_="input-header"),
        ui.input_text(id="inputuser", label="",value="@useruser"),
        ui.input_action_button("submit", "submit"),
        class_ = "container"
    ),

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
                ui.h1("Films Reviewed", id="films-reviewed-header-text"),
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
                class_="rating-plot"
            ),
            ui.div(
                ui.div(
                    class_="most-directors"
                ),
                ui.div(
                    class_="most-actors"
                ),
                class_="bar-graphs"
            ),
            class_="rating-subsection"
        ),
        ui.div(
            ui.div(
                class_="minmax-ave-rating"
            ),
            ui.div(
                class_="films-liked-chart"
            ),
            class_="rating-subsection"
        ),
        class_="rating-section"
    ),

    # other properties for main container
    ui.tags.style("@font-face { font-family: Akzidenz; src: url(Akzidenz-grotesk-bold.woff); } "
    "@font-face { font-family: AkzidenzLight; src: url(Akzidenz-grotesk-ce-light.woff); }" 
    "@font-face { font-family: CooperItalic; src: url(CooperLtBT-Italic.woff) }"),

    ui.tags.style(".data-container { background-image: url(purp-bg.png); }"),
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
            fig.update_yaxes(title_font_color="white")
            fig.update_xaxes(title_font_color="white")
            fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
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
            if (len(r) >= 55):
                return r[:52] + "..." + "\""
            else:
                return r
        
    @render.text
    def popularReview2():
        new_reviews = user_reviews.get()
        if new_reviews is None:
            return None
        else:
            r = "\"" + str(new_reviews['mostPop2'][1]) + "\""
            if (len(r) >= 55):
                return r[:52] + "..." + "\""
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
                    x=0.8), margin=dict(t=0, b=0, l=0, r=0.2))
            return fig
    return

app = App(app_ui, server, static_assets=www_dir, debug=False)

# app_ui = ui.page_sidebar(
#     ui.sidebar(
#         ui.input_slider("mass", "Mass", 2000, 6000, 6000),
#         ui.input_checkbox_group(
#             "species",
#             "Species",
#             ["Adelie", "Gentoo", "Chinstrap"],
#             selected=["Adelie", "Gentoo", "Chinstrap"],
#         ),
#         title="Filter controls",
#     ),
#     ui.layout_column_wrap(
#         ui.value_box(
#             "Number of penguins",
#             ui.output_text("count"),
#             showcase=icon_svg("earlybirds"),
#         ),
#         ui.value_box(
#             "Average bill length",
#             ui.output_text("bill_length"),
#             showcase=icon_svg("ruler-horizontal"),
#         ),
#         ui.value_box(
#             "Average bill depth",
#             ui.output_text("bill_depth"),
#             showcase=icon_svg("ruler-vertical"),
#         ),
#         fill=False,
#     ),
#     ui.layout_columns(
#         ui.card(
#             ui.card_header("Bill length and depth"),
#             ui.output_plot("length_depth"),
#             full_screen=True,
#         ),
#         ui.card(
#             ui.card_header("Penguin data"),
#             ui.output_data_frame("summary_statistics"),
#             full_screen=True,
#         ),
#     ),
#     ui.include_css(app_dir / "styles.css"),
#     title="Penguins dashboard",
#     fillable=True,
# )


# def server(input, output, session):
#     @reactive.calc
#     def filtered_df():
#         filt_df = df[df["species"].isin(input.species())]
#         filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
#         return filt_df

#     @render.text
#     def count():
#         return filtered_df().shape[0]

#     @render.text
#     def bill_length():
#         return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

#     @render.text
#     def bill_depth():
#         return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

#     @render.plot
#     def length_depth():
#         return sns.scatterplot(
#             data=filtered_df(),
#             x="bill_length_mm",
#             y="bill_depth_mm",
#             hue="species",
#         )

#     @render.data_frame
#     def summary_statistics():
#         cols = [
#             "species",
#             "island",
#             "bill_length_mm",
#             "bill_depth_mm",
#             "body_mass_g",
#         ]
#         return render.DataGrid(filtered_df()[cols], filters=True)
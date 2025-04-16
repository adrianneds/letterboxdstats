# from flask import Flask, request, render_template, url_for, g
# from dash.dependencies import Input, State, Output
# import ssl
# import pandas as pd
# app = Flask(__name__)
# from dash import Dash, dcc, html, Input, Output, callback
# from main import *

# app = Dash()

# app.layout = html.Div(
#     className = "container",
#     children=[
#         html.H1("Enter your letterboxd username", id = "enterUser"),
#         # input field
#             dcc.Input(
#             id="inputuser".format("text"),
#             type="text",
#             placeholder="@useruser on letterboxd".format("text"),
#             value = '',
#             style={"width":"300px", "height": "30px", "margin-top":"5%"}
#             ),
#         html.Button('Submit', type = 'submit', id='submitButton', style={"margin-top":"1.5%"}),
#         html.H1(id='no_films',children=""),
#         html.Div(id='pie', children="")
#     ]
# )

# # process input
# @app.callback(
#     Output("no_films", "children"),  
#     Input("submitButton", "n_clicks"),  
#     State("inputuser", "value")  
# )

# @app.callback(
#     Output("pie", "children"),  
#     Input("submitButton", "n_clicks"),  
#     State("inputuser", "value")  
# )

# # do something with the input username
# def update_output(n_clicks, username):
#     if n_clicks > 0:  
#         return f"You've logged {generateStats(username)['nofilms']} films"
    
# # do something with the input username
# def update_output2(n_clicks, username):
#     if n_clicks > 0:  
#         return dcc.Graph(generatePieLiked(generateStats(username)))
    
# def generateGraphs(username):
#     user_stats = generateStats(username)
#     container = html.Div(className="container container2",
#                          children = [
#                          html.H1("You've logged" + user_stats['nofilms'] + " films"),
#                          dcc.Graph(figure=generatePieLiked(user_stats)),
#                          ])
#     return container
    
# def generateStats(username):
#     user_stats = main(username)
#     return user_stats
    
# def generatePieLiked(user_stats):
#    df = user_stats['liked']
#    fig = px.pie(df, values="count", hole=.3)
#    return fig

# def generatePieRev(user_stats):
#    df = user_stats['liked']
#    fig = px.pie(df, values="count", hole=.3)
#    return fig

# if __name__ == "__main__":
#     app.run(debug=True)
    


# #     g.cur_app = app

# #     # Add Dash app to Flask context. Specify the app's url path and pass the flask server to your data
# #     # app = simple_app.init_app("/simple_app/")
# #     # app = population.init_app("/population/")


# import faicons as fa
# import plotly.express as px

# # Load data and compute static values
# from shared import app_dir, tips
# from shinywidgets import render_plotly

# from shiny import reactive, render
# from shiny.express import input, ui

# bill_rng = (min(tips.total_bill), max(tips.total_bill))

# # Add page title and sidebar
# ui.page_opts(title="Restaurant tipping", fillable=True)

# with ui.sidebar(open="desktop"):
#     ui.input_slider(
#         "total_bill",
#         "Bill amount",
#         min=bill_rng[0],
#         max=bill_rng[1],
#         value=bill_rng,
#         pre="$",
#     )
#     ui.input_checkbox_group(
#         "time",
#         "Food service",
#         ["Lunch", "Dinner"],
#         selected=["Lunch", "Dinner"],
#         inline=True,
#     )
#     ui.input_action_button("reset", "Reset filter")

# # Add main content
# ICONS = {
#     "user": fa.icon_svg("user", "regular"),
#     "wallet": fa.icon_svg("wallet"),
#     "currency-dollar": fa.icon_svg("dollar-sign"),
#     "ellipsis": fa.icon_svg("ellipsis"),
# }

# with ui.layout_columns(fill=False):
#     with ui.value_box(showcase=ICONS["user"]):
#         "Total tippers"

#         @render.express
#         def total_tippers():
#             tips_data().shape[0]

#     with ui.value_box(showcase=ICONS["wallet"]):
#         "Average tip"

#         @render.express
#         def average_tip():
#             d = tips_data()
#             if d.shape[0] > 0:
#                 perc = d.tip / d.total_bill
#                 f"{perc.mean():.1%}"

#     with ui.value_box(showcase=ICONS["currency-dollar"]):
#         "Average bill"

#         @render.express
#         def average_bill():
#             d = tips_data()
#             if d.shape[0] > 0:
#                 bill = d.total_bill.mean()
#                 f"${bill:.2f}"


# with ui.layout_columns(col_widths=[6, 6, 12]):
#     with ui.card(full_screen=True):
#         ui.card_header("Tips data")

#         @render.data_frame
#         def table():
#             return render.DataGrid(tips_data())

#     with ui.card(full_screen=True):
#         with ui.card_header(class_="d-flex justify-content-between align-items-center"):
#             "Total bill vs tip"
#             with ui.popover(title="Add a color variable", placement="top"):
#                 ICONS["ellipsis"]
#                 ui.input_radio_buttons(
#                     "scatter_color",
#                     None,
#                     ["none", "sex", "smoker", "day", "time"],
#                     inline=True,
#                 )

#         @render_plotly
#         def scatterplot():
#             color = input.scatter_color()
#             return px.scatter(
#                 tips_data(),
#                 x="total_bill",
#                 y="tip",
#                 color=None if color == "none" else color,
#                 trendline="lowess",
#             )

#     with ui.card(full_screen=True):
#         with ui.card_header(class_="d-flex justify-content-between align-items-center"):
#             "Tip percentages"
#             with ui.popover(title="Add a color variable"):
#                 ICONS["ellipsis"]
#                 ui.input_radio_buttons(
#                     "tip_perc_y",
#                     "Split by:",
#                     ["sex", "smoker", "day", "time"],
#                     selected="day",
#                     inline=True,
#                 )

#         @render_plotly
#         def tip_perc():
#             from ridgeplot import ridgeplot

#             dat = tips_data()
#             dat["percent"] = dat.tip / dat.total_bill
#             yvar = input.tip_perc_y()
#             uvals = dat[yvar].unique()

#             samples = [[dat.percent[dat[yvar] == val]] for val in uvals]

#             plt = ridgeplot(
#                 samples=samples,
#                 labels=uvals,
#                 bandwidth=0.01,
#                 colorscale="viridis",
#                 colormode="row-index",
#             )

#             plt.update_layout(
#                 legend=dict(
#                     orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5
#                 )
#             )

#             return plt


# ui.include_css(app_dir / "styles.css")

# # --------------------------------------------------------
# # Reactive calculations and effects
# # --------------------------------------------------------


# @reactive.calc
# def tips_data():
#     bill = input.total_bill()
#     idx1 = tips.total_bill.between(bill[0], bill[1])
#     idx2 = tips.time.isin(input.time())
#     return tips[idx1 & idx2]


# @reactive.effect
# @reactive.event(input.reset)
# def _():
#     ui.update_slider("total_bill", value=bill_rng)
#     ui.update_checkbox_group("time", selected=["Lunch", "Dinner"])

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
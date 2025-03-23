from flask import Flask, request, render_template, url_for, g
from dash.dependencies import Input, State, Output
import ssl
import pandas as pd
app = Flask(__name__)
from dash import Dash, dcc, html, Input, Output, callback
from main import *

app = Dash()

app.layout = html.Div(
    id = "container",
    children=[
        html.H1("Enter your letterboxd username", id = "enterUser"),
        # input field
            dcc.Input(
            id="inputuser".format("text"),
            type="text",
            placeholder="@useruser on letterboxd".format("text"),
            value = '',
            style={"width":"300px", "height": "30px", "margin-top":"5%"}
            ),
        html.Button('Submit', type = 'submit', id='submitButton', style={"margin-top":"1.5%"}),
        html.Div(id='output')
    ]
)

# Callback function to process input
@app.callback(
    Output("output", "children"),  # Updates the output div
    Input("submitButton", "n_clicks"),  # Triggers on button click
    State("inputuser", "value")  # Captures user input
)

def update_output(n_clicks, username):
    if n_clicks > 0:  
        return f"Input: {username}"
    else:
        "Please enter a username."

if __name__ == "__main__":
    app.run(debug=True)




#     g.cur_app = app

#     # Add Dash app to Flask context. Specify the app's url path and pass the flask server to your data
#     # app = simple_app.init_app("/simple_app/")
#     # app = population.init_app("/population/")

from flask import Flask, request, render_template, url_for, g
import ssl
import pandas as pd
app = Flask(__name__)

with app.app_context():
    
    g.cur_app = app

    # Add Dash app to Flask context. Specify the app's url path and pass the flask server to your data
    # app = simple_app.init_app("/simple_app/")
    # app = population.init_app("/population/")

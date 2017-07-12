from flask import Flask

app = Flask(__name__)

from app import views

#script creates application object of class Flask, imports the views module
#views are handlers that respond to web browser reqs, written as python
#functions.


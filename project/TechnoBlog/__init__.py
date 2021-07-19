#It is to estaiblish the following
#1)the database i.e. sqlite3
#2)sqlalchemy(so that we can directly use classes instead of using rows and column based database)
#3)bcrypt(so that we can use for encrypting passwords)
#4)Login Manager(to handle the login-logout sessions defining access of user and prevent from cookies performing unethical logging and also manages remember me)
#5)mail system
#and then finally calling routes.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

#in this step we are creating module by passing 
#main inthe argument of imported package FLask to create module 
#IT IS INSTANTIATING FLASK APP
app = Flask(__name__)
#Application need some kind of configuration.There are different settings you might 
#want to change depending on the application environment like toggling the debug mode 
#setting the secret key and other ssuch environmental-specific things.
#the way Flask is designed usually requires the configuration to be available
#the application starts up.You can hard code the configuration inthe code ,
#which for many small application is not actually that bad ,but there are other ways
#Independent of how you load your config ,there is a config object available 
#which holds the loaded configuration value. The config attributes of the flask object.
#This is the place where Flask itself puts certain configuration values and also
#where extensions can put their configuration values. But this is also where you can have your own configuration  
#WE NEED A SECRET KEY FROM FLASK LOGIN TO DEAL WITH CONFIGURATION VALUES
#this is a standard secret key to use whenever we want
#one use is in creating the token
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#conn=sqlite3.connect(:'site.db':) wale kaam ko generalize kiya jaa raha h
#basically creating a database
#CONFIGURING THE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#sql alchemy is object relational modeling library for python and orm
#it allow us to take oop constructs like classes,methods,constructors and relate them
# to web application
#it better because it let us work in classes for web development rather than 
#struggling with rows and column of sql
#HERE WE ARE INSTANTIATING THE DATABASE
#WE NEED TO CREATE DATABASE IN SQLITE ON OUR OWN
db = SQLAlchemy(app)
#For sensitive data that must be protected, such as passwords, bcrypt is an advisable choice.
#so that it can be used in future
bcrypt = Bcrypt(app)
#flask login is an extension in flask that allow us to manage our user sessions
#it is basically to define who ia who 
#login manager is for instantiating the flask login extension
#here we are also instantiating it
login_manager = LoginManager(app)
# Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time.

# It will:

# Store the active user’s ID in the session, and let you log them in and out easily.
# Let you restrict views to logged-in (or logged-out) users.
# Handle the normally-tricky “remember me” functionality.
# Help protect your users’ sessions from being stolen by cookie thieves.
# Possibly integrate with Flask-Principal or other authorization extensions later on.
# However, it does not:

# Impose a particular database or other storage method on you. You are entirely in charge of how the user is loaded.
# Restrict you to using usernames and passwords, OpenIDs, or any other method of authenticating.
# Handle permissions beyond “logged in or not.”
# Handle user registration or account recovery.
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#Estaiblishing the configurartions to send the email
#PLATFORM THAT I WNAT TO USE
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#PORT NO.
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#PROVIND USERNAME WHICH IS SAVED IN AS ENVIRONMENTAL VARIABLE AND ALSO SAME GOES FOR THE PASSWORD
# app.config['MAIL_USERNAME'] = os.environ.get('USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_USERNAME'] = 'doctoranytime0@gmail.com'
app.config['MAIL_PASSWORD'] = 'BugHunterSquad'
mail = Mail(app)

from TechnoBlog import routes
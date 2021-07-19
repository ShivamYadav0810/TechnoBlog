import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from TechnoBlog import app, db, bcrypt, mail
from TechnoBlog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from TechnoBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from newsapi import NewsApiClient
import yfinance as yf
import requests
import pandas_datareader as pdr
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
import math
from datetime import datetime
import matplotlib.pyplot as plt
import numpy
from PIL import Image
#Creating decorator for home page
#routes are basically for if we want to navigate between pages
#decorator are to add additional functionality to existing function and in this case this app.route 
#will handle all the complicated backend stuff and simply allow us to write a function that returns 
#the information that will be shown on a website for this specific route
#"/"it denotes the root page of our website

from requests import Request,Session
from requests.exceptions import ConnectionError,Timeout,TooManyRedirects
import json
data={}
url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters={
    'start':'1',
    'limit':'1',
    'convert':'USD'
}
headers={
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY':'18e46709-d689-430c-8aa3-8c0fadf3e649'
}
session=Session()
session.headers.update(headers)
response=session.get(url,params=parameters)
data=json.loads(response.text)

@staticmethod
def verify_reset_token(token):
    s=serializer(app.config['SECRET_KEY'])
    try:
        user_id=s.loads(token)['user_id']
    except:
        return none
    return User.query.get(user_id)

@app.route("/")
@app.route("/home")
def home():
    #when we have large no. of blogs then it is quite unconventional 
    #to load all the blogs all that once so we paginate our page which 
    #means that we can load certain no. of blogs on page and provide a link 
    #to access rest of pages
    
    page=request.args.get('page',1,type=int)
    #setting type =int wil cause our site to throw a value error 
    #if someone tries passing anything other then integer other than 
    #integer as page no
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    # str=form.content.data
    # iny=[str]
    # vect=cv.transform(iny).toarray()
    # my_prediction = clf.predict(vect)
    # tr=""
    # if my_prediction[0]==0:
    #     tr="Quality"
    # elif my_prediction[0]==1:
    #     tr="Spam"
    
    
    # if my_prediction==0
    return render_template('home.html', posts=posts)
    # from render_template not only we can pass an html page which is to be displayed on webpage 
    #but also we can pass an variable which we can access in html file
    #tamplating engine that flask uses is called jinja tool and it allow us to write code within the template

@app.route("/about")
def about():
    return render_template('about.html', title='About')
    #get and post enable us to interact directly with webpages send and recieve response

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        #creating reference variable(object/instance) of registration class 
    form = RegistrationForm()
    #On the above created object all the validates are true pass the following message adn redirect them to home page
    if form.validate_on_submit():
        #before giving information that your id is created we need to hash the password and create an instance of User class 
        #and passing details like username,amail,hashed_password to an instance of all data and then comiting it to the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
        #else return back to registration page
    return render_template('register.html', title='Register', form=form)
    #here we are creating a class whenever we enter info in registration form via routes.py we are passing the information to this class
    #here we apply certain checks on the data and inthe the end return an object of its class which is then commited to database
    #via routes.py also here we estaiblish a connection between our registration details and posts having author as the primary key
  

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        #currently a sample username password is given to check for valid login
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #now we need to create a condition that simontanously checks that the user exists and that their password verifies with what they have in database
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#we donot want to keep the name if the that they uploaded because it may collided with name of image that may already be present in our folder
#root path attribute:it will give our root pathof our app to our package directory 
#we need to resize the image becuase the image size in css is set to 125pixels hence it doesnot make sense if we try to uplaod an image of 4000 pixels
#if will take up both space and time
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#we need to create a function to check the validation of tobe uploaded profile pic


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #to update profile picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            #to update the new username
        current_user.username = form.username.data
        #to update the new email
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        #if nothing is updated
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')
# @app.route("/post/<int:post_id>/delete",method=['POST'])
# @login_required
# def  delete_post(post_id):
#     post=Post.query.get_or_404(post_id)
#     if post.author!=current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted','success')
#     return redirect(url_for('home'))


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='doctoranytime0@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



@app.route("/Index")
def Index():
    newsapi = NewsApiClient(api_key="d6f0ac4d31384c72a7e907bf89b51ab4")
    topheadlines = newsapi.get_top_headlines(sources="al-jazeera-english")


    articles = topheadlines['articles']

    desc = []
    news = []
    img = []


    for i in range(len(articles)):
        myarticles = articles[i]


        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])



    mylist = zip(news, desc, img)


    return render_template('index.html', context = mylist)


@app.route("/stocks")
def stocks():
    
    key="27631707bf4f333ecc64b6c34e7d58d993d23969"
    df = pdr.get_data_tiingo('AAPL', api_key=key)
    df.to_csv('AAPL.csv')
    df=pd.read_csv('AAPL.csv')
    df1=df.reset_index()['close']
    scaler=MinMaxScaler(feature_range=(0,1))
    df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
    training_size=int(len(df1)*0.65)
    test_size=len(df1)-training_size
    train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-time_step-1):
            a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return numpy.array(dataX), numpy.array(dataY)
    time_step = 100
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, ytest = create_dataset(test_data, time_step)
    X_train=X_train.reshape(-1,1,100)
    X_test=X_test.reshape(-1,1,100)
    # X_train=X_train.reshape(-1,1,100)
    model=Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(1,100)))
    model.add(LSTM(50,return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',optimizer='adam')
    model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)
    x_input=test_data[340:].reshape(1,-1)
    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()
    lst_output=[]
    n_steps=100
    i=0
    while(i<30):
    
        if(len(temp_input)>100):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, n_steps,1))
            yhat = model.predict(x_input, verbose=0)
            print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1
    day_new=np.arange(1,101)
    day_pred=np.arange(101,131)
    df3=scaler.inverse_transform(df3).tolist()
    df3=df1.tolist()
    df3.extend(lst_output)
    p=plt.plot(df3[1200:])
    now = datetime.now()
    month = now.strftime("%m")
    day=now.strftime("%d")
    year=now.strftime("%Y")
    date1=month+":"+day+":"+year+".jpg"
    plt.savefig(date1,dpi=300,bbox_inches='tight')
    date2=month+":"+day+":"+year+"2"+".jpg"
    plt.savefig(date2,dpi=300,bbox_inches='tight')
    img1 = Image.open(date1)
    img2= Image.open(date2)
    mylist = zip(img1, img2)
    return render_template('index.html', context = mylist)



# API Route for pulling the stock quote
@app.route("/quote")
def display_quote():
    # get a stock ticker symbol from the query string
    # default to AAPL
    symbol = request.args.get('symbol', default="AAPL")

    # pull the stock quote
    quote = yf.Ticker(symbol)

    #return the object via the HTTP Response
    return quote.info

# API route for pulling the stock history
@app.route("/history")
def display_history():
    #get the query string parameters
    symbol = request.args.get('symbol', default="AAPL")
    period = request.args.get('period', default="1y")
    interval = request.args.get('interval', default="1mo")

    #pull the quote
    quote = yf.Ticker(symbol)   
    #use the quote to pull the historical data from Yahoo finance
    hist = quote.history(period=period, interval=interval)
    #convert the historical data to JSON
    data = hist.to_json()
    #return the JSON in the HTTP response
    return data

# This is the / route, or the main landing page route.
@app.route("/Stock")
def Stock():
    # we will use Flask's render_template method to render a website template.
    return render_template("homepage.html")
    
@app.route("/crypto")
def crypto():
    time=data['status']['timestamp']
    name=data['data'][0]['name']
    symbol=data['data'][0]['symbol']
    market_pairs=data['data'][0]['num_market_pairs']
    date_updated=data['data'][0]['date_added']
    max_supply=data['data'][0]['max_supply']
    circulating=data['data'][0]['circulating_supply']
    total_supply=data['data'][0]['total_supply']
    rank=data['data'][0]['cmc_rank']
    price=data['data'][0]['quote']['USD']['price']
    volume=data['data'][0]['quote']['USD']['volume_24h']
    per_change_1h=data['data'][0]['quote']['USD']['percent_change_1h']
    per_change_24h=data['data'][0]['quote']['USD']['percent_change_24h']
    per_change_7d=data['data'][0]['quote']['USD']['percent_change_7d']
    per_change_30h=data['data'][0]['quote']['USD']['percent_change_30d']
    market_cap=data['data'][0]['quote']['USD']['market_cap']
    return render_template("crypto.html",time=time,name=name,symbol=symbol,market_pairs=market_pairs,date_updated=date_updated,max_supply=max_supply,circulating=circulating,total_supply=total_supply,rank=rank,price=price,volume=volume,per_change_1h=per_change_1h,per_change_24h=per_change_24h,per_change_7d=per_change_7d,per_change_30h=per_change_30h,market_cap=market_cap)





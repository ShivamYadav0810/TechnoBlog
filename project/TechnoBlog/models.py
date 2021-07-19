#using sqlalchemy we can represent our databse as class and they are called models
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from TechnoBlog import db, login_manager,app
from flask_login import UserMixin

#we add some functionality to our database models and then it will handle all the sessions in the background
#for reloading the user from userid store in the seesion 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#we need to provide some methods for flask-login(abstraction)
#1)Authentication:it will return true if they have provided valid credentials 
#2)IsActive
#3)IAnonymous
#4)getID
#Lol! instead of doing all that we will i,port a class called mixin
 #here we are creating a class whenever we enter info in registration form via routes.py we are passing the information to this class
    #here we apply certain checks on the data and inthe the end return an object of its class which is then commited to database
    #via routes.py also here we estaiblish a connection between our registration details and posts having author as the primary key
#user mixin provides some methods for using login manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
     #adding a post feild in user class to estailblish relation between author column and post using backref
    #lazy argument just to find when sql alchemy loads the data from database=true means sql alchemy will load the data as necessary in one go because with relationship we will be able to use this post attribute to get all the post crated by an indivitual author 
    #in user class we are using P Post which is not scase while usimg User this is because with user modeule we are referencing the actual post class and inthe foreign we are referencing table name and  column name So user module has the table name and column foreign we are refferencing table name and column name So user module has the table name at lower case and post module will have the table name automatically set to lower case post 
    
    posts = db.relationship('Post', backref='author', lazy=True)
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
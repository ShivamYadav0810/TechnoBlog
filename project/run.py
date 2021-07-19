#it is initializing the app 
#SERVERS ARE INBUILD h
#methods to run FLask application :
#1)in cmd type
#set FLASK_APP=TechnoBlog.py
#run flask
#2)create a function in python file 
#if __name__=__main__:
#   app.run(debug=true)
from TechnoBlog import app


if __name__ == '__main__':
    app.run(debug=True)
print("hell0")
form itsdangerous import TimedJSONWebSignatureSerializer as serializer
#now we are going to use this serializer and pass an secret key and an expiration time  in seconds
#expiration time is 30 sec
s=serializer('secret',30)
#now to generate a token we can use the dump s method and then pass a payload that will be our user_id
token=s.dumps({'user_id':1}).decode('utf-8')
#now we have a token with expiration of 30sec
#token will be a long string of characters that is valid for 30sec
s.loads=(token)
#this will give us the user id basically we have stored a userid ?or in development case an link and a token for verification of id which is valid for 30 sec
#now we need to create this token on user request
    #creating a method to create tokens
    def get_reset_token(self,expires_sec=1800):
        s=Serializer(app.config['SECRET_KEY'],expires_sec)
        #returning a token created here
        #returning userid and userid will be instance of this user 
        #we are simply setting this up with our secret key and an expiration time and the we are returning that token which is created by dumps method and also contains a payload of the current user id 
        return s.dumps({'user_id':self.id}).decode('utf-8')
    #creating a method for verifying this token
    #this method doesnot user any instances so we need to tell python that it is a static method
    #we basically we are telling python not to expect a self as an argument
    @staticmethod
    def verify_reset_token(token):
        s=Serializer(app.config['SECRET_KEY'])
        #we wil again create a serializable object with this secreet key but we donot need to pass in the expires seconds this time
        #also need to apply a catch block in case token in invalid
        try:
            #this user id comes from the payload we passed in
            user_id=s.load(token)['user_id']
        except:
            return None
        #by this we will get the user with current id
        return User.query.get(user_id)
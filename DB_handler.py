import pyrebase
import json
import uuid

class DBModule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def login(self, uid, pwd):
        users = self.db.child("users").get().val()
        try:
            userinfo = users[uid]
            if userinfo["pwd"] == pwd:
                return True
            else:
                return False
        except:
            return False

    def signin_verification(self, uid):
        users = self.db.child("users").get().val()
        for i in users:
            if uid == i:
                return False
        
        return True

    def signin(self, _id_, pwd, name, email):
        information = { 
            "pwd": pwd, 
            "uname":name, 
            "email":email
        }
        if self.signin_verification(_id_):
            self.db.child("users").child(_id_).set(information)
            return True
        else:     
            return 
            
    def write_post(self, title, contents, uid):
        pid = str(uuid.uuid4())[:12]
        information = {
            "title":title,
            "contents":contents,
            "uid":uid
        }
        self.db.child("posts").child(pid).set(information)

    def post_list(self):
        post_lists = self.db.child("posts").get().val()
        return post_lists

    def post_detail(self, pid):
        post = self.db.child("posts").get().val()[pid]
        return post

    def get_user(self, uid):
        post_list = []
        users_post = self.db.child("posts").get().val()
        for post in users_post.items():
            if post[1]["uid"] == uid:
                post_list.append(post)
        return post_list
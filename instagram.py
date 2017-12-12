import random
import json
import requests
from bs4 import BeautifulSoup
import fake
import time

class Instagram():
    def __init__(self,username,password,proxy = False):
        self.username = username
        self.password = password
        self.useragent = random_ua()["User-Agent"]
        self.s = requests.Session()
        if not proxy:
            self.s_get = self.s.get("https://www.instagram.com/accounts/login/")
        else:
            while True:
               try:
                   self.proxy = proxy()
                   self.s.proxies = self.proxy
                   self.s_get = self.s.get("https://www.instagram.com/accounts/login/")
                   break
               except:
                   pass

    def login(self):
        post_url = "https://www.instagram.com/accounts/login/ajax/"
        form_data={"username":self.username,"password":self.password}
        self.s.headers.update({
            'UserAgent':self.useragent,
			'x-instagram-ajax':'1',
			'X-Requested-With': 'XMLHttpRequest',
			'origin': 'https://www.instagram.com',
			'ContentType' : 'application/x-www-form-urlencoded',
			'Connection': 'keep-alive',
			'Accept': '*/*',
			'Referer': 'https://www.instagram.com/accounts/login/',
			'authority': 'www.instagram.com',
			'Host' : 'www.instagram.com',
			'Accept-Language' : 'en-US;q=0.6,en;q=0.4',
			'Accept-Encoding' : 'gzip, deflate'
		})
        self.s.headers.update({'X-CSRFToken' : self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(post_url, data=form_data)
        try:
            r = json.loads(r.text)
            if r["authenticated"] == True:
                self.s_get = self.s.get("https://www.instagram.com/")
                # giriş yapınca csrftoken güncellendiği için bunuda güncelliyorum
            return r
        except:
            return r

    def logout(self):
        post_url = "https://www.instagram.com/accounts/logout/"
        form_data = {"csrfmiddlewaretoken":self.s_get.cookies.get_dict()['csrftoken']}
        self.s.headers.update({'X-CSRFToken' : self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.get(post_url,data=form_data)
        try:
            r = json.loads(r.text)
            return r
        except:
            return r

    def follow(self,follow_id):
        follow_url = "https://www.instagram.com/web/friendships/{}/follow/".format(follow_id)
        self.s.headers.update({'X-CSRFToken' : self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(follow_url)
        try:
            r = json.loads(r.text)
            return r
        except:
            return r

    def unfollow(self,unfollow_id):
        unfollow_url = "https://www.instagram.com/web/friendships/{}/unfollow/".format(unfollow_id)
        self.s.headers.update({'X-CSRFToken' : self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(unfollow_url)
        try:
            r = json.loads(r.text)
            return r
        except:
            return r

    def signup(self,first_name,email):
        signup_post = "https://www.instagram.com/accounts/web_create_ajax/"
        form_data={
            "email":email,
            "password":self.password,
            "username":self.username,
            "first_name":first_name,
            "seamless_login_enabled":"1"
            }
        self.s.headers.update({
            'UserAgent':self.useragent,
    		'x-instagram-ajax':'1',
    		'X-Requested-With': 'XMLHttpRequest',
    		'Host': 'https://www.instagram.com',
    		'ContentType' : 'application/x-www-form-urlencoded',
    		'Connection': 'keep-alive',
    		'Accept': '*/*',
    		'Referer': "https://www.instagram.com/",
    		'authority': 'www.instagram.com',
    		'Host' : 'www.instagram.com',
    		'Accept-Language' : 'en-US;q=0.6,en;q=0.4',
    		'Accept-Encoding' : 'gzip, deflate'
    	})
        self.s.headers.update({'X-CSRFToken' : self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(signup_post, data=form_data)
        try:
            r = json.loads(r.text)
            return r
        except:
            return r


def random_ua():
    explorer = ["chrome","opera","firefox","internetexplorer","safari"]
    ex = fake.ua["browsers"][explorer[random.randrange(5)]]
    useragent = ex[random.randrange(len(ex))]
    return {'User-Agent': useragent}

def proxy():
    json_ip = requests.get("https://freevpn.ninja/free-proxy/json").json()
    "https://gimmeproxy.com/api/getProxy" # proxy siteleri
    "https://getproxylist.com/"
    num = random.randrange(10000)
    json_num = json_ip[num]
    if json_num["type"] == "https":
        ip = "https://"+json_num["proxy"]
        return {"https":ip }
    elif json_num["type"] == "http":
        ip = "http://"+json_num["proxy"]
        return {"http":ip }

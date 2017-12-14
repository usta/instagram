import random
import json
import requests
from bs4 import BeautifulSoup
import fake
import time
import sys

class Instagram():
    def __init__(self, username, password, proxy = False):
        self.username = username
        self.password = password
        self.isloggedin = False
        self.useragent = self.random_ua()["User-Agent"]
        self.s = requests.Session()
        self.proxy = self.random_proxy() if proxy else {}
        self.s.proxies = self.proxy
        self.s_get = self.s.get("https://www.instagram.com/accounts/login/")

    def json_loads(self, req):
        r = {}
        try:
            r = json.loads(req.text)
        except Exception as e:
            print("An Error Occured! Details :\n",sys.exc_info())
        finally:
            self.s_get = self.s.get("https://www.instagram.com/")
            return r

    def login(self):
        self.s_get = self.s.get("https://www.instagram.com/accounts/login/")
        post_url = "https://www.instagram.com/accounts/login/ajax/"
        form_data={"username": self.username, "password": self.password}
        self.s.headers.update({
            'UserAgent': self.useragent,
			'x-instagram-ajax': '1',
			'X-Requested-With': 'XMLHttpRequest',
			'origin': 'https://www.instagram.com',
			'ContentType': 'application/x-www-form-urlencoded',
			'Connection': 'keep-alive',
			'Accept': '*/*',
			'Referer': 'https://www.instagram.com/accounts/login/',
			'authority': 'www.instagram.com',
			'Host' : 'www.instagram.com',
			'Accept-Language': 'en-US;q=0.6,en;q=0.4',
			'Accept-Encoding': 'gzip, deflate'
		})
        self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(post_url, data=form_data)
        self.isloggedin = True
        return self.json_loads(r)

    def logout(self):
        post_url = "https://www.instagram.com/accounts/logout/"
        r = self.s.get(post_url)
        self.isloggedin = False

    def follow(self, follow_id):
        if self.isloggedin:
            follow_url = "https://www.instagram.com/web/friendships/{}/follow/".format(follow_id)
            self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
            r = self.s.post(follow_url)
            return self.json_loads(r)
        else:
            print("You must login first")

    def unfollow(self, unfollow_id):
        if self.isloggedin:
            unfollow_url = "https://www.instagram.com/web/friendships/{}/unfollow/".format(unfollow_id)
            self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
            r = self.s.post(unfollow_url)
            return self.json_loads(r)
        else:
            print("You must login first")

    def signup(self, first_name, email):
        signup_post = "https://www.instagram.com/accounts/web_create_ajax/"
        form_data={
            "email": email,
            "password": self.password,
            "username": self.username,
            "first_name": first_name,
            "seamless_login_enabled": "1"
            }
        self.s.headers.update({
            'UserAgent': self.useragent,
    		'x-instagram-ajax': '1',
    		'X-Requested-With': 'XMLHttpRequest',
    		'Host': 'https://www.instagram.com',
    		'ContentType': 'application/x-www-form-urlencoded',
    		'Connection': 'keep-alive',
    		'Accept': '*/*',
    		'Referer': "https://www.instagram.com/",
    		'authority': 'www.instagram.com',
    		'Host' : 'www.instagram.com',
    		'Accept-Language': 'en-US;q=0.6,en;q=0.4',
    		'Accept-Encoding': 'gzip, deflate'
    	})
        self.s.headers.update({'X-CSRFToken': self.s_get.cookies.get_dict()['csrftoken']})
        r = self.s.post(signup_post, data=form_data)
        return self.json_loads(r)

    @staticmethod
    def random_ua():
        explorer = ["chrome", "opera", "firefox", "internetexplorer", "safari"]
        ex = fake.ua["browsers"][explorer[random.randrange(len(explorer))]]
        useragent = ex[random.randrange(len(ex))]
        return {'User-Agent': useragent}

    @staticmethod
    def random_proxy():
        json_data = requests.get("https://freevpn.ninja/free-proxy/json").json()
        # possible alternate proxies
        # "https://gimmeproxy.com/api/getProxy"
        # "https://getproxylist.com/"

        json_ip = []
        # We are just selecting https and http types
        for i in json_data:
            if i["type"] in ["http", "https"]:
                json_ip.append({"type": i["type"], "proxy": i["proxy"]})

        if len(json_ip) == 0: # If we dont have any http / https proxies
            return {}

        num = random.randrange(len(json_ip))
        json_proxy = json_ip[num]
        return {json_proxy["type"]: "{}://{}".format(json_proxy["type"], json_proxy["proxy"])}

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import random


def random_ua():
    ua = UserAgent()
    return {'User-Agent': ua.random}

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


class Instagram():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.s = requests.Session()
        self.s.headers.update({
            'UserAgent':random_ua()["User-Agent"],
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
        login_url = "https://www.instagram.com/accounts/login/"
        while True:
            try:
                self.s.proxies = proxy()
                s_get = self.s.get(login_url)
                break
            except:
                pass
        self.s.headers.update({'X-CSRFToken' : s_get.cookies.get_dict()['csrftoken']})
        self.soup=BeautifulSoup(s_get.content,"html.parser")
        self.post_url = "https://www.instagram.com/accounts/login/ajax/"

    def data(self):
        data={
        }
        data['username'] = self.username
        data['password'] = self.password
        return data

    def login(self,data):
        r = self.s.post(self.post_url, data=data)
        data = json.loads(r.text)
        try:
            if data['authenticated'] == True:
                return True,{"data":data,"kullanıcı adı":self.username,"şifre":self.password}
        except KeyError:
            pass
        return False,{"data":data}

def login_instagram(user,pass_):
    t = Instagram(user,pass_)
    data = t.data()
    login = t.login(data)
    return login

print(login_instagram("username","password"))

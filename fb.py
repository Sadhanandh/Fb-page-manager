from urllib import urlencode
import random
import urllib2
import json
from urlparse import parse_qs
import mdatabase

APP_ID = "541146969281888"
APP_SECRET = "b0ebd997a2ccda30d50c2a8650986595"
AUTH_SCOPE = ["offline_access","publish_stream","manage_pages"]
REDIRECT_URL_C = "http://gsample.pythonanywhere.com/fbcode"



state = str(random.randint(2000,4000))
furl = ('https://www.facebook.com/dialog/oauth?' +
        urlencode({'client_id':APP_ID,
        'redirect_uri':REDIRECT_URL_C,
        'response_type':'code',
        'state':state,
        'scope':','.join(AUTH_SCOPE)}))


def login():
    val = "<a href=" + furl +">Click To Login </a>"
    return val


def capture(CODE):
    aurl = ("https://graph.facebook.com/oauth/access_token?"+
    urlencode({'client_id':APP_ID,
        'redirect_uri':REDIRECT_URL_C,
		'client_secret':APP_SECRET,
		'code': CODE}))
    try:
        resp = urllib2.urlopen(aurl).read()
        try:
            resp = parse_qs(resp)
            ACCESS_TOKEN=resp["access_token"][0]
            S_token = ACCESS_TOKEN
            return S_token
        except urllib2.HTTPError:
            pass
    except AttributeError:
        pass


def super_capture(ACCESS_TOKEN):
    curl= ("https://graph.facebook.com/oauth/access_token?"+
			urlencode({"client_id": APP_ID ,
					   "client_secret" :  APP_SECRET,
					   "grant_type" : "fb_exchange_token",
					   "fb_exchange_token": ACCESS_TOKEN }))

    resp = None
    S_id = None
    S_name = None
    S_token = None
    try:
        resp = urllib2.urlopen(curl).read()
        try:
            resp = parse_qs(resp)
            ACCESS_TOKEN_P=resp["access_token"][0]
            S_token = ACCESS_TOKEN_P
        except urllib2.HTTPError:
            pass
    except AttributeError:
        pass

    nurl = ("https://graph.facebook.com/me?" +
			urlencode({"access_token" : ACCESS_TOKEN_P}))

    try:
        resp = urllib2.urlopen(nurl).read()
    except urllib2.HTTPError:
        pass
    try:
        obj = json.loads(resp)
        S_id = obj["id"]
        S_name = obj["name"]
    except :
        pass
    if (S_token != None and S_name !=None and S_id != None):
        print "done"
    mdatabase.super_capture(S_name,S_id,S_token)
    pageurl = "https://graph.facebook.com/%s/accounts?access_token=%s"%(S_id,S_token)
    res = urllib2.urlopen(pageurl).read()
    j = json.loads(res)
    optns = []
    for xs in j["data"]:
        optn = {}
        optn["name"] = xs["name"]
        optn["id"] = xs["id"]
        optns.append(optn)

    return S_name +","+ S_id,optns

def pageselected(PAGE,ID):
    return mdatabase.pageselected(PAGE,ID)

def getpageid(ID):
    ans = mdatabase.getpageid(ID)
    if len(ans)>0 and len(ans[0])==3:
        return ans[0][2]
    else:
        return None

def registerpage(atk,PAGE_ID):
    aurl = "https://graph.facebook.com/%s/tabs"%(PAGE_ID.strip())
    data = urlencode({'app_id':APP_ID,
        'access_token':atk})
    res = urllib2.urlopen(aurl,data)
    data = res.read()
    if data == 'true':
        return "Successful"
    else:
        return "Try again!"

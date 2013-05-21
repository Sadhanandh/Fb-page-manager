import json
import urllib2
import urllib

aa_token = "xxxx"
def getme(u_id,a_token=aa_token):
    url =  "https://graph.facebook.com/%s?access_token=%s"%(u_id,a_token)
    msg= "Error"
    from_id = url
    try:
        res = urllib2.urlopen(url)
        mydata= json.loads(res.read())
        msg = mydata['message']
        from_id = mydata['from']['id']
    except Exception:
        pass
    return from_id + " Said : "+ msg

def postme(msg,u_id,a_token=aa_token):
    indata = urllib.urlencode({'access_token' : a_token,'message' : msg})
    url = "https://graph.facebook.com/%s/comments"%(u_id)
    res = urllib2.urlopen(url,indata)
    mydata= json.loads(res.read())
    return mydata['id']


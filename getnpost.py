import json
import urllib2
import urllib
import mdatabase

aa_token = "xxxx"
def getme(u_id,a_token=aa_token):
    url =  "https://graph.facebook.com/%s?access_token=%s"%(u_id,a_token)
    msg= "Error"
    from_id = url
    try:
        res = urllib2.urlopen(url)
        mydata= json.loads(res.read())
        msg = mydata['message']
        from_id = mydata['from']['name']
    except Exception:
        pass
    return "<span id='username' >" + from_id + "</span> : <span id='message'>"+ msg+"</span>"

def postme(msg,u_id,a_token=aa_token,s_page=None):
    indata = urllib.urlencode({'access_token' : a_token,'message' : msg})
    url = "https://graph.facebook.com/%s/comments"%(u_id)
    res = urllib2.urlopen(url,indata)
    mydata= json.loads(res.read())
    m_id = mydata.get('id',"error")
    if m_id!='error':
        mdatabase.save("comment",m_id,"0",s_page) # TODO : 0 or int(time.time()) or get the time from fb api & convert it to epoch
    return m_id


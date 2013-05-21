import MySQLdb as mdb
import getnpost


SQL_SERVER = "mysql.server"
SQL_USER = "Gsample"
SQL_PASS = "databasepass"
SQL_DB = "Gsample$mydata"

def enter(i_data):
    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute('insert into facebook(name) values("%s")'%(i_data))
    cur.connection.commit();

def save(s_type,s_id,s_time):
    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute('insert into convo(utype,uid,utime) values("%s","%s","%s")'%(s_type,s_id,s_time))
    cur.connection.commit();

def delete(i_data):
    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute('delete from convo where uid="%s"'%(i_data))
    cur.connection.commit();

def getallposts():
    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute('select uid from convo where utype="post"')
    ans = cur.fetchall()
    cur.close()
    c.close()
    res = []
    if len(ans)>0:
        for x in ans:
            res.append(x[0])
    return res




def searchermsg(s_uid,s_utime='0',a_id=None):
    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute('select uid,utime from convo where utype="comment" and uid like "%s_%%" and utime > %s  order by utime asc'%(s_uid,s_utime) )
    ans = cur.fetchall()
    cur.close()
    c.close()
    time = '0'
    msga = []
    if len(ans)>0:
        for x in ans:
            msga.append(getnpost.getme(x[0].strip('"'),a_id))
            time = x[1]

        return {'ids':msga,'time':time,'found':len(msga)}
    else:
        return {'found':"None"}


def getpageid(ID):
    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute("select * from facebookaccess where id = '%s'" %(ID))
    ans = cur.fetchall()
    cur.close()
    c.close()
    return ans



def pageselected(PAGE,ID):
    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute("select access_token from facebookaccess where id=%s"%(ID))
    atk = cur.fetchall()
    atk = atk[0][0]
    pageurl = "https://graph.facebook.com/%s/accounts?access_token=%s"%(ID,atk)
    import urllib2
    import json
    res = urllib2.urlopen(pageurl).read()
    j = json.loads(res)
    mypage = {}
    for xs in j["data"]:
        if xs["id"]==PAGE:
            mypage["name"] = xs["name"]
            mypage["id"] = xs["id"]
            mypage["access_token"] = xs["access_token"]
    if mypage.has_key("access_token"):
        cur.execute('insert into facebookaccess(name,id,access_token) values("%s","%s","%s") on duplicate key update name="%s",access_token="%s"' %(mypage["name"],mypage["id"],mypage["access_token"],mypage["name"],mypage["access_token"]))
        cur.connection.commit();
    cur.close()
    c.close()
    if mypage.has_key("access_token"):
        return "You have been successfully authenticated! <br />  Your Page : %s is now accessible </br> Please note down your unique number which is to entered as your user id in the login page<br /> %s <br /><br />Remember this is only valid for 60 days.You need to re authorize this app within this 60 days."%(mypage["name"],mypage["id"])
    else:
        return "Error .Your request could not be completed"


def super_capture(S_name,S_id,S_token):

    c = mdb.connect(SQL_SERVER,SQL_USER,SQL_PASS,SQL_DB)
    cur = c.cursor()
    cur.execute('insert into facebookaccess(name,id,access_token) values("%s","%s","%s") on duplicate key update name="%s",access_token="%s"' %(S_name,S_id,S_token,S_name,S_token))
    cur.connection.commit();
    cur.execute("select * from facebookaccess")
    cur.close()
    c.close()


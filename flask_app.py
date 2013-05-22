

from flask import Flask,request,current_app,render_template,session
import json
import mdatabase
import getnpost
import fb

#callback support
def jsonp(func):
    callback = request.args.get('callback', False)
    if callback:
        data = json.dumps(func)
        content = str(callback) + '(' + data + ')'
        mimetype = 'application/javascript'
        return current_app.response_class(content, mimetype=mimetype)
    else:
        data = json.dumps(func)
        content = data
        mimetype = 'application/json'
        return current_app.response_class(content, mimetype=mimetype)






app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!'
@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/verify',methods=['GET','POST'])
def verify():
    output = ''
    if request.method == 'GET' and request.args.get('hub.mode')=='subscribe' and request.args.get('hub.verify_token')=='1234':
        output = request.args.get('hub.challenge')
    if request.method == 'POST':
        mydata = json.loads(request.data)
        mdatabase.enter(str(mydata))

        for val in xrange(len(mydata['entry'])):

            if mydata['entry'][val]['changes'][0]['value']['verb'] == 'add':
                if mydata['entry'][val]['changes'][0]['value']['item'] == 'status':
                    s_type =  'post'
                    s_id  = mydata['entry'][val]['changes'][0]['value']['post_id']
                elif mydata['entry'][val]['changes'][0]['value']['item'] == 'comment':
                    s_type =  'comment'
                    s_id =  mydata['entry'][val]['changes'][0]['value']['comment_id']
                elif mydata['entry'][val]['changes'][0]['value']['item'] == 'like':
                    pass
                    #no sender id
                s_time = mydata['entry'][val]['time']
                s_page = mydata['entry'][val]['id']
                mdatabase.save(s_type,s_id,s_time,s_page)
            elif mydata['entry'][val]['changes'][0]['value']['verb'] == 'remove':
                if mydata['entry'][val]['changes'][0]['value']['item'] == 'status':
                    s_id  = mydata['entry'][val]['changes'][0]['value']['post_id']
                elif mydata['entry'][val]['changes'][0]['value']['item'] == 'comment':
                    s_id =  mydata['entry'][val]['changes'][0]['value']['comment_id']
                mdatabase.delete(s_id)

        return str(mydata)
    return output


@app.route('/postme',methods=['GET','POST'])
def postme():
    puid = '330241307102935_330288167098249'
    #remove this asap //testing purpose only
    if request.method == 'GET':
        return getnpost.postme(request.args.get('msg'),request.args.get('puid',puid),session['aid'],session['PAGE'])
    elif request.method == 'POST':
        return getnpost.postme(request.form['msg'],request.form.get('puid',puid),session['aid'],session['PAGE'])

@app.route('/getme',methods=['GET','POST'])
def getme():
    return getnpost.getme(request.args.get('uid','None'),session['aid'])

@app.route('/getallposts')
def getallposts():
    return render_template("getallposts.html",pagelist=map(lambda x:x[x.find("_")+1:],mdatabase.getallposts(session['PAGE'])))

@app.route('/searchermsg',methods=['GET'])
def searchermsg():
    return jsonp(mdatabase.searchermsg(request.args.get('uid','none'),request.args.get('time','0'),session['aid']))

@app.route("/fbcode")
def fbcode():
    if request.args.has_key("code"):
        ur = fb.capture(request.args.get("code"))
        gr,pages = fb.super_capture(ur)
        un,ui = gr.split(",")
        return render_template("pagesform.html",pages = pages,ui = ui)
    else:
        return "Failed. You have not authenticated!"
@app.route("/fbselect",methods= ["post"])
def selected():
    return fb.pageselected(request.form["pages"],request.form["id"])

@app.route("/fblogin" )
def fblogin():
    return fb.login()


@app.route("/login")
def login():
    return """
    <form action="/loginpost" method="post">
    UserID:
    <input type="TEXT" name="id" value="" />
    <br />
    PAssword(dummy):
    <input type="PASSWORD" name="pass" value="" />
    <br />
    <input type="submit" class="submit" value="Ok" name="" />
</form>
"""

@app.route("/loginpost",methods=['GET','POST'])
def loginpost():
    aid = fb.getpageid(request.form['id'])
    if aid!=None:
        session['aid'] = aid
        session['PAGE'] = request.form['id']
        return "Successfully logged in"
    else :
        return "Not successful!"

@app.route("/comment_box")
def comment_box():
    return render_template("comment_box.html",pid=request.args.get('postid'))

@app.route("/registerpage")
def registerpage():
    return fb.registerpage(session['aid'],session['PAGE'])


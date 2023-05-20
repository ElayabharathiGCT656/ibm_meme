from flask import Flask,render_template,request,session
import requests
import ibm_db
import re
import json
import webbrowser

app=Flask(__name__)

app.secret_key = 'a'
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=lbw48262;PWD=wZlN3M0gQFzRuN2x;", "", "")
# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wxr23699;PWD=782wDyzZhf6ZArlW;", "", "")
print("connected")
@app.route('/')
def home():
    return render_template('Home.html')
@app.route('/About')
def about():
    return render_template('About.html')
@app.route('/meme',methods=['POST','GET'])
def meme():
    if request.method=="POST":
        keywords = request.form["key"]
        print (keywords)
        url = "https://humor-jokes-and-memes.p.rapidapi.com/memes/search"
        querystring={"keywords":keywords, "media-type": "image", "keywords-in-image": "false", "min-rating":"3","number":"2"}
        headers={
            "X-RapidAPI-Key":"73e9df854cmsh6dbcd86fce82b33p1919f9jsn75aeea457c41",
            'X-RapidAPI-Host': 'humor-jokes-and-memes.p.rapidapi.com'
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        output = json.loads(response.text)
        print (output)
        op1 = output['memes'][0]['url']
        webbrowser.open(op1)
        op2 = output['memes'][1]['url']
        webbrowser.open(op2)
        return render_template('Meme.html', outputl=op1, output2=op2)
    return render_template('Meme.html')  
@app.route("/reg",methods=['POST','GET'])
def signup():
    msg=''
    if request.method=='POST':
        print("req gone")
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        sql="SELECT * FROM REGISTER WHERE NAME=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            print("Account already exits")
            return render_template('Login.html',error=True)
        else:
            insert_sql="INSERT INTO REGISTER VALUES (?,?,?)"
            second_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(second_stmt,1,name)
            ibm_db.bind_param(second_stmt,2,email)
            ibm_db.bind_param(second_stmt,3,password)
            ibm_db.execute(second_stmt)
            msg="You have successfully registered"
            return render_template("Login.html",msg=msg)
    return render_template("Register.html",msg=msg)

@app.route("/log",methods=['POST','GET'])
def login1():
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        sql="SELECT * FROM REGISTER WHERE EMAIL=? AND PASSWORD=? "
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            print("logged in successfully!")
            session['Logged']=True
            session['Id']=account['EMAIL']
            session['email']=account['EMAIL']
            return render_template('Meme.html')
        else:
            msg="Incorrect Email/Password"
            return render_template('Login.html',msg=msg)
    else:
        return render_template('Login.html')  
if __name__=="__main__":
    app.run(debug=True)  

from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı gormek için giriş yapın","danger")
            return redirect(url_for("index"))
    return decorated_function

class RegisterForm(Form):
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Hacettepe maili ile giriş yapın")])
    

app = Flask(__name__)
app.secret_key = "kgo"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "kgo"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/",methods = ["GET","POST"])
def index():
    form = RegisterForm(request.form)
    
    if request.method == "POST" and form.validate():
        email = form.email.data
        
        cursor = mysql.connection.cursor()
        
        sorgu = "Insert into users(email) VALUES(%s)"
        
        sorgu1 = "Select * from users where email = %s"
        
        if cursor.execute(sorgu1,(email,)): #email varsa giris
            data = cursor.fetchone()
            voted = data["voted"]
            if voted == 1:
                cursor.close()
                return redirect(url_for("thanks"))
            else:
                cursor.close()
                flash("Başarıyla Giriş Yapıldı","success")
                
                session["logged_in"] = True
                session["email"] = email
                return redirect(url_for("vote"))
        else:                               #email yoksa giris
            if email[-17:] == "@hacettepe.edu.tr":
                cursor.execute(sorgu,(email,))
                mysql.connection.commit()
            
                cursor.close()
            
                flash("Başarıyla Giriş Yapıldı","success")
                
                session["logged_in"] = True
                session["email"] = email
                return redirect(url_for("vote"))
            else:
                flash("Lütfen Hacettepe Maili ile Giriş Yapın","danger")
                return redirect(url_for("index"))
    else: 
        return render_template("index.html",form = form)

@app.route("/vote",methods = ["GET","POST"])
@login_required
def vote():
    if request.method == "POST":
        """
        q1 = request.form["q1"]
        q2 = request.form["q2"]
        q3 = request.form["q3"]
        q4 = request.form["q4"]
        q5 = request.form["q5"]
        q6 = request.form["q6"]
        q7 = request.form["q7"]
        q8 = request.form["q8"]
        q9 = request.form["q9"]
        q10 = request.form["q10"]
        q12 = request.form["q12"]
        q13 = request.form["q13"]
        q14 = request.form["q14"]
        q15 = request.form["q15"]
        q16 = request.form["q16"]
        q17 = request.form["q17"]
        q18 = request.form["q18"]
        q19 = request.form["q19"]
        q20 = request.form["q20"]
        q21 = request.form["q21"]
        q22 = request.form["q22"]
        q24 = request.form["q24"]
        q26 = request.form["q26"]
        q27 = request.form["q27"]
        q28 = request.form["q28"]
        q29 = request.form["q29"]
        q30 = request.form["q30"]
        q31 = request.form["q31"]
        q32 = request.form["q32"]
        q33 = request.form["q33"]
        q34 = request.form["q34"]
        q35 = request.form["q35"]
        q36 = request.form["q36"]
        q37 = request.form["q37"]
        q38 = request.form["q38"]
        q39 = request.form["q39"]
        q40 = request.form["q40"]
        q41 = request.form["q41"]
        q42 = request.form["q42"]
        q43 = request.form["q43"]
        q44 = request.form["q44"]
        q45 = request.form["q45"]
        q46 = request.form["q46"]
        q47 = request.form["q47"]
        q48 = request.form["q48"]
        q49 = request.form["q49"]
        
        
        
        list = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q24,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41,q42,q43,q44,q45,q46,q47,q48,q49]
        
        cursor = mysql.connection.cursor()
        
        sorgu = "Select * from celebs where name = %s"
        
        sorgu1 = "Update celebs set vote = vote + 1 where name = %s"
        
        sorgu2 = "Update users set voted = 1 where email = %s"
        
        for i in list:
            if cursor.execute(sorgu,(i,)):
                cursor.execute(sorgu1,(i,))
                mysql.connection.commit()
        
        cursor.execute(sorgu2,(session["email"],))
        mysql.connection.commit()
        cursor.close() 
        """
        cursor = mysql.connection.cursor()
        sorgu2 = "Update users set voted = 1 where email = %s"
        cursor.execute(sorgu2,(session["email"],))
        mysql.connection.commit()
        cursor.close()
        session.clear()           
        return redirect(url_for("thanks"))
    return render_template("vote.html")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

if __name__ == "__main__":
    app.run(debug=True)
    
    

  

    

    

    

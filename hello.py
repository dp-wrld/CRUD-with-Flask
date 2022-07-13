from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    Contact = db.Column(db.String())
    
    def __init__(self, Name, Contact):
        self.Name = Name
        self.Contact = Contact


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def home():
    data = Result.query.all()
    return render_template("hello.html",datas=data)

@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        uname=request.form['uname']
        contact=request.form['contact']
        data = Result(uname, contact)
        db.session.add(data)
        db.session.commit()
        flash('User Added','success')
        return redirect(url_for("home"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:uid>",methods=['POST','GET'])
def edit_user(uid):
    if request.method=='POST':
        newname=request.form['uname']
        newcontact=request.form['contact']
        editData = Result.query.get(uid)

        editData.Name = newname
        editData.Contact = newcontact
        db.session.commit()
        flash('User Updated','success')
        return redirect(url_for("home"))
    data = Result.query.get(uid)
    
    return render_template("edit_user.html",datas=data)
    
@app.route("/delete_user/<string:uid>",methods=['GET'])
def delete_user(uid):
    delData = Result.query.filter_by(id=uid).first()
    db.session.delete(delData)
    db.session.commit()
    flash('User Deleted','warning')
    return redirect(url_for("home"))
    
if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)
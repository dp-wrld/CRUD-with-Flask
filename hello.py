from io import BytesIO
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

  
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/New_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate()

def create_app():
    db.init_app(app)
    migrate.init_app(app, db)

    return app

class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    Bday = db.Column(db.Date())
    Gender = db.Column(db.String(20))
    Position = db.Column(db.String())
    Age = db.Column(db.Integer())
    Hobby = db.Column(db.String())
    Image = db.Column(db.String(), nullable = True)
    Address = db.Column(db.String())
    
    def __init__(self, Name, Bday, Gender, Position, Age, Hobby, Image, Address):
        self.Name = Name
        self.Bday = Bday
        self.Gender = Gender
        self.Position = Position
        self.Age = Age
        self.Hobby = Hobby
        self.Image = Image
        self.Address = Address


@app.before_first_request
def create_tables():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    data = Result.query.order_by(Result.id)
    # print(type(data))
    return render_template("hello.html",data = data)


@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method=='POST':
        uname=request.form['uname']
        bday = request.form['bday']
        gender = request.form['gender']
        possition=request.form['position']
        age = request.form['age']
        hobby=request.form.getlist('hobby')
        hobby = (",").join(hobby)
        image = request.files['image']
        address=request.form['address']

        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                    
            data = Result(Name=uname,Bday=bday, Gender=gender, Position= possition, Age= age, Hobby= hobby, Image= filename, Address= address)
            db.session.add(data)
            db.session.commit()
        flash('User Added','success')
        return redirect(url_for("home"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:uid>",methods=['POST','GET'])
def edit_user(uid):
    if request.method=='POST':
        uname=request.form['uname']
        bday = request.form['bday']
        gender = request.form['gender']
        possition=request.form['position']
        age = request.form['age']
        hobby=request.form.getlist('hobby')
        image = request.files['image']
        address=request.form['address']

        editData = Result.query.get(uid)

        editData.Name = uname
        editData.Bday = bday
        editData.Gender = gender
        editData.Position = possition
        editData.Age = age
        editData.Hobby = hobby
        editData.Image = image
        editData.Address = address
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
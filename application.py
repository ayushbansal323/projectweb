import os
import requests
from flask import Flask, session ,render_template,request, redirect, url_for , escape
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = Flask.secret_key

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#   raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://nddktgugfpzndc:c3a23bf1d6742e7b546cae46cd868bc80aa8026505f02b840ed029c59688fe92@ec2-75-101-142-91.compute-1.amazonaws.com:5432/d8kjqb76sv2nrq")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/",methods=["GET"])
def index():
	if 'user_id' in session:
	    return redirect(url_for('home'), code= 307)
	return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route("/signup",methods=["GET", "POST"])
def signup():
    note=""
    notetype=""
    if request.method == "POST":
    	username = request.form.get("username")
    	if db.execute("SELECT username FROM register WHERE username=:username" , {"username":username}).rowcount != 0:	
    		note="The username already exists"
    		notetype="danger"
    		return render_template("register.html",note=note,notetype=notetype)	
    	password1 = request.form.get("password1")
    	password2 = request.form.get("password2")
    	if password1 != password2:
    		note="Password does not match"
    		notetype="danger"
    		return render_template("register.html",note=note,notetype=notetype)
    	if len(password1) < 8:
    		note="Password length should be atleast of 8 character"
    		notetype="warning"
    		return render_template("register.html",note=note,notetype=notetype)
    	db.execute("INSERT INTO register(username,password) VALUES (:username ,:password)",
    	{"username": username, "password":password1})
    	db.commit()
    	note="Account created please login to continue"
    	notetype="success"
    return render_template("register.html",note=note,notetype=notetype)

@app.route("/",methods=["POST"])
def login():
	username = request.form.get("username")
	password = request.form.get("password")
	if db.execute("SELECT * FROM register WHERE username=:username" , {"username":username}).rowcount == 0:	
		note="The username does not exist"
		notetype="danger"
		return render_template("index.html",note=note,notetype=notetype)
	register=db.execute("SELECT * FROM register WHERE username=:username" , {"username":username}).first()
	if register.username!=username or register.password!=password:	
		note="The username or password does not match"
		notetype="danger"
		return render_template("index.html",note=note,notetype=notetype)
	session['user_id'] = register.id	
	return redirect(url_for('home'), code=307)

@app.route("/home",methods=["POST","GET"])
def home():
    if 'user_id' in session:
        books=db.execute("SELECT * FROM books WHERE id>:start and id<=:end",{"start":0, "end":60}).fetchall()
        return render_template("home.html",books=books,count_id=0)
    return redirect(url_for('index'))

@app.route("/home/<int:post_id>",methods=["POST","GET"])
def homeid(post_id):
    if 'user_id' in session:
        books=db.execute("SELECT * FROM books WHERE id>:start and id<=:end",{"start":post_id*60, "end":(post_id+1)*60}).fetchall()
        return render_template("home.html",books=books,count_id=post_id)
    return redirect(url_for('index'))

@app.route("/book/<string:book_id>",methods=["POST","GET"])
def book(book_id):
    if 'user_id' in session:
        book=db.execute("SELECT * FROM books WHERE  isbn=:book_id",{"book_id":book_id}).first()
        reviews=db.execute("SELECT username,review,rating FROM register LEFT JOIN reviews ON reviews.register_id = register.id where book_id=:book_id;",{"book_id":book.id}).fetchall()
        goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ytbfU6ieOcUxjN52ynvLxA", "isbns": book_id})
        goodread=goodreads.json()
        goodreadrating=goodread['books']
        return render_template("book.html",book=book,reviews=reviews,goodreads=goodread,goodreadrating=float(goodreadrating[0]['average_rating']))
    return redirect(url_for('index'))
    
@app.route("/search",methods=["POST","GET"])
def searchid():
    if 'user_id' in session:
    	searchtype =request.form.get("selector")
    	search = request.form.get("search")
    	books=[]
    	if searchtype == "year":
    		books=db.execute("SELECT * FROM books WHERE year = :search",{"search":search}).fetchall()
    	elif searchtype == "isbn":
    		search = '%'+search+'%'
    		books=db.execute("SELECT * FROM books WHERE isbn LIKE :search",{"search":search}).fetchall()
    	elif searchtype == "author":
    		search = '%'+search+'%'
    		books=db.execute("SELECT * FROM books WHERE author LIKE :search",{"search":search}).fetchall()
    	elif searchtype == "title":
    		search = '%'+search+'%'
    		books=db.execute("SELECT * FROM books WHERE title LIKE :search",{"search":search}).fetchall()
    	return render_template("search.html",books=books,sel=searchtype,sea=search)
    return redirect(url_for('index'))
    
@app.route("/review/<string:book_id>",methods=["POST","GET"])
def addreview(book_id):
    if 'user_id' in session:
    	bookid=db.execute("SELECT * FROM books WHERE isbn = :book_id",{"book_id":book_id}).first()
    	review=request.form.get("review")
    	rating=request.form.get("rating")
    	db.execute("INSERT INTO reviews(register_id,book_id,review,rating) values(:register_id,:bookid,:review,:rating);",{"register_id": session['user_id'], "bookid":bookid.id , "review":review , "rating":rating})
    	db.commit()
    	return redirect(url_for('book',book_id=book_id))
    return redirect(url_for('index'))
	


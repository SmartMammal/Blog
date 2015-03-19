"""
Views.py:
* Simple views designed to see all of th posts
"""

from flask import render_template

from blog import app
from database import session
from models import Post

"""
# OLD: Display all posts
@app.route("/")
def posts():
    posts = session.query(Post) #Query of Post objects
    posts = posts.order_by(Post.datetime.desc()) # Order by datatime column w/ most recent posts first
    posts = posts.all() #Get all posts
    return render_template("posts.html",
        posts=posts
    )
"""

# NEW: Display all posts w/ pagination
@app.route("/")
@app.route("/page/<int:page>") #Designed to take you to specific page of content
def posts(page=1, paginate_by=10): #Page is page number, paginate by is # items per page
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count() #Use count method, get # items of Post query obect

    start = page_index * paginate_by #Calc the start item you should see
    end = start + paginate_by #calc last item you should see

    total_pages = (count - 1) / paginate_by + 1 #Get total # pages of content
    has_next = page_index < total_pages - 1 #Is there a page after current page
    has_prev = page_index > 0 #Is there a page before current page

    posts = session.query(Post) #Query of Post objects
    posts = posts.order_by(Post.datetime.desc()) #Order by datatime column w/ most recent posts first
    posts = posts[start:end] #Get posts from start to end -- for a given page
    
    # Pass all of these points into the template
    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/post/<int:post_id>", methods=["GET"])
def get_single_post(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    total_posts = session.query(Post).count()

    return render_template("single_post.html", post=post)  

from flask.ext.login import login_required #imports the login_required decorator

#Adds new post
#login_required decorator from Flask-Login used to prevent unauthorized users from adding posts
#Use get parameter... specifies that the route will only be used for GET requests to th page
@app.route("/post/add", methods=["GET"]) 
#@login_required
def add_post_get():
    return render_template("add_post.html")

#Adds a new route to take form data and create a new post; similar to add_post_get above but this only accepts POST requests
import mistune #This is a Markdown parser -- preprocesses the content field
from flask import request, redirect, url_for
from flask.ext.login import current_user #as part of login and re author in user model

@app.route("/post/add", methods=["POST"])
#@login_required
def add_post_post():
    #Use Flask's request.form dictionary to access the data submitted with form and assign it to the correct fields in the post
    post = Post(
        title=request.form["title"], 
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))
  
#Edits old post
#Use get parameter... specifies that the route will only be used for GET requests to th page
@app.route("/post/<int:post_id>/edit", methods=["GET"]) 
def edit_post(post_id):
    post = session.query(Post)
    post = post.get(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_post_post(post_id):
    # Get the post for the current post ID
    #post = session.query(Post)
    #post = post.get(post_id)
    
    title = request.form["title"]
    content = request.form["content"]
    
    #Update: New session > Lookup the current post_id > update it with the title and content
    session.query(Post).filter(Post.id == post_id).update({"title":title, "content":content} )
    session.commit()
    return redirect(url_for("posts"))

#To delete a post
@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    #post = session.query(Post)
    #post = post.get(post_id)
    session.query(Post).filter(Post.id == post_id).delete()
    session.commit()
    return redirect(url_for("posts"))

#To call the login view
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from .models import User

# Post method for /login
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"] # Read the email entered
    password = request.form["password"] #and read the password entered
    user = session.query(User).filter_by(email=email).first() #query to find the user object with the matching email address
    if not user or not check_password_hash(user.password, password): #check that the user exists using Wekzeug's check_password_hash to compare entered password to the stored hash
        flash("Incorrect username or password", "danger") #if incorrect use flash function to store a message which you can see when you render the next page
        return redirect(url_for("login_get")) #redirect the user back to the login page

    login_user(user) #if the user username & password are correct then call login_user to send a cookie (small chunk of data) to the user's browser which is used to identify the user
    return redirect(request.args.get('next') or url_for("posts")) #when user is logged in, redirect to post page; if there is next param in the URL query string, then redirect to that address

#Need a Logout Functionality
from flask.ext.login import logout_user

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for("posts"))
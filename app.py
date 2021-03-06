import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# creates our Flask app
app = Flask(__name__)
# Database setup

ENV = 'prod'

# tells our Flask app where our db is stored
# path to where our db is stored
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///posts.db') 
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uxkxqhuemkxskl:575935b2d06e4dd4479479163c0aca91f0715d7983f9915a463fd36de7ae9a29@ec2-18-210-214-86.compute-1.amazonaws.com:5432/d6j3gfi4nhrsak'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# link our Flask app to the db
db = SQLAlchemy(app)

# create Model for our Blog Post - designing the db Model here
class BlogPost(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # prints out when we create a Blog Post
    def __repr__(self):
        return 'Blog post ' + str(self.id)


#Create dummy posts - mimics a database
# all_posts = [
#     {
#         'title': 'Post 1',
#         'content': 'Content of Post1: Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
#         'author': 'Gail Deadwyler'
#     },
#     {
#         'title': 'Post 2',
#         'content': 'Content of Post2: Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
#     },

# ]
#create an SQLlite test db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#initialize db
# db = SQLAlchemy(app)

# create our Model for the db - columns
# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r' % self.id



# set up base route
@app.route('/')
def index():
    return render_template('index.html')
    #return '<h1>Home Page</h1>'

# route to retrieve form data and add to db
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    # take form data and save to db
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post) # only adds data in current session
        db.session.commit() # permanently saved to db
        return redirect('/posts')
    else: # show all the Blog Posts
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

# delete data from db based on unique post id
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post) # deletes data in current session
    db.session.commit() # permanently saved to db
    return redirect('/posts')

# allows user to edit posts based on unique post id
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

#
@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post) # only adds data in current session
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')





# if this page is the main page, run it
if __name__ == '__main__':
    app.run(debug=True)
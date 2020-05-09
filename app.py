from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

app = Flask(__name__)
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

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/onlyget', methods=['GET','POST'])
def only_get():
    return "You only get this webpage"


# if this page is the main page, run it
if __name__ == '__main__':
    app.run(debug=True)
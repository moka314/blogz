from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:cheese@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='y337kGcys&zP3B'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body=body


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.args.get('id'):
        q = request.args.get('id')
        post = Blog.query.filter_by(id=q).first()
        template = jinja_env.get_template('individual.html')
        return template.render(post=post)
    posts= Blog.query.all()
    return render_template('blog.html', posts=posts)



@app.route('/newpost', methods=['POST'])
def newpost():
    if request.method =='POST':
        title = request.form['title']
        body = request.form['body']
        title_error = ''
        body_error = ''

        if len(title)<1:
            title_error = 'Please enter a title for Your Blog'
        if len(body)<1:
            body_error = 'Please enter a Blog Post'  

        if not title_error and not body_error:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            q = new_post.id
            post = Blog.query.filter_by(id=q).first()
            template = jinja_env.get_template('individual.html')
            return template.render(post=post)
        else:
            return render_template('newpost.html',title_error=title_error, body_error=body_error,title=title,body=body)

@app.route('/newpost', methods=['GET'])
def newpost_get():    
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
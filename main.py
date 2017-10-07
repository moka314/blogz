from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:cheese@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body=body


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
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
            return redirect('/blog')
        else:
            return render_template('newpost.html',title_error=title_error, body_error=body_error,title=title,body=body)
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
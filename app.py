from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    intro = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' %self.id


@app.route('/')
@app.route('/home')
def home():
    return render_template("shop.html")


@app.route('/about')
def about():
    return render_template("discount.html")


@app.route('/posts')
def posts(id):
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html",articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html",article=article)


@app.route('/posts/<int:id>/delete',methods=['POST','GET'])
def posts_delete(id):
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
       # article = Article.query.get_or_404(id)
        try:
            db.session.delete(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении произошла ошибка"
    else:
        article = Article.query.get_or_404(id)
        return render_template("posts.html", article=article)


@app.route('/catalog')
def catalog():
    return render_template("catalog.html")


@app.route('/create_article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title,intro=intro,text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении произошла ошибка"
    else:
        return render_template("create_article.html")


@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    article=Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении произошла ошибка"
    else:
        article = Article.query.get(id)
        return render_template("create_article.html", article=article)





#@app.route('/shop')
#def shop():
   # return render_template('shop.html', Hello= 'Go in the our shop')


if __name__=='__main__':
    app.run(debud=True)

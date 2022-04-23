from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Body")
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    all_posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=all_posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(index)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["POST", "GET"])
def new_post():
    greeting1 = "New Post"
    greeting2 = "You're going to make a great blog post!"
    form = CreatePostForm()
    if form.validate_on_submit():
        to_be_added = BlogPost(title=form.title.data, date=str(date.today()), subtitle=form.subtitle.data,
                               body=form.body.data, author=form.author.data, img_url=form.img_url.data)
        db.session.add(to_be_added)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form,greeting1 = greeting1,greeting2=greeting2)


@app.route("/edit-post",methods = ["POST","GET"])
def edit_post():
    blog_id = request.args.get("post_id")
    if request.method == "GET":
        greeting1 = "Edit Post"
        greeting2 = "Editing Mode Enabled"
        post = BlogPost.query.filter_by(id=blog_id).first()
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body)
        return render_template("make-post.html", form=edit_form,greeting1 = greeting1,greeting2=greeting2)
    else:
        blog_to_update = BlogPost.query.filter_by(id=blog_id).first()
        blog_to_update.title = request.form.get("title")
        blog_to_update.subtitle = request.form.get("subtitle")
        blog_to_update.img_url = request.form.get("img_url")
        blog_to_update.author = request.form.get("author")
        blog_to_update.body = request.form.get("body")
        db.session.commit()
        return redirect(url_for("get_all_posts"))


@app.route("/delete-post",methods = ["POST","GET"])
def delete_post():
    blog_id = request.args.get("post_id")
    blog_selected = BlogPost.query.get(blog_id)
    db.session.delete(blog_selected)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)

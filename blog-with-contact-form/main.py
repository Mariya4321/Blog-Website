from flask import Flask, render_template, request
import requests
import smtplib
import os

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/33fe40530a76ae363c6a").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        with smtplib.SMTP(os.environ["SMTP_ADDS"]) as connection:
            connection.starttls()
            connection.login(os.environ["MY_EMAIL"], os.environ["PASSWORD"])
            connection.sendmail(
                from_addr=os.environ["MY_EMAIL"],
                to_addrs=os.environ["SEND_EMAIL"],
                msg=f"Subject: Contact \n\nName = {name}\nEmail = {email}\nPhone no. = {phone}\nMessage = {message}"
            )
        return render_template('contact.html', msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

from flask import Flask, render_template, redirect, request
import string
import random
import db

app = Flask(__name__)

shortened_urls = {}

def gen_short_url():
    char = string.ascii_letters + string.digits
    short_url = "".join(random.choices(char, k=7))
    return short_url

@app.route("/", methods=['GET', 'POST'])
def shorten_url():
    if request.method == "POST":
        long_url = request.form['original_url']
        short_url = gen_short_url()

        while db.url_exist(short_url):
            short_url = gen_short_url()

        db.save_url(short_url, long_url)
        full_url = f"{request.url_root}{short_url}"
        return render_template("index.html", short_url=full_url)
    return render_template("index.html")

@app.route("/<short_url>")
def redirection(short_url):
    long_url = db.get_url(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
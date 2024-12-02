from flask import request, redirect, url_for, render_template, flash, session
from web_root import app

# Generate root contents http://xxx.xxx.xxx.xxx:5000
@app.route('/')
def show_articles():
    # Load index.html and Return contents
    return render_template('articles/index.html')
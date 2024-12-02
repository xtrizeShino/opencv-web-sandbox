from flask import request, redirect, url_for, render_template, flash, session
from web_root import app

@app.route('/')
def show_articles():
    return render_template('articles/index.html')
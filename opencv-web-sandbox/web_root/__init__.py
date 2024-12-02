from flask import Flask

app = Flask(__name__)
app.config.from_object('web_root.config')

from web_root.views import views, streams
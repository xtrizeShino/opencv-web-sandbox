from flask import Flask

# Generate Flask instance
app = Flask(__name__)
# Load config.py
app.config.from_object('web_root.config')
# Define contents as index.html(views) and streams/stream(streams.py)
from web_root.views import views, streams
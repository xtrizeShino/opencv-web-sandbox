from web_root import app

# entry point to run Flask class
# -->> Flask class is generated in __init__.py
if __name__ == '__main__':
    # Start Web Server
    app.run(host="0.0.0.0")

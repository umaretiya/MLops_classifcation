from flask import Flask

"https://github.com/umaretiya/MLops_classifcation"

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to Machine Learning Classification Automation Projects</h1>"

if __name__ == "__main__":
    app.run()
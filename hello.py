from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager

app = Flask(__name__)
bootstrap = Bootstrap(app)
manger=Manager(app)

@app.route("/")
def hello():
	return render_template("base.html")

if __name__=="__main__":
	manger.run()
	
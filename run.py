from flask import Flask, jsonify, render_template, request, Blueprint
import chartkick
import recite
app = Flask(__name__)
ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

@app.route('/')
@app.route('/index')
def index():
	data=recite.getWordCount()
	# data=[['2017-07-01', 20]]
	print(data)
	return render_template('data.html', data=data)
if __name__ == "__main__":
	app.run(debug=True)
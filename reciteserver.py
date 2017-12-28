# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, Blueprint
from recite import botRecite as br
from recite import getWordlist as getWordlist
from recite import getWordCount
from recite import addToReview
from recite import sciReview
from recite import sciReviewUpdate
from recite import sciReviewData
from recite import percent_review
import chartkick
import sqlite3
app = Flask(__name__)
ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")
@app.route('/hello/')
def hello():
	word = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
	return render_template('hello.html', data=word)
# @app.route('/recite/')
# def recite(number=None):
# 	return br()
# @app.route('/_add_numbers')
# def add_numbers():
#     a = request.args.get('a', 0, type=int)
#     b = request.args.get('b', 0, type=int)
#     return jsonify(result=a + b)
@app.route('/sciReviewUpdate')
def update():
	word=request.args.get('sciword',0,type=str)
	sciReviewUpdate(word)
	return jsonify(scimsg='+1s')

@app.route('/sciReview')
def review():
	number = request.args.get('scinumber',0,type=int)
	reviewlist = sciReview(number)
	return jsonify(reviewlist=reviewlist)

@app.route('/addToReview')
def addToReBook():
	word = request.args.get('word','')
	trans= request.args.get('trans','')
	print(word)
	if(str(word)=='' and str(trans)==''):
		return jsonify(msg='你确定你没有在调戏我吗？')
	else: 
		data=[word,trans]
		# print(data)
		addToReview(data)
		return jsonify(msg='成功添加至生词本')
@app.route('/recite')
def recite():
	number = request.args.get('number',0,type=int)
	return jsonify(wordlist=getWordlist(number))
# @app.route('/showdata')
# def showdata():
# 	reviewlist = sciReviewData()
# 	datalist=[ [x[1], x[4]] for x in reviewlist ]
# 	return jsonify(data=datalist)
@app.route('/')
@app.route('/index')
def index():
	reviewlist = sciReviewData()
	datalist=[ [ x[3], x[4]] for x in reviewlist ]
	return render_template('reciteindex.html', datalist=datalist)

@app.route('/getdata')
def getdata():
	data = getWordCount()
	per = percent_review()
	piedata=[['Reviewing', str(per)], ['Unreview', str(100-per)]]
	return render_template('data.html', data=data,piedata=piedata)

if __name__ == '__main__':
    app.run(debug=True)
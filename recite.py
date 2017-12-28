# -*- coding: utf-8 -*-
import argparse
import math
import os
import sqlite3
import sys
from random import shuffle
from sys import platform
import csv
from datetime import datetime, date
parser = argparse.ArgumentParser(description='Word recite tool')
parser.add_argument('-qr', '--quickrecite', help='set quick recite mode and wordnumber')
parser.add_argument('-rv', '--reviewwords', help='review words with Ebbinghaus curv')
args = parser.parse_args()
def time_passed(value):
    now = datetime.now()
    past = now - value
    day= past.days*24
    minus= past.seconds/60
    return minus/60+day

def clearScr():
    if platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")
def getForget(date):
	hourstr=str(time_passed(datetime.strptime(date,'%Y-%m-%d %H:%M:%S')))
	hours=float(hourstr)
	#艾宾浩斯记忆曲线近似公式
	forget=round(1-0.56*pow(hours,0.06),2)
	return forget

def percent_review():
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	rem=[]
	for row in c.execute( "select * from reviewwords" ):
		rem.append(list(row))
	l=float(len(rem))
	percent=l / 5518.0
	print(l)
	print(round(percent*100,2))
	return round(percent*100,2)
#wechat
def botRecite():
	wordslist=[]
	with open('wordbook.csv') as csvfile:
		d = csv.reader( csvfile )
		rows = [row for row in d]
		shuffle(rows)
		wordslist = [ (x[0], x[1]) for x in rows[:1] ]
	value=wordslist[0][0]+'\n'+wordslist[0][1]
	try:
		unicode(value, "ascii")
	except UnicodeError:
		value = unicode(value, "utf-8")
	else:
		pass
	return value

def sciReviewUpdate(word):
	w=str(word)
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	timenow=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	param=(timenow,w)
	# print(w)
	# print("word:"+word)
	c.execute('''UPDATE reviewwords SET date=? WHERE en=?''',param)
	conn.commit()

def sciReviewData():
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	rem=[]
	flag=0
	word=[]
	for row in c.execute( 'select * from reviewwords'):
	    rem.append(list(row))

	l=len(rem)
	for i in range(0, l):
		if(rem[i][3]!=None):
			forget=getForget(rem[i][3])
			rem[i].append(forget)
		else:
			timenow=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			forget1=getForget(timenow)
			rem[i].append(forget1)
	rem=sorted(rem, key=lambda rem : rem[4])
	for i in range(0, l):
		rem[i][1]=rem[i][1].encode('raw_unicode_escape')
		rem[i][3]=rem[i][3].encode('raw_unicode_escape')
	# print(rem)
	return rem
def sciReview(number):
	n=int(number)
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	rem=[]
	flag=0
	word=[]
	for row in c.execute( "select * from reviewwords" ):
	    rem.append(list(row))
	l=len(rem)
	for i in range(0, l):
			if(rem[i][3]!=None):
				forget=getForget(rem[i][3])
				rem[i].append(forget)
			else:
				# print(rem[i][3])
				id=rem[i][0]
				timenow=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				param=(timenow,id)
				c.execute('''UPDATE reviewwords SET date=? WHERE id=?''',param)
				conn.commit()
				forget1=getForget(timenow)
				# print(timenow)
				rem[i].append(forget1)
	rem=sorted(rem, key=lambda rem : rem[4])
	word = [ [x[1], x[2], x[4]]for x in rem[:n] ]
	return word

def addToReview(words):
	word=words[0]
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	print(word)
	rem=[]
	for row in c.execute( "select * from reviewwords where en = ?",(word,) ):
	    rem.append(list(row))
	if(rem==[]):
		c.executemany( "insert into `reviewwords` (en,cn) values(?, ?)", (words,) )
		conn.commit()

def getWordCount():
	data_row=[]
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	for row in c.execute( "select date,num from 'recitecount' "):
		row=list(row)
		row[0]=row[0].encode('raw_unicode_escape')
		data_row.append(row)
	return data_row

def getWordlist(number):
	wordslist=[]
	n=int(number)
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	with open('wordbook.csv') as csvfile:
		d = csv.reader( csvfile )
		rows = [row for row in d]
		shuffle(rows)
		wordslist = [ (x[0], x[1]) for x in rows[:n] ]
	now=str(date.today())
	# print(now)
	num = n
	param=(now,n)
	c.execute( "create table if not exists `recitecount`( id INTEGER PRIMARY KEY AUTOINCREMENT,date text,num INTEGER)")
	date_row=[]
	for row in c.execute( "select * from 'recitecount' where date = ?",(now,)):
	    date_row.append(list(row))
	# print(date_row)
	if(date_row==[]):
		c.execute( "insert into `recitecount` (date,num) values(?,?)", param)
		conn.commit()
	else:
		c.execute('''UPDATE recitecount SET num=num+? WHERE date=?''',(n,now))
		conn.commit()
	return wordslist

def reviewEbbinghaus(wordnumber2):
	# reload(sys)
	# sys.setdefaultencoding('utf-8')
	w=int(wordnumber2)
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	c.execute( "create table if not exists `reviewwords`( id INTEGER PRIMARY KEY AUTOINCREMENT,en not null, cn not null,date text)")
	filename = ''
	voca_rem = []
	rev_rem=[]
	mode = 0
	while 1:
	    print( "词汇列表文件(回车使用上一次数据): " )
	    filename = str(input())
	    if filename and os.path.isfile(filename):
	        # c.execute( "delete from `reviewwords`" )
	        with open(filename) as csvfile:
	            d = csv.reader( csvfile )
	            rows = [row for row in d]
	            shuffle(rows)
	            to_db = [ (x[0], x[1]) for x in rows[:w] ]
	        c.executemany( "insert into `reviewwords` (en,cn) values(?, ?)", to_db )
	        conn.commit()
	        break
	    elif not filename:
	        break
	    else:
	        print( "未找到文件" )

	while 1:
	    print( "选择背诵模式： 1. 英文提示\t2. 中文提示" )
	    ch = str(input())
	    if ch == '1':
	        mode = 1
	        break
	    elif ch=='2':
	        mode = 2
	        break
	    else:
	        print( "请选择 1 或 2" )

	for row in c.execute( "select * from reviewwords" ):
	    voca_rem.append(list(row))

	if not len(voca_rem):
	    print( "没有找到词汇信息，请确认数据导入情况" )
	    exit()
	print (voca_rem)
	while len(voca_rem):
		flag=0
		temp_rem = []
		clearScr()
		s = len(voca_rem)
		print( "有%d个未掌握词汇，回车开始复习" % (s) )
		input()
		for i in range(0, s):
			if(voca_rem[i][3]!=None):
				forget=getForget(voca_rem[i][3])
				voca_rem[i].append(forget)
				flag = 1
			else:
				flag=0
		if flag==1:
			voca_rem=sorted(voca_rem, key=lambda voca_rem : voca_rem[4]) 
		print (voca_rem)
	    # shuffle(voca_rem)   #Random sort
		for i in range(0, s):
			clearScr()
			print( "第%d个/共%d个"%(i+1, s) )

			if mode==2:
				print( "中文释义: %s"%(voca_rem[i][2], ) )
				if str(input()) == voca_rem[i][1]:
					print( "回答正确" )
				else:
					print( "英文释义：%s"%(voca_rem[i][1], ) )
					id=voca_rem[i][0]
					timenow=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					print(timenow)
					print(id)
					param=(timenow,id)
					c.execute('''UPDATE reviewwords SET date=? WHERE id=?''',param)
					conn.commit()

			else:
				print( "英文释义：%s"%(voca_rem[i][1], ) )
				if str(input()) == voca_rem[i][2]:
					print( "回答正确" )
				else:
					print( "中文释义: %s"%(voca_rem[i][2], ) )
					id=voca_rem[i][0]
					timenow=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					param=(timenow,id)
					c.execute('''UPDATE reviewwords SET date=? WHERE id=?''',param)
					conn.commit()

			print( "\n回车 - 移除该词汇， m+回车 - 标记此词汇" )

			if str(input()) == 'm' :
				temp_rem.append( voca_rem[i] )
				print( "已标记" )

		voca_rem = temp_rem

	print( "复习完毕，现在可以退出" )
	input()

#快速背单词	
def reciteNew(wordnumber1):
	# reload(sys)
	# sys.setdefaultencoding('utf-8')
	w=int(wordnumber1)
	conn = sqlite3.connect('wordbooks.db')
	c = conn.cursor()
	c.execute( "create table if not exists `vocabulary`( en not null, cn not null )" )
	filename = ''
	voca_rem = []
	mode = 0
	while 1:
	    print( "词汇列表文件(回车使用上一次数据): " )
	    filename = str(input())
	    if filename and os.path.isfile(filename):
	        # c.execute( "delete from `vocabulary`" )
	        with open(filename) as csvfile:
	            d = csv.reader( csvfile )
	            rows = [row for row in d]
	            shuffle(rows)
	            print(rows[:w])
	            to_db = [ (x[0], x[1]) for x in rows[:w] ]
	        c.executemany( "insert into `vocabulary` values(?, ?)", to_db )
	        conn.commit()
	        break
	    elif not filename:
	        break
	    else:
	        print( "未找到文件" )

	while 1:
	    print( "选择背诵模式： 1. 英文提示\t2. 中文提示" )
	    ch = str(input())
	    if ch == '1':
	        mode = 1
	        break
	    elif ch=='2':
	        mode = 2
	        break
	    else:
	        print( "请选择 1 或 2" )

	for row in c.execute( "select * from vocabulary" ):
	    voca_rem.append(row)

	if not len(voca_rem):
	    print( "没有找到词汇信息，请确认数据导入情况" )
	    exit()

	while len(voca_rem):
	    temp_rem = []
	    clearScr()
	    s = len(voca_rem)
	    print( "有%d个未掌握词汇，回车开始复习" % (s) )
	    input()

	    shuffle(voca_rem)   #Random sort
	    for i in range(0, s):
	        clearScr()
	        print( "第%d个/共%d个"%(i+1, s) )

	        if mode==2:
	            print( "中文释义: %s"%(voca_rem[i][1], ) )
	            if str(input()) == voca_rem[i][0]:
	                print( "回答正确" )
	            else:
	                print( "英文释义：%s"%(voca_rem[i][0], ) )
	        else:
	            print( "英文释义：%s"%(voca_rem[i][0], ) )
	            if str(input()) == voca_rem[i][1]:
	                print( "回答正确" )
	            else:
	                print( "中文释义: %s"%(voca_rem[i][1], ) )

	        print( "\n回车 - 移除该词汇， m+回车 - 标记此词汇" )

	        if str(input()) == 'm' :
	            temp_rem.append( voca_rem[i] )
	            print( "已标记" )

	    voca_rem = temp_rem

	print( "复习完毕，现在可以退出" )
	input()
if __name__ == '__main__':
	if(args.quickrecite):
		reciteNew(args.quickrecite)
	else:
		reviewEbbinghaus(args.reviewwords)
# conn = sqlite3.connect('wordbooks.db')
# c = conn.cursor()
# timenow=''
# timenow=timenow+datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# c.execute('''UPDATE reviewwords SET date=? WHERE id=?''',('2017-06-16 17:58:38',1))
# conn.commit()
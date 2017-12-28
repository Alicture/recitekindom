# -*- coding: utf-8 -*-
import requests
import sys
import getopt
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
def get_data(url):
	reload(sys)
	sys.setdefaultencoding('utf-8') 
	str1=""
	driver = webdriver.Chrome('/Users/luozepeng/Downloads/chromedriver') # 创建一个driver用于打开网页，记得找到brew安装的chromedriver的位置，在创建driver的时候指定这个位置
	driver.get(url) # 打开网页
	time.sleep(2)
	page = 0;
	while page<3:
		url=url+"?page={}".format(page)
		time.sleep(2)
		soup=bs(driver.page_source,"html.parser")
		data = soup.select('div.span8 > table > tbody > tr')
		for line in data:
		    for d in line.findAll('td',class_="span2"):
	    		words=d.text
		    for d in line.findAll('td',class_="span10"):
	        	trans=d.text
	        	trans=trans.replace("\n","")
			print(words+","+trans+"\n")
			str1+=words+","+trans+"\n"
		driver.find_element_by_xpath("//div[@class='jquery-bootstrap-pagination pagination']/ul/li/a[contains(text(),'>')]").click()
		print(page)
		page=page+1
	fout = open('wordbook.csv','a')
	fout.write(str1)
	time.sleep(1)
	fout.close() 
def get_url(url):
	result = requests.get(url)
	page =result.text
	doc =bs(page,"html.parser")
	data = doc.select('.wordbook-wordlist-name')
	urls=[]
	for line in data:
		urls=urls+[element.get('href') for element in line.findAll('a')]
	return urls
#单词本 https://www.shanbay.com/wordbook/34/
# def main(argv):
#    url = ''
#    page = ''
#    try:
#       opts, args = getopt.getopt(argv,"hi:o:",["oriurl=","pagenum="])
#    except getopt.GetoptError:
#       print 'crawler.py -u <sourceurl> -p <pagenumber>'
#       sys.exit(2)
#    for opt, arg in opts:
#       if opt == '-h':
#          print 'crawler.py -u <sourceurl> -p <pagenumber>'
#          sys.exit()
#       elif opt in ("-u", "--oriurl"):
#          url = arg
#       elif opt in ("-p", "--pagenum"):
#          outputfile = arg
#    get_data(url,page)

# if __name__ == "__main__":
#    main(sys.argv[1:])
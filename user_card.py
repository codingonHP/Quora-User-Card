from flask import Flask,jsonify,render_template,request
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("main.html")



@app.route("/quoracard/<username>",methods=["GET"])
def get_details(username):
	baseUrl = "https://www.quora.com/profile/"
	soup = BeautifulSoup(requests.get(baseUrl+username).text,'html.parser')
	imgUrl = soup.find('img',{'class':'profile_photo_img'}).get('src')
	profileName = soup.find('div',{'class':'ProfileNameAndSig'}).find('span',{'class':'user'}).text
	answerCount = soup.find('div',{'class':'nav_item_selected'}).findAll('span',{'class':'list_count'})[0].text
	followerCount = soup.find('li',{'class':'FollowersNavItem'}).findAll('span',{'class':'list_count'})[0].text
	try:
		viewCount = soup.find('div',{'class':'AboutListItem AnswerViewsAboutListItem'}).text.split(' ')[0]
	except(AttributeError):
		viewCount = 0	
	
	
	try:

		topWriter = soup.find('div',{'class':'AboutListItem TopWriterAboutListItem'}).text.split(' ')[0]
		tpFlag = 1 
	except(AttributeError):
		tpFlag = 0

	return render_template("card.html",profileurl=baseUrl+username,imgUrl=imgUrl,profileName=profileName,answerCount=answerCount,followerCount=followerCount,viewCount=viewCount,tpFlag=tpFlag)	


if __name__ == '__main__':
	app.run()

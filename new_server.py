import os, json
from flask import Flask, render_template, request, make_response
from werkzeug import secure_filename
import csv
import sys
import pymongo
from bson.objectid import ObjectId
from os import walk

app = Flask(__name__)
MONGODB_URI = "mongodb://sneha:test123@ds063150.mongolab.com:63150/testmongolabs"

@app.route('/')
def index():
	return render_template('index.html')
    # return 'Hello World!'


@app.route('/graphFromData', methods = ['GET', 'POST'])
def generate_graph():
	if request.method == 'GET':
		print request
		return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))
	# if request.method == 'POST':

	return "Graph generated Successfully!"

@app.route('/generategraph', methods = ['GET', 'POST'])
def get_graph():
	if request.method == 'GET':
		print request
		return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))
	if request.method == 'POST':
		print request
		return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))

@app.route('/searchProduct',methods =['GET','POST'])
def search_products():
	if request.method == 'GET':
		print "checking search keyword " + request.args['searchKeyword']
		keyword = request.args['searchKeyword']
		
		client = pymongo.MongoClient(MONGODB_URI)
		db = client.get_default_database()
		prod_details = db['prod_details']
		cursor = prod_details.find({'ProdName': keyword })
		# { '$in': [ '/ keyword /' ] }
		#.sort('prodId', 1)
		
		listProd = []
		# print ('prodId: %d,Prod Name: %s , Prod Desc: %s.' % (doc['prodId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
		for doc in cursor: 
			print doc['ProdId']
			print ('ProdId: %d,Prod Name: %s , Prod Desc: %s, ProdCount: %d' % (doc['ProdId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
			listProd.append(doc)
		
		client.close()
		return render_template("search.html", status = "Search Successful!", item2 = listProd, itemlist = listProd)
	if request.method == 'POST':
		return render_template('search.html')

# @app.route('/modifyCount', methods = ['GET','POST'])
@app.route('/likeItem', methods = ['GET'])
def like_item():
	print "hello"
	itemCount = 0
	# print "checking search arg id- item id: " + str(request.args["_id"])
	if request.method == 'GET':
		itemId = request.args["id"]
		client = pymongo.MongoClient(MONGODB_URI)
		db = client.get_default_database()
		prod_details = db['prod_details']
		cursor = prod_details.find({"_id" : ObjectId(itemId) })
		for doc in cursor:
			print doc['ProdCount']
			itemCount = doc['ProdCount'] + 1

		prod_details.update( {"_id" : ObjectId(itemId) },{ "$set": {'ProdCount' : itemCount }}	)

		client.close()
	return str(itemCount)	

@app.route('/search',methods =['GET','POST'])
def search():
	if request.method == 'GET':
		print request
		return render_template('search.html')
	if request.method == 'POST':
		print request
	return render_template("search.html")


@app.route('/customerDashboard', methods =['GET','POST'])
def dashboard():
	return render_template('customerDashboard.html')
	#, status = "Search Successful!", item2 = listProd, itemlist = listProd)

@app.route('/retailerDashboard', methods =['GET','POST'])
def retailer_dashboard():
	return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))

@app.route('/about')
def about():
	return render_template('contactUs.html')

@app.route('/services')
def services():
	return render_template('services.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/contact')
def contact():
	return render_template('contactUs.html')

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)

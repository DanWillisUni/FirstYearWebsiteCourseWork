#imports
from flask import Flask
from flask import Flask,render_template,redirect,flash, session, abort, request
import csv
import datetime
import time
import os
import math

app = Flask(__name__)

#reads all the lines from a file into a list
def readFile(aFile):
	#opens a file object	
	with open(aFile,'r') as inFile:
		#reads the file into an array
		reader = csv.reader(inFile)
		aList = [row for row in reader]
	return aList

#writes the specified list to the file specified
def writeFile(aList,aFile):
	#opens a file object
	with open(aFile,'a',newline='') as outFile:
		#writes to a file
		writer = csv.writer(outFile)
		writer.writerows(aList)
	return

#overwrites the file
def overWriteFile(aList,aFile):
	with open(aFile,'w',newline='') as outFile:
		#writes to a file
		writer = csv.writer(outFile)
		writer.writerows(aList)
	return

#checks the date is in the correct format    
def Validate(date_text):
	try:
		#checks if the date is valid
		if date_text != datetime.datetime.strptime(date_text, '%d/%m/%y').strftime('%d/%m/%y'):
			raise ValueError
		return True
	except ValueError:
		return False
#gets the dates between 2 dates
def daterange(date1str, date2str):
	#makes the date string into date objects
	date1 = datetime.datetime.strptime(date1str, '%d/%m/%y')
	date2 = datetime.datetime.strptime(date2str, '%d/%m/%y')
	#gets all the dates in the range
	for n in range(int ((date2 - date1).days)+1):
		yield date1 + datetime.timedelta(n)

#homepage
@app.route('/')
def home():
	return render_template('home.html')

#shows reviews
@app.route('/review')
def review():	
	aList = readFile('static\\reviews.csv')#reads in the file of reviews
	return render_template('review.html',aList = aList)

#add reviews
@app.route('/addReview',methods=['GET'])
def addReview():
	name = request.args['name']
	#sets the name to 'Anon' if it is left blank
	if name == "":
		name = "Anon"
	comment = request.args['comment']
	date = datetime.datetime.strptime(time.strftime("%x"), '%m/%d/%y').strftime('%d/%m/%y')#et todays date and convert it to conventional UK	
	newList=[name,comment,date]#getting the informationin the correct format to add to the file
	newListList=[newList]
	writeFile(newListList,'static\\reviews.csv')#writing to the file	
	return review()#rerender reviews page	

#display current rentals
@app.route('/renting')
def renting():
	wholeList = readFile('static\\bookings.csv')
	aList =[]
	for item in wholeList:
		#leaving out the persoal info
		newList=[item[0],item[1],item[4]]
		aList.append(newList)
	return render_template('renting.html',aList = aList)

#requesting a rental, including validation and a price calculation
@app.route('/addBooking',methods=['GET'])
def addBooking():
	Continue = True;
	name = request.args['name']
	email = request.args['email']
	rawarrival = request.args['arrival']	
	arrival = datetime.datetime.strptime(rawarrival, '%Y-%m-%d').strftime("%d/%m/%y")#converting the arrival date object to a string
	if Validate(arrival) == False: #if the arrival date isnt a date
		Continue = False
		flash("Arrival date invalid")	
	rawdeparture = request.args['departure']	
	departure = datetime.datetime.strptime(rawdeparture, '%Y-%m-%d').strftime("%d/%m/%y")#converting the departure object to a string
	if Validate(departure) == False:#if the departure date isnt a date
		Continue = False
		flash("Departure date is invalid")
	at = (datetime.datetime.strptime(arrival,'%d/%m/%y')-datetime.datetime(1970,1,1)).total_seconds()#get the total amount of seconds to the arrival date
	dt = (datetime.datetime.strptime(departure,'%d/%m/%y')-datetime.datetime(1970,1,1)).total_seconds()#get the total amount of seconds to the departure date
	if at >= dt:#if the arrival date is greater than the departure date
		Continue = False
		flash("Arrival date is after the Departure date")
	if int(time.time()) > at: #if arrival date is in the past
		Continue = False
		flash("Arrival date is in the past or today")
	#checking for double booking
	wholeList = readFile('static\\bookings.csv')
	allDateList = []	
	for item in wholeList:#for each line in the file
		#picks out the dates and gets every date in between the dates
		for dt in daterange(item[0],item[1]):
			allDateList.append(dt)#gets every date already booked
	newList = []
	for dt in daterange(arrival, departure):
		newList.append(dt)#gets all the dates of their stay
	Broken = False #to break the second loop
	for i in allDateList:#for every date already booked
		for o in newList:#for every date in the new booking
			if i == o:#if two dates match
				Continue = False
				flash("Double booking")
				Broken = True
				break;
		if Broken == True:
			break;	
	if Continue == True:#if everything is valid
		newList=[arrival,departure,name,email,"NC"]
		newListList=[newList]
		writeFile(newListList,'static\\bookings.csv')#add the booking to the file
		#work out price 
		peakDates = 0
		nonPeakDates = 0
		newList = []
		for dt in daterange(arrival, departure):#for each date in between arrival and departure
			newList.append(dt)#add the date to the array
		counter = 0#to skip the first day easily
		for i in newList:#for each date in the file
			if(counter != 0):
				if (i.month == 7 or i.month == 8 or i.month == 9):#if the month is peak
					peakDates += 1
				else:
					nonPeakDates += 1
			counter += 1
		price = str((50*nonPeakDates) + (70*peakDates))#add the peak and nonpeak prices up
		flash('It costs £' + price)#flash the price
	#re render renting	
	return renting()

#local attractions page
@app.route('/attractions')
def attractions():
	return render_template('attractions.html')

#admin page
@app.route('/admin')
def admin():
	if not session.get('logged_in'):#if not logged in
		return render_template('login.html')
	else:
		#render admin
		wholeList = readFile('static\\bookings.csv')
		aList =[]
		for item in wholeList:
			newList=[item[0],item[1],item[2],item[3],item[4]]
			aList.append(newList)
		return render_template('admin.html',aList = aList)

#Confirmation of bookings
@app.route('/confirmation',methods=['GET'])
def confirmation():
	email = request.args['email']
	wholeList = readFile('static\\bookings.csv')#reads in thw whole file
	aList =[]
	for item in wholeList:#for each line in the file
		if email == item[3]:#if the email matchs the email the admin is looking for
			item[4]="C"#change it to confirmed
	overWriteFile(wholeList,'static\\bookings.csv')#overwrite everthing in the file	
	return admin()

#login page
@app.route('/login', methods=['POST'])
def admin_login():
	if request.form['password'] == '1234' and request.form['username'] == 'admin':#if username and password are correct
		session['logged_in'] = True#log the admin in
	return admin()

#logging out
@app.route('/logout')
def logout():
	session['logged_in'] = False#logs out
	return render_template('home.html')

if __name__ == '__main__':
	app.secret_key = 'PlsGiveUsFullMarks:)'#secret key used for flash
	app.run(debug = True)
from flask import Flask, render_template, request, redirect, session, get_template_attribute, jsonify
from flask.json import JSONEncoder

import sys
import json

import random
app = Flask(__name__)

app.secret_key = 'bineet'

email_addresses = []
batters = []
bowlers = []
match = None
batter_on_strike = None
batter_on_non_strike = None
bowler_bowling = None
batter_on_strike_id = None
batter_on_non_strike_id = None
bowler_bowling_id = None

#Batter class 
class Match(object):

	def __init__ (self, venue, teams, pool, score):
		self.venue = venue
		self.teams = teams
		self.pool = pool
		self.score = score
						
	def next(self):
		return self.pool.next()
		
	def setPool(self, pool):
		self.pool = pool
		
	def nextBatterId(self):
		return str(self.score.wickets+2)

#Batter class 
class Batter(object):

	def __init__ (self, id, name, onstrike, pool):
		self.id = id
		self.name = name
		self.runs = 0
		self.balls = 0
		self.is_batting = 1
		self.is_out = 0
		self.on_strike = onstrike
		self.pool = pool
		self.partner = None
		self.image = 'http://lorempixel.com/200/200/'
		self.order = None

	def setOrder(self, order):
		self.order = order
		
	def next(self):
		return self.pool.next()
		
	def setPool(self, pool):
		self.pool = pool
	
	def addPartner(self, partner):
		self.partner = partner 
		
	def addScore(self, next):
		if(next == 'a'): # 1
			self.runs += 1
			self.balls += 1
			self.on_strike = 0
			return self.partner.id
			
		if(next == 'b'): # .
			self.balls += 1
			return self.id
			
		if(next == 'c'): # W
			self.balls += 1
			self.on_strike = 0
			self.is_batting = 0
			return None
			
# Bowler class
class Bowler(object):

	def __init__ (self, id, name, pool):
		self.id = id
		self.name = name
		self.runs = 0
		self.balls = 0
		self.is_bowling = self.balls%6 != 0
		self.is_bowled_out = 0
		self.has_bowled = 0
		self.wickets = 0
		self.wideBalls = 0
		self.noBalls = 0
		self.pool = pool
		self.image = 'http://lorempixel.com/200/200/'
				
	def next(self):
		return self.pool.next()
		
	def setPool(self, pool):
		self.pool = pool
		
	def addScore(self, next):
		if(next == 'a'): # 1
			self.runs += 1
			self.balls += 1
			
		if(next == 'b'): # .
			self.balls += 1
			
		if(next == 'c'): # W
			self.balls += 1
			self.wickets += 1
		

# Score class to maintain the match score		
class Score(object):

	def __init__ (self):
		self.runs = 0
		self.balls = 0
		self.wickets = 0
		self.overs = "0.0"
		
	def add(self, next):
		if(next == 'a'): # for 1
			self.runs+=1
			self.balls+=1
		elif(next == 'b'): # for .
			self.balls+=1
		elif(next == 'c'): # for W
			self.wickets+=1
			self.balls+=1
		

# Pool class to get the next ball outcome	
class Pool(object):

	def __init__ (self, a, b, c):
		self.pool = []
		for index in range(a):
			self.pool.append('a')
			
		for index in range(b):
			self.pool.append('b')
			
		for index in range(c):
			self.pool.append('c')		
	
	def next(self):
		return random.choice(self.pool)
			
	def addA(self, match, batter, bowler):
		#self.pool.append('a')
		match.pool.append('a')
		batter.pool.append('a')
		bowler.pool.append('a')
	
	def addB(self, match, batter, bowler):
		#self.pool.append('b')
		match.pool.append('b')
		batter.pool.append('b')
		bowler.pool.append('b')
		
	def addC(self, match, batter, bowler):
		#self.pool.append('c')
		match.pool.append('c')
		batter.pool.append('c')
		bowler.pool.append('c')
		

class MyJSONEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Batter):
			return {
				'name': obj.name, 
				'runs': obj.runs,
				'balls': obj.balls,
				'on_strike': obj.on_strike,
				'is_batting':obj.is_batting,
				'image': obj.image
			}
		elif isinstance(obj, Bowler):
			return {
				'name': obj.name, 
                'runs': obj.runs,
                'balls': obj.balls,
				'wickets': obj.wickets,
				'is_bowling': obj.is_bowling,
				'image': obj.image
			}
		elif isinstance(obj, Match):
			return {
				'venue': obj.venue
			}
		return super(MyJSONEncoder, self).default(obj)
		
app.json_encoder = MyJSONEncoder
		
@app.route('/')
def hello_world():	
	return render_template('index.html', score=Score(), batters={})


@app.route('/start', methods = ['GET','POST'])
def start():
	global batters
	global bowlers
	global match
	global batter_on_strike
	global batter_on_non_strike
	global bowler_bowling
	global batter_on_strike_id
	global batter_on_non_strike_id
	global bowler_bowling_id
	
	match = Match("Ranchi", ["India","Australia"], Pool(11, 9, 1), Score())
	
	bowler1 = Bowler("1", "Bineet", Pool(12, 10, 1))
	bowler2 = Bowler("2", "Bineet", Pool(12, 10, 1))
	bowler3 = Bowler("3", "Bineet", Pool(12, 10, 1))
	bowler4 = Bowler("4", "Bineet", Pool(12, 10, 1))
	bowler5 = Bowler("5", "Bineet", Pool(12, 10, 1))
	bowler6 = Bowler("6", "Bineet", Pool(12, 10, 1))
	bowler7 = Bowler("7", "Bineet", Pool(12, 10, 1))
	bowler8 = Bowler("8", "Bineet", Pool(12, 10, 1))
	bowler9 = Bowler("9", "Bineet", Pool(12, 10, 1))
	bowler10 = Bowler("10", "Bineet", Pool(12, 10, 1))
	bowler11 = Bowler("11", "Bineet", Pool(12, 10, 1))
	
	bowlers = {bowler1.id : bowler1, bowler2.id:bowler2, bowler3.id:bowler3, bowler4.id:bowler4, bowler5.id:bowler5, bowler6.id:bowler6, bowler7.id:bowler7, bowler8.id:bowler8, bowler9.id:bowler9, bowler10.id:bowler10, bowler11.id:bowler11}
	
	batter1 = Batter("1", "Mishra", 1, Pool(10, 12, 2))		
	batter2 = Batter("2", "Kumar", 0, Pool(14, 8, 1))
	batter3 = Batter("3", "Mishra", 0, Pool(10, 12, 2))		
	batter4 = Batter("4", "Kumar", 0, Pool(14, 8, 1))
	batter5 = Batter("5", "Mishra", 0, Pool(10, 12, 2))		
	batter6 = Batter("6", "Kumar", 0, Pool(14, 8, 1))
	batter7 = Batter("7", "Mishra", 0, Pool(10, 12, 2))		
	batter8 = Batter("8", "Kumar", 0, Pool(14, 8, 1))
	batter9 = Batter("9", "Mishra", 0, Pool(10, 12, 2))		
	batter10 = Batter("10", "Kumar", 0, Pool(14, 8, 1))
	batter11 = Batter("11", "Mishra", 0, Pool(10, 12, 2))

	batters = {batter1.id:batter1, batter2.id:batter2, batter3.id:batter3, batter4.id:batter4, batter5.id:batter5, batter6.id:batter6, batter7.id:batter7, batter8.id:batter8, batter9.id:batter9, batter10.id:batter10, batter11.id:batter11}
	
	batter_on_strike = batters["1"]
	batter_on_strike_id = batter_on_strike.id

	batters["1"].addPartner(batters["2"])
	batters["2"].addPartner(batters["1"])
		
	bowler_bowling = bowlers["1"]
	bowler_bowling_id = bowler_bowling.id

	return jsonify(runs=match.score.runs, wickets=match.score.wickets, overs=str(int(match.score.balls/6)) +"."+ str(match.score.balls%6), batters=batters, bowlers=bowlers)	
	
@app.route('/next', methods = ['GET','POST'])
def next():

	global batters
	global bowlers
	global match
	global batter_on_strike
	global batter_on_non_strike
	global bowler_bowling
	global batter_on_strike_id
	global batter_on_non_strike_id
	global bowler_bowling_id


	bat_score = batter_on_strike.next()
	bowl_score = bowler_bowling.next()
	match_score = match.next()
	
	score = random.choice([bat_score, bowl_score, match_score])
	
	match.score.add(score);
	
	batter_on_strike_id = batter_on_strike.addScore(score)

	if(batter_on_strike_id == None):
		nextBatterId = match.nextBatterId()
		batters[nextBatterId].addPartner(batter_on_strike.partner)
		batter_on_strike.partner.addPartner(batters[nextBatterId])
		batter_on_strike = batters[nextBatterId]
	else:
		batter_on_strike = batters[batter_on_strike_id]


	bowler_bowling.addScore(score)
			
	return jsonify(runs=match.score.runs, wickets=match.score.wickets, overs=str(int(match.score.balls/6)) +"."+ str(match.score.balls%6), batters=batters, bowlers=bowlers)	

@app.route('/save', methods = ['GET', 'POST'])
def save():
	global batters
	print (batters)

	try:
		for i in range(1, 2):
			print ('sl_batter_'+ str(i) + '')
			print (request.form['ih_batter_1'])
			index = request.form['sl_batter_'+ str(i) + '']
			print('index: '+index)
			#batters[index].setOrder(str(i))
			#print('batter order: ' + batters[index].order)

		return json.dumps({'html':'<span>All fields good !!</span>'})

	except:
		print (sys.exc_info()[0])
		return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route('/signup', methods = ['POST'])
def signup():
	email = request.form['email']
	email_addresses.append(email)
	return redirect('/')
	
@app.route('/emails.html')
def emails():
	return render_template('emails.html', email_addresses=email_addresses)

@app.route('/setup', methods = ['GET','POST'])
def setup():
	global batters	
	global bowlers

	return render_template('setup.html', batters=batters, bowlers=bowlers)

if __name__ == "__main__":
	app.run(debug=True)
	
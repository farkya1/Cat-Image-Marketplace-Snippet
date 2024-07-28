# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from .utils.blockchain.blockchain import Blockchain
from werkzeug.datastructures   import ImmutableMultiDict
from datetime import datetime
from pprint import pprint
import json
import random
import functools
import os

import string
import random
#from . import socketio
db = database()



#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function


#gets the email of the user
def getUser():

	return db.reversibleEncrypt('decrypt', session['email']) if 'email' in session else 'Unknown'

#logins the user
@app.route('/login')
def login():
	return render_template('login.html')

#gets the email of the user
@app.route('/getemail', methods = ["GET"])
@login_required
def getEmail():
	return json.dumps({'email':getUser()})

#logouts the user
@app.route('/logout')
def logout():
	session.pop('email', default=None)

	if 'admin' in session:
		session.pop('admin', default=None)
	return redirect('/')

#proccess the login information to see if the user is in the system
@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():

	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	
	result = db.authenticate(form_fields['email'],form_fields['password'])
	

	if result['success'] != 1:
		return json.dumps({'success':0})

	session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
	if len(db.query(f"""SELECT * FROM users WHERE email = \"{form_fields['email']}\" AND role = 'admin'""")):
		session["admin"] = True


	return json.dumps({'success':1})


#gets a random string of length
def generateRandomKey():
    
    characters = string.ascii_letters + string.digits

    randomChars = random.choices(characters, k=30)

    randomKey = ''.join(randomChars)

    return randomKey

#proccess the login information to see if the user is in the system
@app.route('/signupuser', methods = ["POST"])
def signupuser():

	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))

	if len(db.query(f"SELECT * from users WHERE email = '{form_fields['email']}'")):
		
		return json.dumps({'success':0})
	
	result = db.createUser(form_fields['email'],form_fields['password'])
	if result['success'] != 1:
		return json.dumps({'success':0})
	
	session['email'] = db.reversibleEncrypt('encrypt', form_fields['email'])

	user = db.query(f"SELECT * from users WHERE email = '{form_fields['email']}'")[0]

	key = generateRandomKey()
		
	header = ["user_id","string_key"]
	information = [[]]

	information[0].append(user["user_id"])
	information[0].append(key)

	db.insertRows("wallet",header,information)

	header = ["string_key","token"]
	information = [[]]

	information[0].append(key)

	information[0].append(random.randint(10,40))

	db.insertRows("tokens",header,information)

	return json.dumps({'success':1})



#######################################################################################
# CHATROOM RELATED
#######################################################################################
#runs the chat page
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

"""

#runs to make the user join the chat and print a message
@socketio.on('joined', namespace='/chat')
def joined(message):
    returnDict = {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:grey;text-align: left'}
    join_room('main')
    if "owner" in session:
        returnDict["style"] = 'width: 100%;color:blue;text-align: right' 
    emit('status', returnDict, room='main')
    

#runs to make the user print a message
@socketio.on('message', namespace='/chat')
def message(message):
    returnDict = {'msg': message, 'style': 'width: 100%;color:grey;text-align: left'}
    if "owner" in session:
        returnDict["style"] = 'width: 100%;color:blue;text-align: right'
    emit('status', returnDict, room='main')

#runs to make the user leave the chat and print a message saying so
@socketio.on('leaving', namespace='/chat')
def leaving():
	leave_room('main')
	if "owner" in session:
		emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	else:
		emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:grey;text-align: left'}, room='main')
		
"""

#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	print(db.query('SELECT * FROM users'))
	x = random.choice(['I have a twin sister.','I have two pet cats.',"I'm an Eagle Scout."])
	return render_template('home.html', user=getUser(), fun_fact = x)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

#runs when feedback is submitted
@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	feedback = request.form
	header = ["name", "email", "feedback"]
	information = [[]]
	information[0].append(feedback["name"])
	information[0].append(feedback["email"])
	information[0].append(feedback["feedback"])

	db.insertRows("feedback", header, information)

	all_feedback = db.query("SELECT * from feedback")

	feedback_data = {}

	for feedback in all_feedback:
		temp_feedback = {}
		temp_feedback["name"] = feedback["name"]
		temp_feedback["feedback"] = feedback["feedback"]
		feedback_data[feedback["feedback_id"]] = temp_feedback


	return render_template('processfeedback.html', feedback_data = feedback_data)



#where you view your nfts
@app.route('/nftsell')
@login_required
def nftsell():
	#collects the relavent information for the page

	user = db.query(f"SELECT * from users WHERE email = '{getUser()}'")[0]
	nfts = db.query(f"SELECT * from images WHERE user_id = '{user['user_id']}'")
	nfts_data = {}
	nfts_data["images"] = nfts

	wallet = db.query(f"SELECT * from wallet WHERE user_id = '{user['user_id']}'")[0]
	tokens = db.query(f"SELECT * from tokens WHERE string_key = '{wallet['string_key']}'")[0]

	nfts_data["tokens"] = tokens["token"]

	return render_template('nftsell.html',image_data = nfts_data)

#where you can buy nfts
@app.route('/nftbuy')
@login_required
def nftbuy():

	#collects the relavent information for the page
	user = db.query(f"SELECT * from users WHERE email = '{getUser()}'")[0]
	notOwned = db.query(f"SELECT * from images WHERE user_id != '{user['user_id']}'")

	nfts_data = {}
	nfts_data["images"] = notOwned

	wallet = db.query(f"SELECT * from wallet WHERE user_id = '{user['user_id']}'")[0]
	tokens = db.query(f"SELECT * from tokens WHERE string_key = '{wallet['string_key']}'")[0]
	nfts_data["tokens"] = tokens["token"]

	return render_template('nftbuy.html', image_data = nfts_data)

#the signup form page
@app.route('/signup')
def signup():
	return render_template('signup.html')

#the start to the marketplace
@app.route('/marketplaceenter')
@login_required
def marketplaceenter():
	return render_template('marketplaceenter.html')

#runs when the user wants to create or upload a nft
@app.route('/ownednft', methods=['POST'])
@login_required
def ownednft():
	form = request.form

	header = ["image_name","description","tokens","user_id"]
	information = [[]]

	
	if(form["action"] == "Upload NFT"):

		#determines if the user would like to upload
		uploaded_file = request.files['fileToUpload']
		if uploaded_file:

			#determines if the user has a file to upload
			uploaded_file.filename = generateRandomKey()+".jpg"

			#randomises the filename not get duplicates in the folder
			
			information[0].append(uploaded_file.filename)
			folder_path = os.getcwd() + r"/flask_app/static/marketplace/images/"+uploaded_file.filename
			uploaded_file.save(folder_path)

			information[0].append(form["NFT Description"])
			information[0].append(form["NFT Token"])
			user = db.query(f"SELECT * from users WHERE email = '{getUser()}'")[0]
			information[0].append(user["user_id"])
			
			
			imageID = db.insertRows("images",header,information)

			#add it to the blockchain class

			chain = Blockchain(1,{"owner":getUser(),"image_name":uploaded_file.filename},[])
			

			header = ["image_id","chain"]
			information = [[]]

			information[0].append(imageID)

			information[0].append(json.dumps(chain.to_dict()))

			blockchainID = db.insertRows("blockchain",header,information)

			header = ["blockchain_id","hashes"]
			information = [[]]

			information[0].append(blockchainID)
			information[0].append(json.dumps([]))

			db.insertRows("hashes",header,information)

			return redirect('/nftsell')
		
	#runs if user is creating nft or did not have a file to upload
	folder_path = os.getcwd() + r"/flask_app/static/marketplace/images"

	#randomly picks file from image folder if not already in use
	files = os.listdir(folder_path)
	random_file = random.choice(files)	
	while len(db.query(f"SELECT * from images WHERE image_name = '{random_file}'")) != 0:
		random_file = random.choice(files)	

	

	information[0].append(random_file)

	information[0].append(form["NFT Description"])
	information[0].append(form["NFT Token"])
	user = db.query(f"SELECT * from users WHERE email = '{getUser()}'")[0]
	information[0].append(user["user_id"])
	

	imageID = db.insertRows("images",header,information)	

	#add it to the blockchain class
	chain = Blockchain(1,{"owner":getUser(),"image_name" : random_file},[])
	

	header = ["image_id","chain"]
	information = [[]]

	information[0].append(imageID)

	jsonDump = chain.to_dict()

	information[0].append(json.dumps(jsonDump))

	blockchainID = db.insertRows("blockchain",header,information)

	header = ["blockchain_id","hashes"]
	information = [[]]

	information[0].append(blockchainID)
	information[0].append(json.dumps([]))



	db.insertRows("hashes",header,information)


	return redirect('/nftsell')


#the user is buying a nft
@app.route('/nftbought', methods = ['POST'])
@login_required
def nftbought():
	purchase = request.form

	imageID = purchase["image"]

	#gets relevant info from the databases
	image = db.query(f"SELECT * from images WHERE image_id = '{imageID}'")[0]

	userBuyer = db.query(f"SELECT * from users WHERE email = '{getUser()}'")[0]

	walletBuyer = db.query(f"SELECT * from wallet WHERE user_id = '{userBuyer['user_id']}'")[0]

	tokensBuyer = db.query(f"SELECT * from tokens WHERE string_key = '{walletBuyer['string_key']}'")[0]


	#determines if the user has enough tokens
	if tokensBuyer["token"] >= image["tokens"]:
		chainDB = db.query(f"SELECT * from blockchain WHERE image_id = '{imageID}'")[0]
		chainDate = json.loads(chainDB["chain"])
		chain = Blockchain.from_dict(chainDate)

		sellerUser = db.query(f"SELECT * from users WHERE user_id = '{image['user_id']}'")[0]

		#sets up the transation info
		transaction = {"currentOwner":userBuyer["email"],"sellerEmail":sellerUser["email"],"sellerID":sellerUser["user_id"],"buyerEmail":userBuyer["email"],"buyerID":userBuyer["user_id"],"cost":image["tokens"], "image_id":imageID, "image_name":image["image_name"]}

		#the blockchain starts mining
		if(chain.mine_transaction(transaction)):
			db.query(f"UPDATE tokens SET token = {tokensBuyer['token'] - image['tokens']} WHERE string_key = '{walletBuyer['string_key']}'")
			db.query(f"UPDATE images SET user_id = '{userBuyer['user_id']}' WHERE image_id = '{imageID}'")
			walletSeller = db.query(f"SELECT * from wallet WHERE user_id = '{sellerUser['user_id']}'")[0]
			tokensSeller = db.query(f"SELECT * from tokens WHERE string_key = '{walletSeller['string_key']}'")[0]

			db.query(f"UPDATE tokens SET token = {tokensSeller['token'] + image['tokens']} WHERE string_key = '{walletSeller['string_key']}'")
			print(db.query("SELECT * from blockchain"))
			return redirect('/nftbuy')

	else:
		#user does not have enough tokens
		return redirect('/badtransaction')
		

#the user does not have enough tokens
@app.route('/badtransaction')
@login_required
def badtransaction():
	return render_template('badtransaction.html')

#runs when the user edits their nft
@app.route('/editimage', methods = ['POST'])
@login_required
def editimage():
	editImage = request.form

	#the user would like to change the description
	if editImage.get("imageDescription"):
		db.query(f"UPDATE images SET description = '{editImage['imageDescription']}' WHERE image_id = '{editImage['imageID']}'")

	#the user would like to change the price
	if editImage.get("imageTokens"):
		db.query(f"UPDATE images SET tokens = '{editImage['imageTokens']}' WHERE image_id = '{editImage['imageID']}'")

	return redirect('/nftsell')


#gets all the nfts on the site
@app.route('/blockchainactivity')
@login_required
def blockchainactivity():

	images = db.query(f"SELECT * from images ")
	return render_template('blockchainactivity.html', image_data = images)

#views a specific nft that shows the transaction history
@app.route('/viewblockchain', methods = ['POST'])
@login_required
def viewblockchain():
	image = request.form

	#gets blockchain from database
	chainDB = db.query(f"SELECT * from blockchain WHERE image_id = '{image['imageID']}' ")[0]
	chainDate = json.loads(chainDB["chain"])
	print(chainDate)

	return render_template('viewblockchain.html', chain_data = chainDate)


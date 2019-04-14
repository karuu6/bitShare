from flask import Flask, request, redirect, render_template, url_for, session
from werkzeug import secure_filename
from sql import DB
from crypto import _hash, get_id
import uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY']='bitshare'
app.config['UPLOAD_FOLDER'] = '/home/documents/projects/bitShare-master/static/songs'

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		if session['logged_in']:
			db  = DB('db',False)
			title=request.form['title']
			art=request.form['art']
			f=request.files['fileupload']
			fname=get_id()
			f.save('static/songs/{}.mp3'.format(fname))
			db.add_song(session['email'], title, art, fname)
			return redirect(url_for('dashboard'))
	else:
		try:
			if session['logged_in'] is True:
				return render_template('upload.html')
		except:
			return render_template('login.html')
	return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
	db = DB('db', False)
	if request.method == 'POST':
		print(request.form)
		email = request.form['username']
		pwd   = request.form['password']
		addr  = request.form['btc-address']
		sig   = _hash(pwd)
		db.add(email,sig,addr)
		return render_template('login.html')
	return render_template('register.html')


@app.route('/dashboard')
def dashboard():
	db = DB('db', False)
	try:
		if session['logged_in']:
			song_ids=db.get_song_ids(session['email'])
			songs = [db.get_song_details(id) for id in song_ids]
			return render_template('dashboard.html',songs=songs, email=session['email'])
	except:
		return render_template('login.html')
	return render_template('login.html')


@app.route('/song/<uid>')
def song(uid):
	db = DB('db', False)
	song=db.get_song_details(uid)
	user=db.get_song_user(uid)
	db.add_view(uid)
	return render_template('song.html', song=song, user=user)

@app.route('/delete/<uid>')
def delete(uid):
	db = DB('db', False)
	if session['logged_in'] is True:
		status = db.delete_song(uid, session['email'])
		if status is True:
			return redirect(url_for('dashboard'))
		elif status is False:
			return 'PERMISSION DENIED ----'
		else:
			return 'SONG NOT FOUND'
	return redirect(url_for('login'))


@app.route('/logout')
def logout():
	session['logged_in']=False
	session['email']=''
	return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		db = DB('db', False)
		email = request.form['username']
		pwd   = request.form['password']
		sig   = _hash(pwd)
		if db.check(email,sig):
			session['logged_in']=True
			session['email']=email
			return redirect(url_for('dashboard'))
	try:
		if session['logged_in'] is True:
			return redirect(url_for('dashboard'))
	except:
		return render_template('login.html')
	return render_template('login.html')




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

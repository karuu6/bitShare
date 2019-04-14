import marshal
import sqlite3
import uuid
import datetime
import os
import sys
from crypto import _hash, get_id


class DB(object):
	def __init__(self, file, init=False):
		self.file = file
		if not os.path.exists(self.file):
			open(self.file, 'a').close()
		self.conn = sqlite3.connect(self.file)
		self.c    = self.conn.cursor()
		if init:
			self._init()

	def _init(self):
		self.c.execute('''CREATE TABLE users
					  (email text, password text, address text, songs text)''')
		self.c.execute('''CREATE TABLE songs
					  (id text, title text, date text, views integer, art text, user text)''')
		self.conn.commit()

	def _serialize(self,x):
		return marshal.dumps(x)

	def add(self, email, hash, addr):
		songs=''
		self.c.execute('SELECT * FROM users WHERE email=?', (email,))
		if not self.c.fetchone():
			self.c.execute('INSERT INTO users values (?,?,?,?)', (email,hash,addr,songs))
			self.conn.commit()
			return True
		return False

	def add_view(self, song_id):
		self.c.execute('SELECT views FROM songs WHERE id=?', (song_id,))
		views = self.c.fetchone()
		if views:
			v = views[0]
			v += 1
			self.c.execute('UPDATE songs SET views=? WHERE id=?', (v,song_id))
			self.conn.commit()

	def delete_song(self, song_id, email):
		self.c.execute('SELECT * FROM songs WHERE id=?', (song_id,))
		if self.c.fetchone():
			self.c.execute('SELECT user FROM songs WHERE id=?', (song_id,))
			user = self.c.fetchone()[0]
			if user == email:
				self.c.execute('DELETE FROM songs WHERE id=?',(song_id,))
				songs = self.get_song_ids(email)
				songs.remove(song_id)
				update = ''.join([s + '|' for s in songs])
				self.c.execute('UPDATE users SET songs=? WHERE email=?', (update,email))
				self.conn.commit()
			else:
				return False
			return True
		return None

	def add_song(self, email, title, art, id):
		self.c.execute('SELECT * FROM users WHERE email=?',(email,))
		x=self.c.fetchone()
		if x:
			cur=x[-1]
			cur += '{}|'.format(id)
			views = 0
			date = str(datetime.datetime.now())[:16]
			self.c.execute('UPDATE users SET songs=? WHERE email=?', (cur,email))
			self.c.execute('INSERT INTO songs values (?,?,?,?,?,?)', (id,title,date,views,art,email))
			self.conn.commit()

	def get_song_details(self, id):
		self.c.execute('SELECT * FROM songs WHERE id=?',(id,))
		try:
			id, title, date, views, art, user = self.c.fetchone()
			return {'id': id, 'title': title, 'date': date, 'views': views, 'art': art}
		except:
			pass

	def get_song_user(self, id):
		self.c.execute('SELECT * FROM songs WHERE id=?',(id,))
		try:
			id, title, date, views, art, user = self.c.fetchone()
			return user
		except:
			pass

	def get_song_ids(self,email):
		self.c.execute('SELECT songs FROM users WHERE email=?',(email,))
		x=self.c.fetchone()[0]
		songs = (x.split('|'))
		del songs[-1]
		return songs
		#return marshal.loads(x[-1])

	def delete(self,email):
		self.c.execute('SELECT * FROM users WHERE email=?', (email,))
		if self.c.fetchone():
			self.c.execute('DELETE FROM users WHERE email=?',(email,))
			self.conn.commit()

	def check(self, email, hash):
		self.c.execute('SELECT * FROM users WHERE email=?',(email,))
		x=self.c.fetchone()
		if not x:
			return False
		return hash == x[1]

	def get_song(self,uid):
		self.c.execute('SELECT * FROM users')
		x=self.c.fetchall()
		for i in x:
			songs=marshal.loads(i[3])
			for s in songs:
				if str(s['uid']) == str(uid):
					return (s['title'],s['file'])
		return ()


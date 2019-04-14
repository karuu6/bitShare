import hashlib
from random import randint

def _hash(msg):
	m=msg.encode()
	h=hashlib.sha256()
	h.update(m)
	return h.hexdigest()

def get_id(r=True, l=16):
	charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
	return ''.join([charset[randint(0, len(charset)-1)] for i in range(l)])

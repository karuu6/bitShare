import requests

class API:
	def __init__(self,secret):
		self.base   = 'https://api.crypto-loot.com'
		self.secret = secret
		self.s      = requests.Session()

	def checkbal(self,addr):
		u=self.base+'/user/balance?secret={}&name={}'.format(self.secret,addr)
		return self.s.get(u).json()['balance']
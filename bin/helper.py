class idOrigDict(object):

	def __init__(self):
		self.orig2id={}
		self.id2orig={}
		self.id=0

	def add(self,orig):
#		print("dict: %r"%orig)
		if not orig in self.orig2id.keys():
			self.orig2id[orig]=self.id
			self.id2orig[self.id]=orig
			self.id+=1
		print self.orig2id
		return self.getId(orig)
	
	def getOrig(self,id):
		return self.id2orig[id]

	def getId(self,orig):
		return self.orig2id[orig]

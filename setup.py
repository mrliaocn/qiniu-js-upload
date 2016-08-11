#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import commands
from qiniu import Auth
import qiniu.config

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=4001, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
			(r"/token", TokenHandler)
		]
		settings = {
			"template_path"	: os.path.join(os.path.dirname(__file__), "templates"),
			"static_path"	: os.path.join(os.path.dirname(__file__), "static"),
			"debug"			: True,
		}
		tornado.web.Application.__init__(self, handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class TokenHandler(tornado.web.RequestHandler):

	def get(self):

		access_key = 'YOUR_ACCESS_KEY'
		secret_key = 'YOUR_SECRET_KEY'

		q = Auth(access_key, secret_key)

		bucket_name = 'YOUR_BUCKET_NAME'
		
		# to set the uploaded file rename to YYYYMMDD_HHMMSS_filename
		# if the filename was "test.jpg", then the new filename will be "20160101_083054_test.jpg"
		# SEE MORE: http://developer.qiniu.com/article/kodo/kodo-developer/up/vars.html#magicvar
		policy = {"saveKey": "$(year)$(mon)$(day)_$(hour)$(min)$(sec)_$(fname)"}


		# in the source of qiniu/auth.py, the function upload_token takes 5 arguments:
		#	 bucket：your bucket_name
		#		key: the filename you want to set, None means set as ths "saveKey" above
		#	expires: expires time (second)
		#	 policy: the options to upload,see more: http://developer.qiniu.com/article/developer/security/put-policy.html
		#
		# def upload_token(self, bucket, key=None, expires=3600, policy=None, strict_policy=True):

		token = q.upload_token(bucket_name, None, 3600, policy)

		# return as json
		self.write(json.dumps({"uptoken":token}))



# 入口函数		
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
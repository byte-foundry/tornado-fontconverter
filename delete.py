import tornado, tornado.web
import boto, boto.s3
import os
from boto.s3.connection import S3Connection
from bucket import Bucket

class Delete(tornado.web.RequestHandler):
	def post(self):
		deletedpath = self.get_argument("deletedpath")
		conn = S3Connection(os.environ['ACCESS_KEY'], os.environ['SECRET_KEY'])
		bucket = conn.get_bucket('allfonts')
		try:
			bucketListResultSet = bucket.list(prefix=deletedpath)
			result = bucket.delete_keys([key.name for key in bucketListResultSet])
		except:
			raise tornado.web.HTTPError(404, 'Not Found')

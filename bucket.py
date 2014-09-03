import tornado, tornado.web
import os, uuid, glob, shutil
import fontforge, re
import boto, boto.s3
from boto.s3.connection import S3Connection
from upload import Upload

exts = '.woff', '.ttf', '.otf', '.svg', '.eot'

class Bucket(tornado.web.RequestHandler):
	@staticmethod
	def send_to_bucket(bucket, path, localpath, match, filename):
		try:
			for root, dirs, files in os.walk(localpath):
				for name in files:
					if (name.endswith(match)):
						full_key_name = os.path.join(path, name)
						k = bucket.new_key(name)
						k.key = full_key_name
						k.set_contents_from_filename(filename + name)
		except:
			raise tornado.web.HTTPError(404, 'Not Found')
		shutil.rmtree(localpath)

	def post(self):
		format = self.get_argument("format")
		path = self.get_argument("s3path")
		res = Upload.build_files(self.request.files['filearg2'][0])
		conn = S3Connection(ACCESS_KEY,SECRET_KEY)
		bucket = conn.get_bucket('allfonts')
		bucket.set_acl('private')
		if (format == 'all'):
			Upload.css_generator(res[0], res[1], 'prototypo')
			Upload.fontpack_generator(res[2])
			match = exts + ('.afm', '.css')
			filepath = res[0] + '/' + res[1] + '/'
			self.send_to_bucket(bucket, path, res[0], match, filepath)
		else:
			if ('.' + format) in exts:
				Upload.font_converter(res[2], format)
				self.send_to_bucket(bucket, path, res[0], format, res[0] + '/' + res[1] + '/')

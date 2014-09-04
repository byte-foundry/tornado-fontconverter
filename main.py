import tornado, tornado.ioloop, tornado.web
import os, uuid, glob, shutil
import fontforge, re, zipfile
from userform import Userform
from upload import Upload
from bucket import Bucket
from delete import Delete
#from unittestfont import *
# uncomment if you want to do unit tests

application = tornado.web.Application([
	(r"/", Userform),
	(r"/upload", Upload),
	(r"/bucket", Bucket),
	(r"/delete", Delete),
	], debug=True)

if __name__ == "__main__":
	#unittest.main() 
	# uncomment if you want to do unit tests
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()

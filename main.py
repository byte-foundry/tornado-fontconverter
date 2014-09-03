import tornado, tornado.ioloop, tornado.web
import os, uuid, glob, shutil
import fontforge, re, zipfile
from userform import Userform
from upload import Upload
from bucket import Bucket

application = tornado.web.Application([
	(r"/", Userform),
	(r"/upload", Upload),
	(r"/bucket", Bucket),
	], debug=True)

if __name__ == "__main__":
	application.listen(8888)
	#unittest.main()
	tornado.ioloop.IOLoop.instance().start()

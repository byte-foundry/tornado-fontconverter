import tornado, tornado.ioloop, tornado.web
import os, uuid, glob, shutil
import fontforge, re, zipfile

EXTS = [".woff", ".ttf", ".otf", ".svg", ".eot"]

class Userform(tornado.web.RequestHandler):
	def get(self):
		self.render("fileuploadform.html")

class Upload(tornado.web.RequestHandler):
	@staticmethod
	def cssGenerator(root, name, fullname):
		cssFile = root + '/' + name + '/' + name + ".css"
		template = "@font-face {\
			\n\tfont-family: '" + fullname + "';\
			\n\tsrc: url('" + name + ".eot');\
			\n\tsrc: url('" + name + ".eot?#iefix') format('embedded-opentype'),\
			\n\turl('" + name + ".woff') format('woff'),\
			\n\turl('" + name + ".ttf') format('truetype'),\
			\n\turl('" + name + ".svg#ywftsvg') format('svg');\
			\n\tfont-style: normal;\
			\n\tfont-weight: normal;\
			\n}\n\n"
		open(cssFile, 'w+').writelines(template)

	@staticmethod
	def fontGenerator(filename):
		#exts = ["woff", "ttf", "otf", "svg", "eot"]
		name = os.path.splitext(filename)[0]
		'''if not os.path.exists(name):
			os.makedirs(name)'''

		font = fontforge.open(filename)
		fullname = font.fullname

		for ext in EXTS:
			f = name + ext
			if (ext == '.otf'):
				#font.close()
				font2 = fontforge.open(filename)
				font2.selection.all()
				font2.autoHint()
				font2.generate(f)
				#font2.close()
			else:
				font.generate(f)
		font.close()

	@staticmethod
	def zipdir(root, path):
		zf = zipfile.ZipFile(path + '.zip', mode ='w')
		for file in glob.glob(path + '/*'):
			zf.write(file)
		zf.close()

	def post(self):
		fileinfo = self.request.files['filearg'][0]
		fname = fileinfo['filename']
		extn = os.path.splitext(fname)[1]
		cname = str(uuid.uuid4()) + extn
		zname = os.path.splitext(fname)[0]
		rname = os.path.splitext(cname)[0]
		os.makedirs(rname)
		os.makedirs(rname + '/'+ zname)
		with open(rname + '/' + zname + '/' + cname, 'w+') as f:
		    f.write(fileinfo['body'])
		os.rename(rname + '/' + zname + '/' + cname, rname + '/' + zname + '/' + fname)

		'''
		zname is default
		extn is .svg
		fname is default.sv
		cname is random name, file's name in the server
		rname is the random name without extension
		'''

		self.cssGenerator(rname, zname, 'prototypo')
		self.fontGenerator(rname + '/' + zname + '/'+ fname)
		os.chdir(rname)
		os.rename(zname + '/' + zname + '.ttf', zname + '/' + 'tmp.ttf');
		os.system('ttfautohint ' + zname + '/' + 'tmp.ttf ' + zname + '/' + zname + '.ttf');
		os.unlink(zname + '/' + 'tmp.ttf')
		self.zipdir(rname, zname)
		os.chdir('..')
		try:
			fd = open(rname + '/' + zname + '.zip', 'r')
			self.set_header ('Content-Type', 'application/zip')
			self.set_header ('Content-Disposition', 'attachment; filename='+ zname + '.zip')
			self.write(fd.read())
			fd.close()
		except:
			raise tornado.web.HTTPError(404, 'Invalid archive')
		shutil.rmtree(rname)


application = tornado.web.Application([
	(r"/", Userform),
	(r"/upload", Upload),
	], debug=True)

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()

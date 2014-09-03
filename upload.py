import tornado, tornado.ioloop, tornado.web
import os, uuid, glob, shutil
import fontforge, re, zipfile
#from fontunittest import *

exts = '.woff', '.ttf', '.otf', '.svg', '.eot'

class Upload(tornado.web.RequestHandler):
	@staticmethod
	def css_generator(root, name, fullname):
		cssfile = root + '/' + name + '/' + name + ".css"
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
		open(cssfile, 'w+').writelines(template)
		with open(cssfile, 'r') as content:
			csscontent = content.read()
		return (csscontent)

	@staticmethod
	def font_converter(filename, format):
		f = os.path.splitext(filename)[0] + '.' + format
		font = fontforge.open(filename)
		font.selection.all()
		font.autoHint()
		font.generate(f)
		font.close()

	@staticmethod
	def fontpack_generator(filename):
		#exts = ["woff", "ttf", "otf", "svg", "eot"]
		name = os.path.splitext(filename)[0]
		'''if not os.path.exists(name):
			os.makedirs(name)'''

		font = fontforge.open(filename)

		for ext in exts:
			f = name + ext
			font = fontforge.open(filename)
			font.selection.all()
			font.autoHint()
			font.generate(f)
		font.close()

	@staticmethod
	def zipdir(root, path):
		zf = zipfile.ZipFile(path + '.zip', mode ='w')
		for file in glob.glob(path + '/*'):
			zf.write(file)
		zf.close()

	@staticmethod
	def build_files(fileinfo):
		fname = fileinfo['filename']
		extn = os.path.splitext(fname)[1]
		cname = str(uuid.uuid4()) + extn
		zname = os.path.splitext(fname)[0]
		rname = os.path.splitext(cname)[0]
		file_path = rname + '/' + zname + '/' + fname
		zip_path = rname + '/' + zname + '.zip'
		os.makedirs(rname)
		os.makedirs(rname + '/'+ zname)
		with open(rname + '/' + zname + '/' + cname, 'w+') as f:
		    f.write(fileinfo['body'])
		os.rename(rname + '/' + zname + '/' + cname, rname + '/' + zname + '/' + fname)

		'''
		if fileinfo['filename'] is default.svg:
			zname is default
			extn is .svg
			fname is default.svg
			cname is random name, file's name in the server
			rname is the random name without extension
			file_path is the path to file
			zip_path is the path to zip
		'''
		return rname, zname, file_path, zip_path

	#VM can't find ttfautohint package -> unused method for now
	@staticmethod
	def ttf_auto_hint(args):
		os.rename(args[1] + '/' + args[1] + '.ttf', args[1] + '/' + 'tmp.ttf');
		os.system('ttfautohint ' + args[1] + '/' + 'tmp.ttf ' + args[1] + '/' + args[1] + '.ttf');
		os.unlink(args[1] + '/' + 'tmp.ttf')

	def post(self):
		format = self.get_argument("format")
		res = self.build_files(self.request.files['filearg1'][0])
		if (format == 'all'):

			'''
			res[0] is random name without extension
			res[1] is zip archive's name without extension
			res[2] is path of svg file
			res[3] is path of archive
			'''

			self.css_generator(res[0], res[1], 'prototypo')
			self.fontpack_generator(res[2])
			os.chdir(res[0])
			#self.ttf_auto_hint(res)
			self.zipdir(res[0], res[1])
			os.chdir('..')
			try:
				fd = open(res[3], 'r')
				self.set_header ('Content-Type', 'application/zip')
				self.set_header ('Content-Disposition', 'attachment; filename='+ res[1] + '.zip')
				self.write(fd.read())
				fd.close()
			except:
				raise tornado.web.HTTPError(404, 'Invalid archive')
		else:
			if ('.' + format) in exts:
				self.font_converter(res[2], format)
				try:
					to_send = res[0] + '/' + res[1] + '/' + res[1] + '.' + format
					fd = open(to_send, 'r')
					self.set_header('Content-Type', 'application/x-font-' + format)
					self.set_header('Content-Disposition', 'attachment; filename=' + res[1] + '.' + format)
					self.write(fd.read())
					fd.close()
				except:
					raise tornado.web.HTTPError(404, 'Invalid format token')
		shutil.rmtree(res[0])

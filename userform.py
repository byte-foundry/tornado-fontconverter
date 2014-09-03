import tornado, tornado.web

class Userform(tornado.web.RequestHandler):
	def get(self):
		self.render("fileuploadform2.html")

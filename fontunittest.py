import unittest, mimetypes
from pyfontconv import *

EXT = ["woff", "ttf", "otf", "svg", "eot"]

def test_type(type):
	for ext in EXT:
		mimetypes.add_type('application/xfont-' + ext, '.' + ext, True)
	return (mimetypes.guess_extension(type, True))

class TestFontConvFunctions(unittest.TestCase):
	def setUp(self):
		self.fileinfo = {"body":"", "filename":"" }
		with open('testfont/testfont.svg', 'r') as content:
			self.fileinfo['body'] = content.read()
			self.fileinfo['filename'] = content.name

	def test_svgtype(self):
		self.assertEqual(mimetypes.guess_type(self.fileinfo['filename'])[0], 'image/svg+xml')

	def test_css_generator(self):
		template = "@font-face {\
			\n\tfont-family: '" + 'prototypo' + "';\
			\n\tsrc: url('" + 'testfont' + ".eot');\
			\n\tsrc: url('" + 'testfont' + ".eot?#iefix') format('embedded-opentype'),\
			\n\turl('" + 'testfont' + ".woff') format('woff'),\
			\n\turl('" + 'testfont' + ".ttf') format('truetype'),\
			\n\turl('" + 'testfont' + ".svg#ywftsvg') format('svg');\
			\n\tfont-style: normal;\
			\n\tfont-weight: normal;\
			\n}\n\n"
		self.assertEqual(Upload.css_generator('/home/bill', 'testfont', 'prototypo'), template)

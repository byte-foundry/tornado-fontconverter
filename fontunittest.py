import unittest, mimetypes
from pyfontconv import *

EXT = ["woff", "ttf", "otf", "svg", "eot"]

def test_type(type):
	for ext in EXT:
		mimetypes.add_type('application/xfont-' + ext, '.' + ext, True)
	return (mimetypes.guess_extension(type, True))

class TestFontConvFunctions(unittest.TestCase):
	def setUp(self):
		self.fileinfo = {"body":"", "filename":"", "format":"" }
		with open('testfont/testfont.svg', 'r') as content:
			self.fileinfo['body'] = content.read()
			self.fileinfo['filename'] = content.name
			self.fileinfo['format'] = 'otf'
		content.close()

	def test_svgtype(self):
		'''TEST: Checking SVG File'''
		self.assertEqual(mimetypes.guess_type(self.fileinfo['filename'])[0], 'image/svg+xml')

	def test_svg_size(self):
		'''TEST : Checking whether svg file isn't empty'''
		self.assertGreater(os.stat(self.fileinfo['filename']).st_size, 0)

	def test_css_generator(self):
		'''TEST: Checking CSS File'''
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

	def test_font_converter(self):
		'''TEST: Checking converted font file'''
		self.assertTrue(Upload.font_converter(self.fileinfo['filename'], self.fileinfo['format']))

	def test_fontpack_generator(self):
		'''TEST : Checking font-pack'''
		self.assertTrue(Upload.fontpack_generator(self.fileinfo['filename']))

	def test_zipfile(self):
		'''TEST : Checking zip archive'''
		self.assertTrue(Upload.zipdir('testfont', 'testfont'))

	def test_ziptype(self):
		'''TEST: Checking zip archive type'''
		self.assertEqual(mimetypes.guess_type('testfont.zip')[0], 'application/zip')

	def test_count_files(self):
		'''TEST : Checking zip archive completion'''
		self.assertEqual(Upload.count_files('testfont'), 7)

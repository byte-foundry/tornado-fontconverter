import unittest, mimetypes, os, sys
import boto, boto.s3
from boto.s3.connection import S3Connection
from upload import Upload
from bucket import Bucket
from delete import Delete

EXT = ["woff", "ttf", "otf", "svg", "eot"]
exts = '.woff', '.ttf', '.otf', '.svg', '.eot'

def test_type(type):
	for ext in EXT:
		mimetypes.add_type('application/xfont-' + ext, '.' + ext, True)
	return (mimetypes.guess_extension(type, True))

class TestFunctions(unittest.TestCase):
	if (sys.argv[-1] != '-v'):
		print 'Run with -v option if you want to activate verbose mode'
	def setUp(self):
		self.fileinfo = {"body":"", "filename":"", "format":"" }
		with open('testfont/testfont.svg', 'r+') as content:
			self.fileinfo['body'] = content.read()
			self.fileinfo['filename'] = content.name
			self.fileinfo['format'] = 'otf'
		content.close()
		self.conn = S3Connection(os.environ['ACCESS_KEY'], os.environ['SECRET_KEY'])
		self.path = 'test1/test2/test3/'
		self.testBucket = self.conn.create_bucket('testbucket-prototypo')
		self.testBucket.set_acl('private')
		
	def test_sendtobucket_onefont(self):
		'''TEST : Checking S3 Bucket data sending - one font'''
		self.assertTrue(Bucket.send_to_bucket(self.testBucket, 'test1/test2/test3/', 'testfont/', '.ttf', 'testfont/'))

	def test_sendtobucket_allfonts(self):
		'''TEST : Checking S3 Bucket data sending - all fonts'''
		match = exts + ('.afm', '.css')
		self.assertTrue(Bucket.send_to_bucket(self.testBucket, 'test11/test22/test33/', 'testfont/', match, 'testfont/'))

	def test_deletebucket_first(self):
		'''TEST : Checking S3 Bucket data deletion'''
		self.assertTrue(Delete.delete_from_bucket('test1/test2/test3/'))

	def test_deletebucket_second(self):
		'''TEST : Checking S3 Bucket data deletion'''
		self.assertTrue(Delete.delete_from_bucket('test11/test22/test33/'))

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
		self.assertEqual(Upload.css_generator('.', 'testfont', 'prototypo'), template)

	def test_font_converter(self):
		'''TEST: Checking converted font file'''
		self.assertTrue(Upload.font_converter(self.fileinfo['filename'], self.fileinfo['format']))

	def test_fontpack_generator(self):
		'''TEST : Checking font-pack'''
		self.assertTrue(Upload.fontpack_generator(self.fileinfo['filename']))

	def test_zipfile(self):
		'''TEST : Checking zip archive'''
		self.assertTrue(Upload.zipdir('testfont'))
	
	def test_count_files(self):
		'''TEST : Checking zip archive completion'''
		self.assertEqual(Upload.count_files('testfont/'), 7)
	
	def test_svgtype(self):
		'''TEST: Checking SVG File'''
		self.assertEqual(mimetypes.guess_type(self.fileinfo['filename'])[0], 'image/svg+xml')

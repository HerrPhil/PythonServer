import sys, logging, requests, zipfile

from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		logger.info('path is ' + self.path)

		if self.path == '/remote/log.zip':
			self.doRemote()
		else:
			logger.info('do default get')
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'file server is running')
	
	def doRemote(self):
		logger.info('do remote get')
		logger.info('remote path is ' + self.path)

		self.send_response(200)
		self.send_header("Content-Length","183")
		self.send_header("Content-type","application/zip")
		self.end_headers()

		reqfile = '/Development/PythonServer/remote/log.zip'
		f = open(reqfile, 'rb')
		self.wfile.write(f.read())
		f.close()
		
	def do_POST(self):
		logger.info('start POSTing')
		content_length = int(self.headers['Content-Length'])

		logger.info('read content')
		body = self.rfile.read(content_length)
		bodydecode = body.decode("utf-8")
		self.send_response(200)
		self.end_headers()

		logger.info(body)
		logger.info(bodydecode)

		logger.info('get the archive')
		rlog = requests.get(bodydecode)

		logger.info('is the get archive successful')
		logger.info(rlog.status_code == requests.codes.ok)

		logger.info('get the zip in memory')
		zlog = zipfile.ZipFile(BytesIO(rlog.content))

		logger.info('extract the zip from memory to local')
		zlog.extractall("/Development/PythonServer/local")

		logger.info('close connections')
		zlog.close()
		rlog.close()

		logger.info('done extract')


httpd = HTTPServer(('localhost', int(sys.argv[1])), SimpleHTTPRequestHandler)
httpd.serve_forever()

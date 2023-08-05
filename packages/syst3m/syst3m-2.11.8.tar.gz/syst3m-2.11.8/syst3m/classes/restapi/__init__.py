
# imports
from syst3m.classes.config import *
from syst3m.classes.color import color
from syst3m.classes import defaults, objects
import urllib

# the restapi over ssh object class.
class RestAPI(objects.Object):
	def __init__(self, 
		# the root domain (optional).
		domain=None,
		# the api key added to every request data (optional).
		api_key=None,
	):
		
		# defaults.
		objects.Object.__init__(self, traceback="ssht00ls.restapi")
		
		# attributes.
		self.domain = domain
		self.api_key = api_key

		#
	def request(self, url="/", data={}, json=True):
		def clean_url(url, strip_first=True, strip_last=True, remove_double_slash=True):
			while True:
				if strip_last and url[len(url)-1] == "/": url = url[:-1]
				elif strip_first and url[0] == "/": url = url[1:]
				elif remove_double_slash and "//" in url: url = url.replace("//","/")
				else: break
			return url
		def encode_data(data):
			return f"?{urllib.parse.urlencode(data)}"
			#

		# url.
		if self.api_key != None:
			data["api_key"] = self.api_key
		if self.domain != None:
			url = f"https://{clean_url(self.domain)}/{clean_url(url)}/"
		else:
			url = f"https://{clean_url(url)}/"
		if data != {}: url += encode_data(data)

		# request.
		response_object = requests.get(url, allow_redirects=True)
		if response_object.status_code != 200:
			return r3sponse.error(f"Invalid request ({url}) [{response_object.status_code}]: {response_object.text}")
		if json:
			try: response = r3sponse.ResponseObject(json=output)
			except Exception as e: 
				if loader != None: loader.stop(success=False)
				return r3sponse.error(f"Unable to serialize output: {response_object}.")
			return response
		return response_object

# initialized object.
restapi = RestAPI()
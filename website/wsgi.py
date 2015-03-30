from app.core.http import Request


class Index(Request):
	def get(self):
		self.to_html('index.html.jade')


from webapp2 import WSGIApplication

app = WSGIApplication([
	('/', Index)
], debug=True)

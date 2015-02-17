from HTMLParser import HTMLParser



#supporint files
class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def save_html(file_name, html_string):
	with open(file_name + ".html", "w") as f:
		f.write(html_string.encode('utf8'))

from flask import Flask
import myhero_story, json
app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello world!"

@app.route('/getAllStory')
def return_all_story():
#	print json.dumps(myhero_story.get_story_type_description())
	return json.dumps(myhero_story.get_story_type_description())

if __name__ == "__main__":
	app.run(host='0.0.0.0')

from flask import Flask
import myhero_story, json
app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello world!"

@app.route('/getAllStory')
def return_all_story():
	return json.dumps(myhero_story.get_story_type_description())

@app.route('/storyList/<story_category>')
def return_story_in_category(story_category):
	return json.dumps(myhero_story.get_story_in_type(story_category))

@app.route('/story/<story_link>')
def return_story_content(story_link):
	return json.dumps(myhero_story.get_story_content(story_link))

if __name__ == "__main__":
	app.run(host='0.0.0.0')

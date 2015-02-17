from flask import Flask
import myhero_story, myhero_art, json
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

@app.route('/getArtMedium')
def return_art_medium():
	return json.dumps(myhero_art.get_art_medium_list())

if __name__ == "__main__":
	app.run(host='0.0.0.0')

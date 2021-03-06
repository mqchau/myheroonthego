from flask import Flask
import myhero_story, myhero_art, myhero_film, json
from pymongo import MongoClient

client = MongoClient()

app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello world!"

#----GROUP OF STORIES-----
@app.route('/getAllStory')
def return_all_story():
	return json.dumps(myhero_story.get_story_type_description())

@app.route('/storyList/<story_category>')
def return_story_in_category(story_category):
	return json.dumps(myhero_story.get_story_in_type(story_category))

@app.route('/story/<story_link>')
def return_story_content(story_link):
	return json.dumps(myhero_story.get_story_content(story_link))

#----GROUP OF ART--------
@app.route('/getArtMedium')
def return_art_medium():
	return json.dumps(myhero_art.get_art_medium_list())

@app.route('/artList/<art_category>/<page_num>')
def return_art_list(art_category, page_num=1):
	return json.dumps(myhero_art.get_art_list(art_category, page_num))

@app.route('/art/<art_key>')
def return_artwork(art_key):
	return json.dumps(myhero_art.get_artwork(art_key))

#-----GROUP OF MOVIE----
@app.route('/getAllMovie')
def return_movie_list():
	return json.dumps(trim_objectid_list(list(client.db.movie_list.find())))

@app.route('/movie/<movie_key>')
def return_movie(movie_key):
	return json.dumps(trim_objectid(dict(client.db.movie_list.find({'movielink': movie_key})[0])))

if __name__ == "__main__":
	app.run(host='0.0.0.0')

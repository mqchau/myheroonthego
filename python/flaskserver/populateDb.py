from pymongo import MongoClient
from myhero_story import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":
    client = MongoClient()

    #find out what collection is in here
    current_collections = client.db.collection_names()
    print "Here are the current collections"
    pp.pprint( current_collections )
    
    #list all collection to repopulate
    collection_to_populate = []
    collection_to_populate.append('story_category')
    collection_to_populate.append('story_list')

    #delete the collections that we're repopulating
    for one_collection in collection_to_populate:
            if one_collection in current_collections:
                client.db[one_collection].drop()
                print 'remove collection ' + one_collection

    #start populating the collections, one by one

    #story categories
    if 'story_category' in collection_to_populate:
        all_story_category = get_story_type_description()
        story_category_db = client.db.story_category
        story_category_db.insert(all_story_category)
        print "populated list of story category"

    #story list
    if 'story_list' in collection_to_populate:
        all_story_category = list(client.db.story_category.find())
        for one_category in all_story_category:
            story_tag = one_category['tag']
            story_in_category = get_story_in_type(story_tag)
            data_to_store = {
                    "tag" : story_tag,
                    "stories" : story_in_category
                    }
            try:
                client.db.story_list.insert(data_to_store)
            except Exception as e:
                pp.pprint(story_in_category)
                print "ERROR: " + str(e)
            print "got all stories in type " + one_category['type']



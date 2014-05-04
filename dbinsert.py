import json
import pymongo
import pprint

"""
After inserting example.osm.json with mongoimport to database
Here we want to retrive data
For each function we retrive diffrent part of data
"""

def get_db(db_name):
    '''
    Return db from mongodob
    '''
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db
def create_index(db):
    '''
    Create geo index on  pos filed of our database  
    '''
    db.boston.ensure_index([('pos',pymongo.GEO2D)])

def get_resturant(db):
    '''
    Find name of all restaurants and print their name and their cuisine
    '''
    print "name of all restaurants and print their name and their cuisine : "
    print_stars()
    cur=db.boston.find({"amenity":"restaurant"},{"name":1, "cuisine" :1,"_id":0})
    print_result(cur)
    
def get_amenity(db):
    '''
    Find distinct values of amenity
    '''
    print "Distinct values of amenity : "
    print_stars()
    cur=db.boston.find({"amenity":{"$exists":1}},{"amenity":1,"_id":0}).distinct("amenity")
    print_result(cur)

def count_amenity(db):
    '''
    Count number of each amenity
    First look if amenity exists in dataset then group by amenity values

    '''
    print "Count number of each amenity : "
    print_stars()
    cur=db.boston.aggregate([{"$match":{"amenity":{"$exists":1}}},{"$group":{"_id": "$amenity", "count":{"$sum":1}}}])     
    pprint.pprint(cur)
    print_stars()

def get_cafe_name_address(db):
    '''
    Get address of cafe
    '''
    print "Cafe names and their address :"
    print_stars()
    cur=db.boston.find({"address":{"$exists":1},"amenity":"cafe"},{"address":1,"name":1,"_id":0})
    print_result(cur)

def find_near_by(db):
    '''
    Find type and name of amenities are near by Harvard University Fine Arts Library
    '''
    print 'Find type and name of amenities are near by Harvard University Fine Arts Library: ' 
    print_stars()
    cur=db.boston.find({"pos":{"$near":[42.3738824,-71.1140051]},"amenity":{"$exists":1},"name":{"$exists":1}},{"name":1,"amenity":1,"_id":0})
    print_result(cur)   

def print_result(cur):
    '''
    Print result of query 
    '''
    for elem in cur:
        print  elem
        print
    print_stars()
    
def print_stars():
    print '****************************************'
    
    
    
if __name__ == "__main__":

    db = get_db('map')
    create_index(db)
    get_resturant(db)
    get_amenity(db)
    count_amenity(db)
    get_cafe_name_address(db)
    find_near_by(db)


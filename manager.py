
'''
Run all data cleaning and create example.osm.json
'''
if __name__ == "__main__":

    import mapparser
    import tags
    import users
    import audit
    import data
    mapparser.test();
    tags.test();
    users.test();
    audit.test();
    data.test();

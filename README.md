MongodbProject
==============
Project Summery:
Gathered from open street map, which collected from  http://www.openstreetmap.org/export#map=16/42.3739/-71.1051 
As example.osm . Please read direction below to how to use this project folder. 

 

Direction 
      Where to start?
Please find out manager.py and run this code. By running manager.py, a json file will be created in the directory called example.osm.json. After that I used command below
mongoimport -d map -c boston --file example.osm.json
to import my data to dabase called map and collection named boston
After that there is a file called dbinsert.py  which contains mongodb queries
     What is size of example.osm in this project?
               It is 4.4 MB
     What problems I faced working with this dataset?
                 I needed to convert dataset from
<node id="257489574" visible="true" version="3" changeset="16874014" timestamp="2013-07-08T13:51:19Z" user="Manu1400" uid="181135" lat="42.3744821" lon="-71.1040915">
  <tag k="address" v="1493 Cambridge Street, Cambridge, MA"/>
  <tag k="amenity" v="hospital"/>
  <tag k="attribution" v="Office of Geographic and Environmental    Information (MassGIS), Commonwealth of Massachusetts Executive Office of Environmental Affairs"/>
  <tag k="emergency" v="yes"/>
  <tag k="emergency_room" v="yes"/>
  <tag k="massgis:id" v="69"/>
  <tag k="name" v="Cambridge Health Alliance-Cambridge Hospital"/>
  <tag k="short_name" v="Cambridge Hospital"/>
  <tag k="source_url" v="http://mass.gov/mgis/hospitals.htm"/>
 </node>


To following json format


{    "amenity": "hospital", 
    "attribution": "Office of Geographic and Environmental Information (MassGIS), Commonwealth of Massachusetts Executive Office of Environmental Affairs", 
    "created": {
        "changeset": "16874014", 
        "timestamp": "2013-07-08T13:51:19Z", 
        "uid": "181135", 
        "user": "Manu1400", 
        "version": "3"
    }, 
    "emergency": "yes", 
    "emergency_room": "yes", 
    "id": "257489574", 
    "massgis:id": "69", 
    "name": "Cambridge Health Alliance-Cambridge Hospital", 
    "pos": [
        42.3744821, 
        -71.1040915
    ], 
    "short_name": "Cambridge Hospital", 
    "source_url": "http://mass.gov/mgis/hospitals.htm", 
    "type": "node", 
    "visible": "true" }
    
    
    



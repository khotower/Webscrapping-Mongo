from flask import Flask,render_template,request,redirect
app = Flask(__name__)
import pymongo
import config
import json
import scrape_mars
try:
    mongo = pymongo.MongoClient(host=config.host, port=config.mongo_port, serverSelectionTimeoutMS=1000)
    # mongo.server_info()
    db =mongo.mars_scrap

except:
    print("ERROR - Can't Connect to the MongoDB ")

@app.route("/scrape",methods=['GET','POST'])
def scrape():
    try:
        to_mongo =scrape_mars.scrape()
        # dbResponse = db.mars.insert_one(to_mongo)
        # collection = db["mars"]
        dbResponse = db.mars.update({"_id":"mars_record"},{"$set":to_mongo},upsert=True)
        print(dbResponse)
        return redirect('/')
    except Exception as ex:
        print("##############")
        print(ex)
        print("##############")

@app.route("/",methods=['GET','POST'])
def Mars_data_to_display():
    try:
        if request.method == 'POST':
            return redirect('/scrape')
        from_mongo = db.mars.find_one({"_id": "mars_record"})
        Mars_News =from_mongo['Mars_News']
        Mars_facts = from_mongo['Mars_facts']
        Mars_hemisphere = from_mongo['Mars_hemisphere']
        Featured_Image = from_mongo['Featured_Image']
        # print(Featured_Image)
        return render_template("index.html",Mars_News=Mars_News,Mars_facts=Mars_facts,Mars_hemisphere=Mars_hemisphere,Featured_Image=Featured_Image)
    except Exception as ex:
        print("##############")
        print(ex)
        print("##############")

if __name__ == "__main__":
    app.run(port=config.port,debug=True)
#Dependencies
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

#Initialize Flask and Mongo
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#Create Redirect Route
@app.route("/")
def home():
    mars_info = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars_info)

#Create Scraper
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.mars.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
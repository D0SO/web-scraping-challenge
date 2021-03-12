from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

# Create the route that will render our scrape function in an html template
@app.route("/")
def index():
    # Find one data record from our databse
    mars = mongo.db.mars.find_one()
    # return rendered page
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    # Initiate Scraping of Mars Data
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    # Store data in the collection
    mars.update({}, mars_data, upsert=True)

    # Return to main page to review scraping results
    return redirect("/")


if __name__ == "__main__":
    app.run()

import flask
import logging
import config
import geocoder
import requests
from flask import request


###
# Globals
###
app = flask.Flask(__name__)

CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY  # Should allow using session variables


GOOGLE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&keyword={}&key={}"\
    .format(CONFIG.START_LAT,CONFIG.START_LONG, CONFIG.RADIUS, CONFIG.SEARCH, CONFIG.GOOGLE_API_KEY)


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    flask.g.search = CONFIG.SEARCH
    flask.g.radius = CONFIG.RADIUS
    return flask.render_template('showmap.html')


@app.route("/setup")
def makeMyMap():
    location = {"lat": CONFIG.START_LAT, "lng": CONFIG.START_LONG}
    return flask.jsonify(results=location)


@app.route("/clicked")
def get_address():
    app.logger.debug("Got a JSON request")
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    address = geocoder.google([lat, lng], method="reverse")
    add_dict = {'address': address.json['address']}
    return flask.jsonify(results=add_dict)


@app.route("/places")
def get_place():
    places = requests.get(GOOGLE_URL)
    return flask.jsonify(results=places.json()['results'])


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert not True  # I want to invoke the debugger
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


####

if __name__ == "__main__":
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
    app.logger.info(
            "Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

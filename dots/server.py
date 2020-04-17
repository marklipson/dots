from flask import Flask, request, jsonify
from dots.data import Data
import os
import json

WEB_FOLDER = os.path.join(os.path.dirname(__file__), "../web")
everything = Data("dots_data.json")
app = Flask("dots", static_url_path="", static_folder=WEB_FOLDER)


@app.route('/run/<name>', methods=["get"])
def check_in(name: str=None):
    # parse data from user
    user_data = json.loads(request.args.get("data") or "{}")
    # store user's data
    everything[name] = user_data
    # return information about everyone
    out = everything.load()
    return jsonify(out)


if __name__ == '__main__':
    app.run(port=11122, debug=True)

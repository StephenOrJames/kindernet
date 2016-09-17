import json
import os
import re
import urllib.parse
import urllib.request

from flask import (
    Flask,
    jsonify,
    render_template,
    request
)
from flask_sqlalchemy import SQLAlchemy

from replacements import REPLACEMENTS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
MIN_SCORE = .6  # The minimum sentiment score to be considered positive


class Conversion(db.Model):
    __tablename__ = "conversions"

    src = db.Column(db.String, nullable=False, primary_key=True)
    dest = db.Column(db.String, nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def api():
    src = request.form.get("src", None)
    if src is None:
        return jsonify(status="error")

    # TODO: slugify src when loading from or storing to db
    conversion = Conversion.query.filter_by(src=src).first()
    if not conversion:
        dest = convert(src)
        conversion = Conversion(src=src, dest=dest)
        db.session.add(conversion)
        db.session.commit()

    return jsonify(status="success", text=conversion.dest)


def convert(original):
    score = get_score(original)

    if score > MIN_SCORE:
        return original  # positive enough

    for word in original.split():
        if word in REPLACEMENTS:
            modified, changes = re.subn(r"(\s)%s(\s)" % word, r"\1%s\2" % REPLACEMENTS[word], original, count=1)
            if changes and get_score(modified) > MIN_SCORE:
                return modified

    return ""


def get_score(text):
    """Get the sentiment score for the specified text."""

    microsoft_key = os.environ.get("MICROSOFT_TEXT_ANALYTICS_KEY", None)
    if microsoft_key is None:
        raise Exception("Please specify MICROSOFT_TEXT_ANALYTICS_KEY.")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": microsoft_key,
        "User-Agent": "Kindernet-server (BigRed//Hacks project)"
    }
    body = {
        "documents": [
            {
                "language": "en",
                "id": "1",
                "text": text
            }
        ]
    }

    req = urllib.request.Request(
        "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment",
        json.dumps(body).encode("UTF-8"),
        headers,
        method="POST"
    )

    with urllib.request.urlopen(req) as response:
        data = response.read().decode("UTF-8")

    return json.loads(data)["documents"][0]["score"]


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

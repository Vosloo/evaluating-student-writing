import sys
from typing import Union

from werkzeug.datastructures import FileStorage

from flask import Flask, render_template, request

sys.path.append("../")
# import pipeline to process text

app = Flask(__name__)


def process_text(text: str) -> str:
    return text


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    if request.method == "POST":
        text: Union[None, str] = None

        if "text" in request.form and request.form["text"] != "":
            text = request.form["text"]
        elif "file" in request.files:
            file: FileStorage = request.files["file"]
            text = file.read().decode("utf-8")

        if text:
            processed_text = process_text(text)
            return render_template("output.html", processed_text=processed_text)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

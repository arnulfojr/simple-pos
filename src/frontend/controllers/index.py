
from flask import render_template

from .. import app


@app.route('/', methods=['GET'])
def render_index():
    return render_template('index.html')


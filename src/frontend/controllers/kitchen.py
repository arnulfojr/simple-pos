
from flask import render_template

from .. import app


@app.route('/kitchen/', methods=['GET'])
def render_kitchen_view():
    return render_template('')


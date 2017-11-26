
from flask import render_template

from .. import app


@app.route('/sale/', methods=['GET'])
def render_pos():
    return render_template('transactions/sale.html')



from flask import render_template

from .. import app


@app.route('/products/', methods=['GET'])
def render_products():
    return render_template('products/browse.html')


@app.route('/products/add/', methods=['GET'])
def render_product_form():
    return render_template('products/form.html', heading=u"Add a new product", edit=False)


@app.route('/products/edit/<uuid:code>/', methods=['GET'])
def render_product_form_as_edit(code):
    return render_template('products/form.html', heading=u"Edit", edit=True, code=code)


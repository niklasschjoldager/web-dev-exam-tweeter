from bottle import error, jinja2_template as template

############################################################
@error(404)
def _(error):
    return template("fourOhFour.html")

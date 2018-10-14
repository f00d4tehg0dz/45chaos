from flask import render_template, request, send_file
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    if request.path.endswith(".JPG"):
        return send_file("static/img/unknown.JPG")
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

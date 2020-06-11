from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
from flask import render_template
from flask_restful import reqparse
import display
from datetime import datetime
import requests


server_settings = config('webconfig.ini', 'Server')

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["{0} per minute".format(server_settings['rate_limit_minute']), "{0} per second".format(server_settings['rate_limit_second'])]
)

title = config('webconfig.ini', 'Static')['title']


@app.before_request
def limit_remote_addr():
    if request.remote_addr != server_settings['allow_ip']:
        abort(403)  # Forbidden


@app.route('/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def welcome():
    return render_template('welcome.html'), 200


@app.route('/getcredential', methods=['GET'])
def get_credential():
    parser = reqparse.RequestParser(trim=True)
    parser.add_argument('id', action='append', required=True)

    path = config('webconfig.ini', 'Image')['path']
    args = parser.parse_args()

    img_paths = list()
    for id in args.id:
        image_path_jpg = '{0}/{1}.jpg'.format(path, id)
        image_path_png = '{0}/{1}.png'.format(path, id)
        r_jpg = requests.get(image_path_jpg).status_code
        r_png = requests.get(image_path_png).status_code

        if r_jpg == 200:
            img_paths.append(image_path_jpg)
        elif r_png == 200:
            img_paths.append(image_path_png)
        else:
            img_paths.append("/static/src/img/nobody.jpg")


    display.show_credential(img_paths)

    return jsonify(200)


@app.route('/showcredential', methods=['GET'])
def credential():
    parser = reqparse.RequestParser(trim=True)
    parser.add_argument('image', action='append', required=True)

    args = parser.parse_args()

    return render_template('display_credential.html',
                           page_title=title,
                           images=args.image,)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(429)
def too_many_requests(e):
    # note that we set the 429 status explicitly
    return render_template('429.html'), 429


@app.errorhandler(400)
def too_many_requests(e):
    # note that we set the 400 status explicitly
    return render_template('400.html'), 400


if __name__ == '__main__':
    app.run(host=server_settings['bind_ip'], port=server_settings['port'])


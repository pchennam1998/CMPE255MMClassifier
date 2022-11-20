import os
import json
from flask import Flask
from flask import redirect, url_for, jsonify, render_template, request
from pandas import DataFrame
import sys

from Models.myTFInference import TFInference



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if __name__ == '__name__':
        app.run(debug=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
   
    # Initialize TFInference
    model = TFInference()

    # PEOPLE_FOLDER = os.path.join('static', 'images')
    # app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

    @app.route('/', methods=['POST', 'GET'])
    def index():

        if request.method == 'GET':
            return render_template('home.html')
        
        elif request.method == 'POST':
            url = request.form['url']
            class_name, confidence = model.main(url)
            return render_template('home.html', class_name=class_name, confidence=confidence)

        # if request.method == 'GET':
        #     return render_template('home.html')
        # elif request.method == 'POST':
        #     url = request.form['n']
        #     class_name, confidence = model.main(url)
        #     return render_template('home.html', class_name=class_name, confidence=confidence)

    return app
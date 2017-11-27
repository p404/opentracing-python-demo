# -*- coding: utf-8 -*-
# pylint: disable=C0103

from flask import Flask, request, render_template, redirect, url_for
import requests
import opentracing
import logging
import re
from jaeger_client import Config
from flask_opentracing import FlaskTracer

app = Flask(__name__)

config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
    },
    service_name='cybermonday',
)
opentracing_tracer = config.initialize_tracer()
tracer = FlaskTracer(opentracing_tracer)

@app.route('/', methods=['GET'])
@tracer.trace()
def index():
    return 'this is index'

@app.route('/login', methods=['POST', 'GET'])
@tracer.trace()
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        span = tracer.get_span()
        email = request.form['email']
        password = request.form['password']
        
        child_span = opentracing_tracer.start_span("validate_email", child_of=span)
        validate_email(email)
        child_span.finish()

        headers = inject_as_headers(opentracing_tracer, span)
        r = requests.post('http://127.0.0.1:5001/auth', json={"email": email, "password": password}, headers=headers)
        if r.status_code == 200:
            return redirect(url_for('index'))
        else:
            return 'login error'

def inject_as_headers(tracer, span):
    text_carrier = {}
    tracer.inject(span.context, opentracing.Format.TEXT_MAP, text_carrier)
    return text_carrier

def validate_email(email):
    email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    if email_regex.match(email):
        return True
    else:
        return False

if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
    app.run(debug=True, port=5000)

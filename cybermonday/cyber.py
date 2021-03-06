# -*- coding: utf-8 -*-
# pylint: disable=C0103

from flask import Flask, request, render_template, redirect, url_for, flash, session
import requests
import opentracing
import logging
import re
from jaeger_client import Config
from flask_opentracing import FlaskTracer

app = Flask(__name__)
app.secret_key = "super secret key"

config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'local_agent': {
            'reporting_host': "jaeger-agent",
            'reporting_port': 5775,
        },
        'logging': True,
    },
    service_name='cybermonday',
)
opentracing_tracer = config.initialize_tracer()
tracer = FlaskTracer(opentracing_tracer)

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

@app.route('/', methods=['GET'])
@tracer.trace()
def index():
    return render_template('index.html')

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
        r = requests.post('http://app_auth:5001/auth', json={"email": email, "password": password}, headers=headers)
        if r.status_code == 200:
            flash("Login successfully")
            return redirect(url_for('index'))
        else:
            return 'login error'

if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
    app.run(debug=True, port=5000, host='0.0.0.0')

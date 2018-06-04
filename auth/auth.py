# -*- coding: utf-8 -*-
# pylint: disable=C0103

from flask import Flask, Response, request 
from flask_sqlalchemy import SQLAlchemy
import opentracing
import logging
import sqlalchemy_opentracing
from jaeger_client import Config
from flask_opentracing import FlaskTracer
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:s3cureauth@db_auth:5432/auth'
db = SQLAlchemy(app)
engine = db.engine
Session = sessionmaker(bind=engine)

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
    service_name='auth',
)
opentracing_tracer = config.initialize_tracer()
tracer = FlaskTracer(opentracing_tracer)
sqlalchemy_opentracing.init_tracing(opentracing_tracer)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)


@app.route('/auth', methods=['POST'])
@tracer.trace()
def login():
    if request.method == 'POST':
        logging.info("Request headers: {}".format(request.headers))

        span = tracer.get_span()
        payload = request.get_json()
        email = payload['email']
        password = payload['password']

        sp = opentracing_tracer.start_span('query', child_of=span)
        session = Session()
        sqlalchemy_opentracing.set_parent_span(session, sp)
        user = session.query(Users).filter_by(email = email).first()
        sp.finish()
        if user is None:
            return Response(status=404, mimetype='application/json')
        elif user.password == password:
            return Response(status=200, mimetype='application/json')
        else:
            return Response(status=401, mimetype='application/json')
   
if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
    app.run(debug=True, port=5001, host='0.0.0.0')
    opentracing_tracer.close()

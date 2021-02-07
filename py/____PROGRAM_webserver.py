#!/usr/bin/env python3

import ____PROGRAM_lib 
import logging
import os
import argparse

from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import DecimalField, RadioField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_bad'

class ActionForm(FlaskForm):
    lval = DecimalField('lval', validators=[DataRequired()])
    rval = DecimalField('rval', validators=[DataRequired()])
    action = RadioField('action', choices=[('add','add'),('sub','subtract')])
    submit = SubmitField('submit')


@app.route('/', methods=['GET', 'POST'])
def render():
    form = ActionForm()
    if form.validate_on_submit():
        fcn = ____PROGRAM_lib.add if form.action == 'add' else ____PROGRAM_lib.sub
        return 'result: %lf' % fcn(float(form.data['lval']), float(form.data['rval']))
    else:
        return render_template('form.html', title='Math Operation', form=form)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='____PROGRAM_webserver')
    parser.add_argument('-p', '--port', required=False, type=int, help='port to listen to ', default=5000)
    parser.add_argument('-a', '--host', required=False, type=str, help='address to listen on ', default='0.0.0.0')
    parser.add_argument('-v', '--verbose', default=False, action="store_true",
                        help="print details")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO if not args.verbose else logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    logging.info('starting up!')


    # this is used for CSRF and other related security matters
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        logging.warn('Using random key for forms!')
        SECRET_KEY = os.urandom(24)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.run(port=args.port, host=args.host)


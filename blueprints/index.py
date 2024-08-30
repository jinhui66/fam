from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
import os
import time

bp = Blueprint('index',__name__,url_prefix="/")

@bp.route('/welcome',methods=['GET','POST'])
def welcome():
    return render_template('welcome.html')

@bp.route('/test',methods=['GET','POST'])
def test():
    return render_template('test.html')

@bp.route('/user_in',methods=['GET','POST'])
def user_in():
    return render_template('user_in.html')

@bp.route('/user_out',methods=['GET','POST'])
def user_out():
    return render_template('user_out.html')

@bp.route('/get_family',methods=['GET','POST'])
def get_family():
    return render_template('get_family.html')

@bp.route('/families',methods=['GET','POST'])
def families():
    return render_template('families.html')

import re
from flask import Flask, render_template, jsonify, request,redirect
import os
from werkzeug.utils import secure_filename

import sys
from argparse import ArgumentParser
from os.path import basename
import subprocess as sp
import convert_single_image as a
import classes
import tensorflow as tf
from classes.inference.Sampler import *

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
# import BeautifulSoup4
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

app.config["IMAGE_UPLOADS"]= "E:/TOT NGHIEP/THESIS/thesisLanUyen2021/static/images/uploads" 
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["MAX_IMAGE_FILESIZE"] = 2 * 2048 * 2048

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def readfileconvert(fileconvert):
    with open(fileconvert, "r") as f:
        content = f.read()
    return content

@app.route('/', methods=["GET","POST"])
#page = function
def index():
    if request.method == 'GET':
        return(render_template('index.html'))

    if request.method == "POST":        
        if request.files:
            if not allowed_image_filesize(request.cookies["filesize"]):
                print("Filesize exceeded maximum limit")
                return redirect(request.url)
            image = request.files["image"]
            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                if filename.find('.png') == -1:
                    ext = filename.rsplit(".", 1)[0]                    
                    filename = ext +'.png'
                    print(filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))     
            print("Image saved")

            #  if not os.path.exists(output_folder):
            # os.makedirs(output_folder)           
            sampler = Sampler(model_json_path='model/model_json.json',
                     model_weights_path = 'model/weights.h5')
            sampler.convert_single_image('static/output', png_path='static/images/uploads/' + filename, print_generated_output=1, get_sentence_bleu=0, original_gui_filepath=None, style='default')

            ext = filename.rsplit(".", 1)[0]
            fileconvert = 'static/output/' + ext +'.html'

            return render_template('index.html', filename = filename, fileconvert = fileconvert, ext = ext,result = readfileconvert(fileconvert))


if __name__=="__main__":
    app.run(debug =True)
import enum
from flask import Flask, jsonify, render_template
from flask_cors import CORS, cross_origin
from sklearn.cluster import KMeans
import random
from datetime import datetime
import csv
from numpy.core.numeric import moveaxis
import pandas as pd
import numpy as np
import json
from datetime import datetime
from flask import request
from random import randint
from sklearn.neighbors import KernelDensity
from sklearn.utils.extmath import density

# declare constants
HOST = "localhost"
PORT = 5000

# initialize flask application
app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
# app.config["CORS_HEADERS"] = "Content-Type"

# sample hello world page
@app.route("/")
def hello():
    return "<h1>python api</h1>"


def route_cipher(plainText, n=4, init_position=0, clockwise=True):
    plainText = preprocesar_texto(plainText)

    direction = 0
    move_list = CircularLinkedList()
    if clockwise:
        move_list.push((0, 1))
        move_list.push((-1, 0))
        move_list.push((0, -1))
        move_list.push((1, 0))
        if init_position % 2 == 0:
            direction = 0
        else:
            direction = 1
    else:
        move_list.push((-1, 0))
        move_list.push((0, 1))
        move_list.push((1, 0))
        move_list.push((0, -1))
        if init_position % 2 == 0:
            direction = 1
        else:
            direction = 0

    itr = move_list.head
    for i in range(init_position):
        itr = itr.next

    block = []
    i = 0
    newLine = []
    for c in plainText:
        if i == n:
            block.append(newLine)
            newLine = []
            i = 0
        newLine.append(c)
        i += 1
    block.append(newLine)

    while len(block[len(block) - 1]) < n:
        block[len(block) - 1].append("X")

    for row in block:
        print(row)

    cipherText = ""

    lim_w = len(block[0])
    lim_h = len(block)

    if init_position == 0:
        start_i = 0
        start_j = lim_w - 1
    elif init_position == 1:
        start_i = lim_h - 1
        start_j = lim_w - 1
    elif init_position == 2:
        start_i = lim_h - 1
        start_j = 0
    elif init_position == 3:
        start_i = 0
        start_j = 0

    w_iter = lim_w
    h_iter = lim_h

    i = start_i
    j = start_j

    while w_iter > 0 and h_iter > 0:
        moves = 0
        if direction % 2 == 0:
            while moves < h_iter:
                cipherText += block[i][j]
                i += itr.data[0]
                j += itr.data[1]
                moves += 1
            i -= itr.data[0]
            j -= itr.data[1]
            w_iter -= 1
        else:
            while moves < w_iter:
                cipherText += block[i][j]
                i += itr.data[0]
                j += itr.data[1]
                moves += 1
            i -= itr.data[0]
            j -= itr.data[1]
            h_iter -= 1
        itr = itr.next
        i += itr.data[0]
        j += itr.data[1]
        direction += 1

    return cipherText


def route_decipher(cipherText, n=4, init_position=0, clockwise=True):
    cipherText = preprocesar_texto(cipherText)
    decipherText = cipherText

    direction = -1
    move_list = CircularLinkedList()
    if clockwise:
        move_list.push((0, 1))
        move_list.push((-1, 0))
        move_list.push((0, -1))
        move_list.push((1, 0))
        if init_position % 2 == 0:
            direction = 0
        else:
            direction = 1
    else:
        move_list.push((-1, 0))
        move_list.push((0, 1))
        move_list.push((1, 0))
        move_list.push((0, -1))
        if init_position % 2 == 0:
            direction = 1
        else:
            direction = 0

    itr = move_list.head
    for i in range(init_position):
        itr = itr.next

    decipherBlock = []
    rows = len(decipherText) // n
    for i in range(rows):
        blockLine = []
        for i in range(n):
            blockLine.append("0")
        decipherBlock.append(blockLine)
    if len(decipherText) % n > 0:
        decipherBlock.append(blockLine)

    lim_w = len(decipherBlock[0])
    lim_h = len(decipherBlock)

    if init_position == 0:
        start_i = 0
        start_j = lim_w - 1
    elif init_position == 1:
        start_i = lim_h - 1
        start_j = lim_w - 1
    elif init_position == 2:
        start_i = lim_h - 1
        start_j = 0
    elif init_position == 3:
        start_i = 0
        start_j = 0

    w_iter = lim_w
    h_iter = lim_h

    i = start_i
    j = start_j

    c = 0

    while w_iter > 0 and h_iter > 0:
        moves = 0
        if direction % 2 == 0:
            while moves < h_iter:
                decipherBlock[i][j] = decipherText[c]
                i += itr.data[0]
                j += itr.data[1]
                moves += 1
                c += 1
            i -= itr.data[0]
            j -= itr.data[1]
            w_iter -= 1
        else:
            while moves < w_iter:
                decipherBlock[i][j] = decipherText[c]
                i += itr.data[0]
                j += itr.data[1]
                moves += 1
                c += 1
            i -= itr.data[0]
            j -= itr.data[1]
            h_iter -= 1
        itr = itr.next
        i += itr.data[0]
        j += itr.data[1]
        direction += 1

    decipherText = ""
    for i in range(lim_h):
        for j in range(lim_w):
            decipherText += decipherBlock[i][j]
    return decipherText


@app.route("/api/encrypt", methods=["GET", "POST"])
@cross_origin()
def encrypt():
    parameters = request.get_json()
    print(parameters)
    block = parameters["block"]
    text = parameters["text"]
    path = parameters["path"]
    position = parameters["position"]

    # plainText = "enteryourmessage"
    # cipherText = route_cipher(text, n=5, clockwise=False, init_position=3)
    # decipherText = route_decipher(cipherText, n=5, clockwise=False, init_position=3)
    return jsonify(parameters)


@app.route("/api/decrypt", methods=["GET", "POST"])
@cross_origin()
def decrypt():
    parameters = request.get_json()
    print(parameters)
    block = parameters["block"]
    text = parameters["text"]
    path = parameters["path"]
    position = parameters["position"]
    # plainText = "enteryourmessage"
    # cipherText = route_cipher(plainText, n=5, clockwise=False, init_position=3)
    # decipherText = route_decipher(cipherText, n=5, clockwise=False, init_position=3)
    return jsonify(parameters)


if __name__ == "__main__":
    app.run(host=HOST, debug=True, port=PORT)

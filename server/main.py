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


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def push(self, data):
        ptr1 = Node(data)
        temp = self.head

        ptr1.next = self.head

        if self.head is not None:
            while temp.next != self.head:
                temp = temp.next
            temp.next = ptr1

        else:
            ptr1.next = ptr1

        self.head = ptr1

    def printList(self):
        temp = self.head
        if self.head is not None:
            while True:
                print(temp.data, end=" ")
                temp = temp.next
                if temp == self.head:
                    break


def eliminar_tilde(texto):
    tilde_table = str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU", "´")
    return texto.translate(tilde_table)


def a_mayuscula(texto):
    return texto.upper()


def remove_punctuation(texto):
    return "".join(c for c in texto if c.isalnum())


def preprocesar_texto(texto):
    texto = eliminar_tilde(texto)
    texto = a_mayuscula(texto)
    texto = remove_punctuation(texto)
    return texto


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


def es_primo(num):
    if num > 1:
        for i in range(2, num // 2 + 1):
            if (num % i) == 0:
                return False
        return True
    else:
        return False


def serie_primos_cipher(idx_array):
    primes_idx = []
    temp = []
    for i in idx_array:
        if es_primo(i):
            primes_idx.append(i)
        else:
            temp.append(i)
    return primes_idx, temp


def serie_pares_cipher(idx_array):
    pares_idx = []
    temp = []

    for i in idx_array:
        if i % 2 == 0:
            pares_idx.append(i)
        else:
            temp.append(i)
    return pares_idx, temp


def serie_fibonacci_cipher(text):
    n = len(text)
    return []


def serie_primos_decipher(text):
    1


def transposicion_serie_cipher(plainText, series_mode=0):
    plainText = preprocesar_texto(plainText)
    text_idx = []
    for i in range(len(plainText)):
        text_idx.append(i)

    cipherText = ""
    cipher_idx = []
    if series_mode == 0:
        primes_idx, pares = serie_primos_cipher(text_idx)
        pares, other = serie_pares_cipher(pares)
        cipher_idx = primes_idx + pares + other

    else:
        fib_idx, pares = serie_fibonacci_cipher(plainText)
        pares, other = serie_fibonacci_cipher(pares)
        cipher_idx = fib_idx + pares + other

    for i in cipher_idx:
        cipherText += plainText[i]

    return cipherText


def transposicion_serie_decipher(cipherText, series_mode=0):
    cipherText = preprocesar_texto(cipherText)
    text_idx = []
    for i in range(len(cipherText)):
        text_idx.append(i)

    decipherText = []
    for i in range(len(cipherText)):
        decipherText.append(0)

    if series_mode == 0:
        primes_idx, pares = serie_primos_cipher(text_idx)
        pares, other = serie_pares_cipher(pares)
        cipher_idx = primes_idx + pares + other
    else:
        fib_idx, pares = serie_fibonacci_cipher(plainText)
        pares, other = serie_fibonacci_cipher(pares)
        cipher_idx = primes_idx + pares + other

    for i in range(len(cipher_idx)):
        decipherText[cipher_idx[i]] = cipherText[i]
    output = ""
    for c in decipherText:
        output += c
    return output


@app.route("/api/encrypt", methods=["GET", "POST"])
@cross_origin()
def encrypt():
    parameters = request.get_json()
    print(parameters)
    # return jsonify(parameters)
    block = int(parameters["block"])
    text = parameters["text"]
    path = parameters["path"]
    position = int(parameters["position"])

    clockwise = True if path == "clockwise" else False
    cipherText = route_cipher(
        text, n=block, clockwise=clockwise, init_position=position
    )
    ans = {}
    ans["cipherText"] = cipherText
    return jsonify(ans)


@app.route("/api/encrypt2", methods=["GET", "POST"])
@cross_origin()
def encrypt2():
    parameters = request.get_json()
    print(parameters)
    # return jsonify(parameters)
    text = parameters["text2"]
    mode = int(parameters["num"])

    cipherText = transposicion_serie_cipher(text, series_mode=mode)
    ans = {}
    ans["cipherText"] = cipherText
    return jsonify(ans)


@app.route("/api/decrypt", methods=["GET", "POST"])
@cross_origin()
def decrypt():
    parameters = request.get_json()
    print(parameters)

    block = int(parameters["block"])
    text = parameters["text"]
    path = parameters["path"]
    position = int(parameters["position"])

    clockwise = True if path == "clockwise" else False
    decipherText = route_decipher(
        text, n=block, clockwise=clockwise, init_position=position
    )
    ans = {}
    ans["decipherText"] = decipherText
    return jsonify(ans)


@app.route("/api/decrypt2", methods=["GET", "POST"])
@cross_origin()
def decrypt2():
    parameters = request.get_json()
    print(parameters)
    # return jsonify(parameters)
    text = parameters["text2"]
    mode = int(parameters["num"])

    decipherText = transposicion_serie_decipher(text, series_mode=mode)
    ans = {}
    ans["decipherText"] = decipherText
    return jsonify(ans)


if __name__ == "__main__":
    app.run(host=HOST, debug=True, port=PORT)

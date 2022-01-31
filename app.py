from flask import Flask, jsonify, send_from_directory
import webbrowser
from threading import Timer
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import os
import sys
from os import walk
from os.path import join
import yara
from coreLogic import *


app = Flask(__name__, static_url_path="")


@app.route("/")
def page():
    global ruleCnt, filesCnt
    ruleCnt = filesCnt = 0
    return send_from_directory("static", "index.html")


@app.route("/rule")
def rule():
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    global ruleCnt, rulePath
    try:
        rulePath = askopenfilename(
            parent=root, filetypes=[("YARA", "*.yar"), ("All", "*")]
        )
        ruleCnt = parseRule(rulePath)
        return jsonify({"rulePath": rulePath, "ruleCnt": str(ruleCnt) + " rules"})
    except:
        rulePath = ""
        ruleCnt = 0
        return jsonify({})


@app.route("/files")
def files():
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    global filesPath, filesCnt
    try:
        filesPath = askdirectory(parent=root)
        filesList = [os.path.join(filesPath, fn) for fn in next(os.walk(filesPath))[2]]
        filesCnt = len(filesList)
        return jsonify({"filesPath": filesPath, "filesCnt": str(filesCnt) + " files"})
    except:
        filesPath = ""
        filesCnt = 0
        return jsonify({})


@app.route("/draw")
def draw():
    if ruleCnt * filesCnt and ruleCnt != "invalid":
        filesList = [os.path.join(filesPath, fn) for fn in next(os.walk(filesPath))[2]]
        scanYARA(filesList)
        table = tableHTML(filesList)
        return jsonify({"draw": table})
    else:
        return jsonify({"draw": ""})


def open_browser():
    webbrowser.open_new_tab("http://localhost:4449")


if __name__ == "__main__":
    ruleCnt = filesCnt = 0
    rulePath = filesPath = yaraRule = ""
    rules = []
    Timer(1, open_browser).start()
    app.run("localhost", 4449)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
#Instances

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')  

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=puerto)
    app.run()
# -*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
from tools import Tools

app = Flask(__name__)
tools = Tools()

@app.route("/")
def _index():
    return render_template('index.html')

@app.route("/<ver>/tools")
def _tools(ver):
    q = request.args.get('q')
    res, comment, score = tools.response(q)

    data = {
        'q':q,
        'response':'「' + res + '！」' + comment,
        'score':score
        }

    return jsonify({
            'status':'OK',
            'data':data
        })

@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    return render_template('error.html', title='error', error_code=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

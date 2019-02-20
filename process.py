from flask import Flask, render_template, request, jsonify
from utils import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/results', methods=['POST'])
def results():
	text = request.form['keywords']
	if text:
		res = most_similarity_project(text)
		return res

	return jsonify({'error' : 'Missing data!'})

if __name__ == '__main__':
	app.run(debug=True)
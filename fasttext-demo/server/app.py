from flask import Flask, request, jsonify
from flask_cors import CORS
import fastText

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
  return "<h3>I am Groot.</h3>"

@app.route('/v1/detectlanguage', methods=['POST'])
def detect_language():
  if not request.json or not 'text' in request.json:
    return jsonify({'result': 'error'})

  result = fastText_predict(request.json['text'])
  return jsonify({'result': result})


def fastText_predict(text):
  model = fastText.load_model('lid.176.ftz')
  return model.predict(text)[0][0][-2:]

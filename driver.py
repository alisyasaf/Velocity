import numpy as np
import pickle
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 2)
    loaded_model = pickle.load(open("./model/model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        # reading_score = request.form['reading']
        # listening_score = request.form['listening']
        speaking_score = request.form['Speaking']
        writing_score = request.form['Writing']

        to_predict_list = list(map(float, [speaking_score, writing_score]))
        result = ValuePredictor(to_predict_list)

        if float(result) == 0:
            prediction = 'BASIC'
        elif float(result) == 1:
            prediction = 'INTERMEDIATE'
        elif float(result) == 2:
            prediction = 'ADVANCED'

        return render_template("result.html", prediction=prediction, name=name)
        


if __name__ == '__main__':
    app.run(debug=True)
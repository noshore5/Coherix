from flask import Flask, render_template, request

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from utils.wavelet_utils import pull_data, workflow, API_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        ticker1 = request.form['ticker1']
        ticker2 = request.form['ticker2']
        try:
            max_period = int(request.form['max_period'])
            min_period = int(request.form['min_period'])
            _,_,sig1,_ = pull_data(ticker1, API_KEY)
            _,_,sig2,_ = pull_data(ticker2, API_KEY)
            _,_,_,fig = workflow(sig1, sig2, (max_period, min_period))
            fig.savefig('static/output.png');  # Save the figure to a file
            result = 'output.png'
        except Exception as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
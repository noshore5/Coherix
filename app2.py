from flask import Flask, render_template_string, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from utils.wavelet_utils2 import pull_data, workflow

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Wavelet Coherence Dashboard</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .container { max-width: 700px; margin: auto; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input[type=text], input[type=number] { width: 100%; padding: 8px; }
        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .btn:hover { background: #0056b3; }
    </style>
</head>
<body>
<div class="container">
    <h2>Wavelet Coherence Analysis</h2>
    <form method="post">
        <div class="form-group">
            <label for="ticker1">Stock 1 Ticker:</label>
            <input type="text" id="ticker1" name="ticker1" value="{{ ticker1 }}">
        </div>
        <div class="form-group">
            <label for="ticker2">Stock 2 Ticker:</label>
            <input type="text" id="ticker2" name="ticker2" value="{{ ticker2 }}">
        </div>
        <div class="form-group">
            <label for="upper_bound">Max Period:</label>
            <input type="number" id="upper_bound" name="upper_bound" value="{{ upper_bound }}">
        </div>
        <div class="form-group">
            <label for="lower_bound">Min Period:</label>
            <input type="number" id="lower_bound" name="lower_bound" value="{{ lower_bound }}">
        </div>
        <div class="form-group">
            <label for="phase">Show Phase Arrows:</label>
            <input type="checkbox" id="phase" name="phase" {% if phase %}checked{% endif %}>
        </div>
        <button type="submit" class="btn">Run Analysis</button>
    </form>
    {% if plot_url %}
    <h3>Result:</h3>
    <img src="data:image/png;base64,{{ plot_url }}" style="width:100%;border:1px solid #ccc;">
    {% endif %}
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_url = None
    ticker1 = request.form.get('ticker1')
    ticker2 = request.form.get('ticker2')
    upper_bound = int(request.form.get('upper_bound', 125))
    lower_bound = int(request.form.get('lower_bound', 8))
    phase = 'phase' in request.form

    if request.method == 'POST':
        key = 'jjeryxeZXNkBhTEQF0SDj8uBBI_N1dBM'
        try:
            sig1 = pull_data(ticker1, key)[2]
            sig2 = pull_data(ticker2, key)[2]
            bounds = (upper_bound, lower_bound)
            _, _, _, fig = workflow(sig1, sig2, bounds, phase=phase, density=20)
            buf = io.BytesIO()
            #fig.savefig(buf, format='png')
            plt.show()
            buf.seek(0)
            plot_url = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
        except Exception as e:
            plot_url = None

    return render_template_string(TEMPLATE, ticker1=ticker1, ticker2=ticker2,
                                 upper_bound=upper_bound, lower_bound=lower_bound,
                                 phase=phase, plot_url=plot_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

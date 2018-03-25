from flask import Flask, render_template_string
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return render_template_string("""
    <html>
    <title>hello1</title>
    <body>Hello world 1 site
        <script type="text/javascript" src="static/client.js"></script>
	<script>
        </script>
    </body>
    </html>""")

app.run(debug=True, port=5000)

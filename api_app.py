from flask import Flask, Response
from flask import jsonify
from flask import request
from flask import render_template_string
from flask_cors import CORS, cross_origin
import random
import string

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello():
    return render_template_string("""
        <html><title>Add jobs</title>
        <body>
            Data: [import from path]
            Job: [combine name | rescheme]
        </body>
    """)

code_is_alive = """
        var running = setInterval(function() {
            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "http://localhost:5001/api/running/"+id, true);
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    console.log(this.response);
                    json_object = JSON.parse(this.response);
                    console.log(json_object);
                    if (json_object.status == 0) {
                        clearInterval(running);
                    }
                }
            }
            xhttp.send();
        }, 4000);
"""

@app.route("/api")
@cross_origin()
def api():
    return "This is the motherfucking api!"

@app.route("/api/running/<id>")
@cross_origin()
def is_running(id):
    print('Job '+id+'is running!');
    data = {
        'status': 1
    }
    json_data = jsonify(data)
    print(request);
    return json_data

@app.route("/api/running/<id>/false")
def false_id(id):
    data = {
        'status': 0
    }



@app.route("/api/sample1")
@cross_origin()
def sampleCode():
    r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(11)])

    data_text = 'bimal kant'
    unique_id = 'xdfzd'

    with open('static/'+r+'.js', 'w') as f:
        f.write(f"""
            console.log('this is a sample.js file');
            console.log('this is line 2 of file');
            data = "{data_text}";
            data_fixed = data.split(' ').join('');
            console.log(data_fixed);
            id = "{unique_id}";
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", "http://localhost:5001/api/postresult/"+id, true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("result="+data_fixed);
        \n"""+code_is_alive)

    data = {
        'id': 1,
        'url': 'http://localhost:5001/static/'+r+'.js',
        'name': 'Join user names'
    }
    json_data = jsonify(data)
    return json_data

@app.route('/api/postresult/<id>',methods=['POST'])
@cross_origin()
def result(id):
    data_result = request.form['result']
    print('result computed for : ', id)
    print(data_result)
    return 'hELO'

app.run(host='127.0.0.1',port=5001,debug=True)


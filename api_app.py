from flask import Flask, Response
from flask import jsonify
from flask import request
from flask import render_template_string
from split import Job, divideData, Pool
from flask_cors import CORS, cross_origin
from queue import Queue
import random
import string

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'this is the secreet key'

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
            data = {
                "data": data_fixed,
                "id": id
            }
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", "http://localhost:5001/pool", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("result="+data);
        \n"""+code_is_alive)

    data = {
        'id': 1,
        'url': 'http://localhost:5001/static/'+r+'.js',
        'name': 'Join user names'
    }
    json_data = jsonify(data)
    return json_data

# @app.route('/api/postresult/<id>',methods=['POST'])
# @cross_origin()
# def result(id):
    # data_result = request.form['result']
    # print('result computed for : ', id)
    # print(data_result)
    # return 'hELO'


job_queue = Queue()
current_job = None
job_hash = {}

@app.route('/job', methods=['POST'])
def add_job():
    request_body = request.get_json()
    print(request_body)
    job = Job(request_body['data'], request_body['code'])
    job_queue.put(job)
    job_hash[job.job_id] = job
    print(job)
    return jsonify({
        "message": "the job has been queued."
    })


# We do a more discrete division for the array elements
# for systems with Lesser Ram
@app.route('/pool', methods=['GET'])
@cross_origin()
def get_from_pool():
    global current_job
    global job_queue
    if not current_job or current_job.status == "complete":
        current_job = job_queue.get()
    try:
        partitioned_job = current_job.division.pool.getTopJob()
    except Exception as e:
        return jsonify({
            "message": "No more jobs in the pool",
        })

    r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(11)])

    import json
    data_text = json.dumps(partitioned_job['data'])
    unique_id = partitioned_job['id']
    code = partitioned_job['code']
    # data_text = 'suyash garg'
    # unique_id = r
    # code = """data_fixed = data.split(' ').join('');"""

    with open('static/'+r+'.js', 'w') as f:
        f.write(f"""
            console.log('this is a sample.js file');
            console.log('this is line 2 of file');
            data = JSON.parse('{data_text}');
            console.log(data);
            {code}
            console.log(data_fixed);
            id = "{unique_id}";
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", "http://localhost:5001/pool/"+id, true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("result="+data_fixed);
        \n"""+code_is_alive)

    data = {
        'id': unique_id,
        'url': 'http://localhost:5001/static/'+r+'.js',
        'name': 'Join user names'
    }
    json_data = jsonify(data)
    return json_data


@app.route('/pool/<id>', methods=['POST'])
@cross_origin()
def post_to_pool(id):
    data = request.form['result'].split(',')
    print(data)
    print(type(data))
    print(id)
    job_id = id.split(" - ")[0]
    sub_job_id = id.split(" - ")[1]
    print(job_id, sub_job_id)
    job_hash[job_id].add_result(data, sub_job_id)
    if job_hash[job_id].status == "complete":
        with open(f'{job_id}.csv', 'w') as f:
            for item in job_hash[job_id].finished_data:
                f.write(f"{item}\n")

    print(f"Completed stuff here! - Here is the result - {data}")
    return jsonify({"message": "Thanks for the result!"})


@app.route('/job', methods=['GET'])
@cross_origin()
def gandu_function():
    return jsonify({
        "message": "jab job khatam ho jaayegi to post kar denge?",
    })

app.run(host='127.0.0.1',port=5001,debug=True)

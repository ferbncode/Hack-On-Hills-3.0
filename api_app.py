from flask import Flask, Response
from flask import jsonify
from flask import request
from flask import render_template_string
from split import Job, divideData, Pool
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from queue import Queue
import requests
import random
import json
import string

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'this is the secreet key'
sio = SocketIO(app)

# active_connections = 
    # {'socketId': 'running/available'}
# 
active_connections = {}


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

@app.route("/api")
@cross_origin()
def api():
    return "This is the api!"

job_queue = Queue()
current_job = None
job_hash = {}

@app.route('/prejob', methods=['POST'])
def pre_job():
    request_body = request.get_json()
    print(request_body)
    if request_body['type'] == "filter":
        column = request_body["column"]
        criteria = request_body["criteria"]
        code = somewhere.generate_code(
            type="filter",
            column=column,
            criteria=critieria
        )
    r = requests.post('127.0.0.1:5001/job', data = {
        "data": request_body["data"],
        "code": request_body["code"],
    })

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
# @app.route('/pool', methods=['POST'])
# @cross_origin()
# <<<<<<< HEAD
# def post_to_pool():
    # data = request.get_json()
    # current_job.merge_results(data)
    # print(f"Completed stuff here! - Here is the result - {data}")

@sio.on('givemejob')
def job_from_pool(message):
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
            id = "{unique_id}";
	    postMessage({{id,data_fixed}});
        \n""")
    data = {
        'id': unique_id,
        'url': 'http://localhost:5001/static/'+r+'.js',
        'name': 'Join user names'
    }
    json_data = json.dumps(data)
    print('json data: ')
    print(json_data)
    emit('pool job', json_data)
    return ''

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
def end_function():
    return jsonify({
        "message": "jab job khatam ho jaayegi to post kar denge?",
    })

@sio.on('postingresult')
def result(message):
  print('getting result from socket')
  current_job.merge_results(message)
  print(f"Completed stuff here! - Here is the result - {message}")
  print(message)
  return ''

@sio.on('currentstatus')
def status_update(message):
  print(message)
  active_connections[request.sid] = "busy"
  return ''

@sio.on('connect')
def handle_con():
    active_connections[request.sid] = 'available'
    print(request.sid)

@sio.on('disconnect')
def handle_dis():
    active_connections.pop(request.sid)
    print('available connections: ')
    print(active_connections)
    print(request.sid, ' disconnected ...')

if __name__ == '__main__':
    sio.run(app,port=5001,debug=False)

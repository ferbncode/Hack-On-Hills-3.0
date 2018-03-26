from flask import Flask, Response, render_template, redirect
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

active_connections = {}
job_queue = Queue()
current_job = None
job_hash = {}


@app.route("/add", methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        data = []
        job_name = request.form['jobname']
        task_type = request.form['tasktype']
        if 'file' in request.files:
            file = request.files['file']
            for line in file.readlines():
                line = line.decode('utf-8').strip()
                data.append(line.split(','))
        criterias = None

        # add a job with the corresponding job type and criteria
        pre(task_type, data, job_name, criterias=criterias)
        return redirect('/list')
    return render_template('index.html')


def generate_code(op_type, criterias):
    """Note that the format of the data and criteria is as following:

    data = [[1, "Bimal", 3], [9, "Suyash", 1], [3, "Utkarsh", 1]]
    criteria = [{"col": "0", "operator": "<=", "value": "9", "typeval": "number"},
                {"col": "1", "operator": "==", "value": "Suyash", "typeval": "string"}]
    """
    if op_type == "filter":
        criterias = str(criterias);

        code = """ criterias = """ + criterias + """ ;
            data_fixed = data.filter(function(element) {
                let res = true;
                for (let criteria of criterias) {
                    let val =  element[Number(criteria["col"])];
                    let reqvalue = criteria["value"];
                    if (criteria["typeval"] == "number") {
                        reqvalue = Number(reqvalue);
                    }
                    let operator = (criteria["operator"]);
                    switch(operator) {
                        case "==":
                            res = (val === reqvalue);
                            break;
                        case ">=":
                            res = (val >= reqvalue);
                            break;
                        case "<=":
                            res = (val <= reqvalue);
                            break;
                        case "<":
                            res = (val < reqvalue);
                            break;
                        case ">":
                            res = (val > reqvalue);
                            break;
                    }
                    if (res === false) {
                        break;
                    }
                }
                return res;
            });
            console.log("Processed Data: ", data_fixed);
        """
    return code


def pre(op_type, data, job_name, criterias=None):
    if op_type == 'mergenames':
        code = """data_fixed = data.map(function(item, index) { return item.split(' ').join(''); });"""
        code = """data_fixed = data;"""
    if op_type == 'filterby':
        code = generate_code(
            op_type='filter',
            criterias=criterias,
        )
    custom_add_job(data, code, job_name)


@app.route('/prejob', methods=['POST'])
def pre_job():
    request_body = request.get_json()
    if request_body['op_type'] == "filter":
        criterias = request_body["criterias"]
        code = generate_code(
            op_type="filter",
            criterias=criterias
        )
    data = request_body["data"]
    name = request_body["name"]
    custom_add_job(data, code, name)
    return jsonify({"message": "job has been created"})


def custom_add_job(data, code, name):
    job = Job(data, code)
    job.name = name
    job_queue.put(job)
    job_hash[job.job_id] = job


@app.route('/job', methods=['POST'])
def job():
    request_body = request.get_json()
    job = Job(request_body['data'], request_body['code'])
    job.name = request_body['name']
    job_queue.put(job)
    job_hash[job.job_id] = job
    return jsonify({
        "message": "the job has been queued."
    })


@sio.on('givemejob')
def job_from_pool(message):
    import json
    global current_job
    global job_queue
    if not current_job or current_job.status == "complete":
        current_job = job_queue.get()
    try:
        partitioned_job = current_job.division.pool.getTopJob()
    except Exception as e:
        return json.dumps({
            "message": "No more jobs in the pool",
        })

    r = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(11)])
    data_text = json.dumps(partitioned_job['data'])
    unique_id = partitioned_job['id']
    code = partitioned_job['code']

    # This js file will contain the required code that runs on the user agent
    with open('static/'+r+'.js', 'w') as f:
        f.write(f"""
            console.log('this is a sample.js file');
            console.log('this is line 2 of file');
            data = JSON.parse('{data_text}');
            console.log(data);
            console.log(typeof(data));
            {code}
            console.log("duniya me sab ho, bug na ho");
            id = "{unique_id}";
            console.log(data_fixed);
	    postMessage({{id,data_fixed}});
        \n""")
    data = {
        'id': unique_id,
        'url': 'http://localhost:5001/static/'+r+'.js',
        'name': 'Join user names'
    }
    json_data = json.dumps(data)
    emit('pool job', json_data)
    return ''


@app.route('/pool/<id>', methods=['POST'])
@cross_origin()
def post_to_pool(id):
    data = request.form['data_fixed']
    id = request.form['id']
    job_id = id.split(" - ")[0]
    sub_job_id = id.split(" - ")[1]
    job_hash[job_id].add_result(data, sub_job_id)
    if job_hash[job_id].status == "complete":
        with open(f'{job_id}.csv', 'w') as f:
            for item in job_hash[job_id].finished_data:
                f.write(f"{item}\n")
    return jsonify({"message": "Thanks for the result!"})


@sio.on('postingresult')
def result(message):
  try:
      data = message['data_fixed']
      id = message['id']
      job_id = id.split(" - ")[0]
      sub_job_id = id.split(" - ")[1]
      job_hash[job_id].add_result(data, sub_job_id)
      if job_hash[job_id].status == "complete":
        with open(f'static/results/{job_id}.csv', 'w') as f:
          for item in job_hash[job_id].finished_data:
            f.write(f"{item}\n")
      return json.dumps({'status': 'success'})
  except Exception as error:
      print(error)
  return ''


@app.route('/list')
def getAlljobs():
    return render_template('list.html', job_hash=job_hash)


@sio.on('currentstatus')
def status_update(message):
  active_connections[request.sid] = "busy"


@sio.on('connect')
def handle_con():
    active_connections[request.sid] = 'available'


@sio.on('disconnect')
def handle_dis():
    active_connections.pop(request.sid)


if __name__ == '__main__':
    sio.run(app,port=5001,debug=False)

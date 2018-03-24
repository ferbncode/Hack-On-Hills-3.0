from flask import Flask, request, jsonify, make_response
from split import Job, divideData, Pool
from queue import Queue


app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is the secreet key'

job_queue = Queue()
current_job = None

@app.route('/job', methods=['POST'])
def add_job():
    request_body = request.get_json()
    print(request_body)
    job = Job(request_body['data'], request_body['code'])
    job_queue.put(job)
    print(job)
    return jsonify({
        "message": "the job has been queued."
    })

# We do a more discrete division for the array elements
# for systems with Lesser Ram
@app.route('/pool', methods=['GET'])
def get_from_pool():
    global current_job
    global job_queue
    if not current_job:
        current_job = job_queue.get()
    try:
        partitioned_job = current_job.division.pool.getTopJob()
    except Exception as e:
        return jsonify({
            "message": "No more jobs in the pool",
        })
    return jsonify(partitioned_job)


@app.route('/pool', methods=['POST'])
def post_to_pool():
    data = request.get_json()
    current_job.merge_results(data)
    print(f"Completed stuff here! - Here is the result - {data}")


@app.route('/job', methods=['GET'])
def gandu_function():
    return jsonify({
        "message": "jab job khatam ho jaayegi to post kar denge?",
    })


if __name__ == '__main__':
    app.run(debug=True)

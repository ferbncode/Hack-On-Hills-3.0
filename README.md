# Open Web Compute
Code for the awesome Hack on Hills 3.0. :)

Our idea is to leverage the resources of the millions of computers connected on the Internet. Any site that wants to support open source high computation tasks can simply add one line of code to their HTML and that will communicate with our API Server and transfer some payload to anyone who access the site (users of the site). The result of these small computations is then merged to present the final output which can be accessed via our API. Jobs which can be added are limitless. But presently, we focused only on data cleaning and filtering jobs.


## What problem are we trying to solve?

* Distributed computing of massive resource intensive jobs.
* Make it trivial to add new job which require computation.
* Deliver some payload and execute it via the web browser using spare CPU cycles.
* Provide a solution to open source applications that require massive computation, networking capabilities.

## Inspiration

* The Great Internet Mersenne Prime Search.
* A software any one can download, use spare cpu cycles in a coordinated way.
+ Cryptocurrenies being mined via web browsers.
* We do a similar task (several tasks) via the web browser.


## The Process

* A new job can be added via the REST api or the web interface.
* This job is divided into sub-jobs which are much smaller.
* When there is a request from a client then allocate a  sub-job from the pool based on device’s capabilities to this device.
* When all the sub-jobs of a job have been processed, the results are combined to get the final result.

## Why will sites allow us?

* This is essentially donating some CPU processing and network bandwidth.
* Web workers are used to run the payload in a background thread separate from
the main thread. So, the UI performance is not affected at all.
* They want to support open source large-scale data analysis projects.
* They have large user base which they can leverage for some application.
* We make it easy too -
```
  <script type=”text/javascript” src=”/openwebcompute.js”></script>.
```

## Managing Security Issues

* Security concerns are handled because running jobs can be openly queried from the API, everyone can see the code and the data it is working on.
* User job doesn’t directly add JS code, it is parsed by our application to generate the code. Adding new functionality would need a plugin like system.

## Follow Up

* Use RabbitMQ for queue of jobs and Redis for storing job and client information.
* Implement scheduling for getting jobs from pool.
* Setup FTP server to get data via ftp protocol.
* We made filterBy for demonstrating purpose. Some easy to add and useful functions would be - data cleaning tasks, aggregation (SUM, MIN, MAX), row wise data encryption, etc.
* Extend it for network intensive tasks like web scraping.

## Setup

* Make sure that you have following installed:
    * Python 3
    * Flask
    * Flask Socket IO (flask_socketio), Flask Cors (flask-cors)
    * Web Workers

* Run `python3 api_app.py` for running the main api server.
* Run `python3 example_site.py` for running the demo site which uses our api.
* Add a job as shown below (POST request to endpoints `/prejob` and `/job')
* View the list of all jobs by entering localhost:5001/list on your browser.
* Visit example site at localhost:5000. This will automatically fetch one job from the pool and execute it.
* Refresh the list page and one can download the result once, the job is complete.

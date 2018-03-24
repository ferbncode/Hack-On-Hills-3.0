from flask import Flask, render_template_string
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template_string("""
    <html>
    <title>hello1</title>
    <body>Hello world 1 site
        <script>
            console.log("calling the backend");
            let json_object;
            function loadFunc() {
                let xhttp = new XMLHttpRequest();
                xhttp.open('GET', 'http://localhost:5001/api/sample1', true);
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        console.log(this.response);
                        json_object = JSON.parse(this.response);
                        const name = json_object.name;
                        const url = json_object.url;

                        console.log('Running job for process: ', name);
                        var head = document.getElementsByTagName('head').item(0);
                        let script = document.createElement('script');
                        script.setAttribute('type','text/javascript');
                        script.setAttribute('src', url);
                        head.appendChild(script);
                    }
                };
                xhttp.send();
            }
            loadFunc();
        </script>
    </body>
    </html>""")

app.run(debug=True)

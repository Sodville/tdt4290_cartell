from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = False


@app.route("/liveness", methods=['GET'])
def home():
    return "OK"

app.run(host="0.0.0.0")

import req
import json
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='FCA')

@app.route("/")
def root():
	return render_template('index.html')

@app.route("/pesquisa")
def pesq():
	return render_template('pesquisar.html')

@app.route("/geral")
def call_class():
	geral = req.get_geral(str(request.args.get("marca")))
	return(json.dumps(geral))

@app.route("/regional")
def call_this():
	reg = req.get_val(int(request.args.get("periodo")), request.args.get("start"))
	return(json.dumps(reg))


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)

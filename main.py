from flask import Flask, request, jsonify
from attn import get_atten
import os

app = Flask(__name__)


@app.route('/atten', methods=["GET"])
def attendanceDet():
	reg_no = request.args.get("regNo")
	dob = request.args.get("dob")
	mobno = request.args.get("mobno")

	data = get_atten(reg_no, dob, mobno)
	return jsonify(**data)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.debug = True
	app.run(host='0.0.0.0', port=port)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://your_user:your_pass@your_host/your_db"
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    hwid = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, default=True)

@app.route("/new", methods=["POST"])
def create():
    info = request.get_json()
    k = str(uuid.uuid4())[:8]
    d = Data(key=k, hwid=info["hwid"])
    db.session.add(d)
    db.session.commit()
    return jsonify({"key": k, "status": "created"})

@app.route("/check", methods=["POST"])
def check():
    info = request.get_json()
    d = Data.query.filter_by(key=info["key"]).first()
    if not d or d.hwid != info["hwid"] or not d.status:
        return jsonify({"status": "invalid"})
    return jsonify({"status": "valid"})

@app.route("/remove/<k>", methods=["DELETE"])
def remove(k):
    d = Data.query.filter_by(key=k).first()
    if not d:
        return jsonify({"status": "not found"})
    db.session.delete(d)
    db.session.commit()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    app.run(debug=False)

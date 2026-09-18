import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Visit(db.Model):
    __tablename__ = "visits"
    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/hello", methods=["GET"])
def hello():
    visited_at = datetime.now()
    ip_address = request.remote_addr
    visit = Visit(visited_at=visited_at, ip_address=ip_address)
    db.session.add(visit)
    db.session.commit()
    return "Hello", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
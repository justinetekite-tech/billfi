import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE_URL = os.environ["DATABASE_URL"]
ADMIN_KEY = os.environ.get("ADMIN_KEY")

VIFURUSHI = [
    {"id": "saa1", "jina": "Saa 1", "bei": 500},
    {"id": "siku1", "jina": "Siku 1", "bei": 1500},
    {"id": "wiki1", "jina": "Wiki 1", "bei": 7000},
]

def db():
    return psycopg2.connect(DATABASE_URL)

def tengeneza_jedwali():
    with db() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vouchers (
                id SERIAL PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                kifurushi TEXT NOT NULL,
                imeuzwa BOOLEAN DEFAULT FALSE
            )""")

tengeneza_jedwali()

@app.route("/")
def nyumbani():
    return "Bill-Fi yangu inafanya kazi!"

@app.route("/vifurushi")
def vifurushi():
    return jsonify(VIFURUSHI)

@app.route("/stoku")
def stoku():
    with db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT kifurushi, COUNT(*) FROM vouchers
                       WHERE imeuzwa = FALSE GROUP BY kifurushi""")
        return jsonify({k: n for k, n in cur.fetchall()})

@app.route("/admin", methods=["GET", "POST"])
def admin():
    ujumbe = ""
    if request.method == "POST":
        if not ADMIN_KEY or request.form.get("key") != ADMIN_KEY:
            return "Nenosiri si sahihi", 403
        kifurushi = request.form["kifurushi"]
        codes = [c.strip() for c in request.form["codes"].splitlines() if c.strip()]
        with db() as conn, conn.cursor() as cur:
            for c in codes:
                cur.execute(
                    "INSERT INTO vouchers (code, kifurushi) VALUES (%s, %s) "
                    "ON CONFLICT (code) DO NOTHING", (c, kifurushi))
        ujumbe = f"Zimeongezwa: {len(codes)}"
    chaguo = "".join(f'<option value="{v["id"]}">{v["jina"]}</option>' for v in VIFURUSHI)
    return f"""<h3>Ongeza voucher</h3><p>{ujumbe}</p>
    <form method="post">
      <input name="key" type="password" placeholder="Nenosiri"><br><br>
      <select name="kifurushi">{chaguo}</select><br><br>
      <textarea name="codes" rows="8" cols="30" placeholder="Code moja kila mstari"></textarea><br><br>
      <button>Ongeza</button>
    </form>"""

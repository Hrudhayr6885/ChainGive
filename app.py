# ============================================================
# app.py  — PERSON 2's file
# Flask web server: connects the smart contract to the GUI
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
import smart_contract as contract

app = Flask(__name__)
app.secret_key = "charity_blockchain_secret_2024"   # needed for flash messages & session

# ── Admin credentials ─────────────────────────────────────────
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "Admin"


# ── Login required decorator ──────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access the Admin panel.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ── HOME ──────────────────────────────────────────────────────
@app.route("/")
def index():
    stats = contract.get_stats()
    charities = contract.get_charities()
    recent_txs = contract.blockchain.get_all_transactions()[-5:][::-1]  # last 5, newest first
    return render_template("index.html", stats=stats, charities=charities, recent_txs=recent_txs)


# ── DONATE PAGE ───────────────────────────────────────────────
@app.route("/donate", methods=["GET", "POST"])
def donate():
    charities = contract.get_charities()

    if request.method == "POST":
        donor_name  = request.form.get("donor_name", "").strip()
        charity_id  = request.form.get("charity_id", "")
        amount      = request.form.get("amount", "0")
        message     = request.form.get("message", "")

        try:
            amount = float(amount)
        except ValueError:
            flash("Please enter a valid amount.", "error")
            return render_template("donate.html", charities=charities)

        result = contract.donate(donor_name, charity_id, amount, message)

        if result["success"]:
            flash(f"✅ Donation successful! Your tracking ID: {result['tx_hash'][:20]}...", "success")
            return redirect(url_for("track", tx_hash=result["tx_hash"]))
        else:
            flash(f"❌ {result['error']}", "error")

    return render_template("donate.html", charities=charities)


# ── TRACK DONATION ────────────────────────────────────────────
@app.route("/track")
def track():
    tx_hash = request.args.get("tx_hash", "")
    tx = None
    if tx_hash:
        tx = contract.blockchain.find_transaction(tx_hash)
    all_txs = contract.blockchain.get_all_transactions()[::-1]   # newest first
    return render_template("track.html", tx=tx, tx_hash=tx_hash, all_txs=all_txs)


# ── BLOCKCHAIN EXPLORER ───────────────────────────────────────
@app.route("/explorer")
def explorer():
    chain = contract.blockchain.to_dict()[::-1]   # newest block first
    is_valid = contract.blockchain.is_chain_valid()
    return render_template("explorer.html", chain=chain, is_valid=is_valid)


# ── LOGIN PAGE ────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session["admin_username"]  = username
            flash("✅ Welcome back, Admin!", "success")
            return redirect(url_for("admin"))
        else:
            flash("❌ Invalid username or password.", "error")

    return render_template("login.html")


# ── LOGOUT ────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    flash("✅ You have been logged out.", "success")
    return redirect(url_for("login"))


# ── ADMIN PANEL ───────────────────────────────────────────────
@app.route("/admin")
@login_required
def admin():
    charities     = contract.get_charities()
    beneficiaries = contract.get_beneficiaries()
    stats         = contract.get_stats()
    return render_template("admin.html",
                           charities=charities,
                           beneficiaries=beneficiaries,
                           stats=stats)


@app.route("/admin/release", methods=["POST"])
@login_required
def admin_release():
    charity_id      = request.form.get("charity_id")
    beneficiary_id  = request.form.get("beneficiary_id")
    amount          = request.form.get("amount", "0")
    try:
        amount = float(amount)
    except ValueError:
        flash("Invalid amount.", "error")
        return redirect(url_for("admin"))

    result = contract.release_funds(charity_id, beneficiary_id, amount)
    if result["success"]:
        flash(f"✅ Funds released! Block hash: {result['tx_hash'][:20]}...", "success")
    else:
        flash(f"❌ {result['error']}", "error")
    return redirect(url_for("admin"))


@app.route("/admin/verify/<beneficiary_id>", methods=["POST"])
@login_required
def admin_verify(beneficiary_id):
    result = contract.verify_beneficiary(beneficiary_id)
    if result["success"]:
        flash(f"✅ Beneficiary verified and recorded on blockchain.", "success")
    else:
        flash(f"❌ {result['error']}", "error")
    return redirect(url_for("admin"))


@app.route("/admin/add_beneficiary", methods=["POST"])
@login_required
def admin_add_beneficiary():
    name       = request.form.get("name", "").strip()
    charity_id = request.form.get("charity_id", "")
    if not name:
        flash("Name is required.", "error")
        return redirect(url_for("admin"))
    result = contract.add_beneficiary(name, charity_id)
    if result["success"]:
        flash(f"✅ Beneficiary '{name}' added (ID: {result['beneficiary_id']}). Pending verification.", "success")
    else:
        flash(f"❌ {result['error']}", "error")
    return redirect(url_for("admin"))


# ── API endpoint (JSON) — for advanced use ────────────────────
@app.route("/api/chain")
def api_chain():
    return jsonify(contract.blockchain.to_dict())


@app.route("/api/stats")
def api_stats():
    return jsonify(contract.get_stats())


# ── Run ───────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🔗 Charity Blockchain Platform running at http://127.0.0.1:8080\n")
    app.run(debug=True, port=8080)

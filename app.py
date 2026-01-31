from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB = os.path.join(os.path.dirname(__file__), "database.db")

# --------------------------
# Home & Login
# --------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = cur.fetchone()
        conn.close()
        if user:
            session["user"] = username
            flash("✅ Login successful!", "success")
            return redirect(url_for("main"))
        else:
            flash("❌ Invalid username or password", "danger")
    return render_template("login.html")

# --------------------------
# Main dashboard cards
# --------------------------
@app.route("/main")
def main():
    if "user" not in session:
        flash("⚠️ Please login first", "warning")
        return redirect(url_for("login"))
    return render_template("main.html", user=session["user"])

# --------------------------
# Live Data Dashboard
# --------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("⚠️ Please login first", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# --------------------------
# API: Readings for live data
# --------------------------
@app.route("/api/readings")
def api_readings():
    if "user" not in session:
        return jsonify([])
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT timestamp,equipment_id,usage_hours,temperature,vibration,pressure,failure FROM readings ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    data = [{"timestamp":r[0],"equipment_id":r[1],"usage_hours":r[2],
             "temperature":r[3],"vibration":r[4],"pressure":r[5],"failure":r[6]} for r in rows]
    return jsonify(data)

# --------------------------
# Predictions
# --------------------------
@app.route("/predictions")
def predictions_page():
    if "user" not in session:
        flash("⚠️ Please login first","warning")
        return redirect(url_for("login"))
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT timestamp,equipment_id,predicted_prob,predicted_label FROM predictions ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    predictions = [{"timestamp":r[0],"equipment_id":r[1],"predicted_prob":r[2],"predicted_label":r[3]} for r in rows]
    return render_template("predictions.html", predictions=predictions, user=session["user"])

# --------------------------
# Maintenance
# --------------------------
@app.route("/maintenance")
def maintenance_page():
    if "user" not in session:
        flash("⚠️ Please login first","warning")
        return redirect(url_for("login"))
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id,equipment_id,description,scheduled_date,status FROM maintenance_tasks ORDER BY scheduled_date")
    rows = cur.fetchall()
    conn.close()
    tasks = [{"id":r[0],"equipment_id":r[1],"description":r[2],"scheduled_date":r[3],"status":r[4]} for r in rows]
    return render_template("maintenance.html", tasks=tasks, user=session["user"])

# --------------------------
# Reports
# --------------------------
@app.route("/reports")
def reports_page():
    if "user" not in session:
        flash("⚠️ Please login first","warning")
        return redirect(url_for("login"))
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT equipment_id, AVG(temperature), AVG(vibration), AVG(pressure), SUM(failure) FROM readings GROUP BY equipment_id")
    rows = cur.fetchall()
    conn.close()
    return render_template("reports.html", rows=rows, user=session["user"])

# --------------------------
# Alerts
# --------------------------
@app.route("/alerts")
def alerts_page():
    if "user" not in session:
        flash("⚠️ Please login first","warning")
        return redirect(url_for("login"))
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT timestamp,equipment_id,failure FROM readings WHERE failure=1 ORDER BY id DESC LIMIT 20")
    fails = cur.fetchall()
    cur.execute("SELECT timestamp,equipment_id,predicted_prob FROM predictions WHERE predicted_prob>=0.8 ORDER BY id DESC LIMIT 20")
    risks = cur.fetchall()
    conn.close()
    return render_template("alerts.html", fails=fails, risks=risks, user=session["user"])

# --------------------------
# Logout
# --------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("ℹ️ Logged out","info")
    return redirect(url_for("login"))

# --------------------------
# Run Flask
# --------------------------
if __name__=="__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from ai_engine import calculate_sugar
from database import init_db
import sqlite3
import serial
import time

app = Flask(__name__)

init_db()

# Store last result temporarily
last_result = {}

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():

    global last_result

    name = request.form['name']
    age = request.form['age']
    bmi = request.form['bmi']
    blood_sugar = request.form['blood_sugar']
    activity = request.form['activity']
    diabetic = request.form.get('diabetic') == 'on'

    conn = sqlite3.connect('fructual.db')
    c = conn.cursor()

    # -------------------------
    # Check or Create User
    # -------------------------
    c.execute("SELECT id FROM users WHERE name=?", (name,))
    user = c.fetchone()

    if user:
        user_id = user[0]
    else:
        c.execute(
            "INSERT INTO users (name, age, bmi, diabetic) VALUES (?, ?, ?, ?)",
            (name, age, bmi, int(diabetic))
        )
        conn.commit()
        user_id = c.lastrowid

    # -------------------------
    # Get Last 3 Logs
    # -------------------------
    c.execute("""
        SELECT blood_sugar FROM logs
        WHERE user_id=?
        ORDER BY date DESC
        LIMIT 3
    """, (user_id,))

    previous_logs = c.fetchall()

    previous_avg = None

    if len(previous_logs) == 3:
        total = sum([row[0] for row in previous_logs])
        previous_avg = round(total / 3, 2)

    # -------------------------
    # AI Calculation
    # -------------------------
    grams, fruit, status, previous_avg, adjustment = calculate_sugar(
        age, bmi, blood_sugar, activity, diabetic, previous_avg
    )

    # Save last result
    last_result = {
        "grams": grams,
        "fruit": fruit
    }

    # -------------------------
    # Save Log
    # -------------------------
    c.execute(
        "INSERT INTO logs (user_id, blood_sugar, recommended_grams) VALUES (?, ?, ?)",
        (user_id, blood_sugar, grams)
    )
    conn.commit()
    conn.close()

    # -------------------------
    # UI OUTPUT
    # -------------------------
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Fructual Result</title>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }}

        body {{
            height: 100vh;
            background: linear-gradient(135deg, #1e2a38, #2c5364);
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            overflow: hidden;
        }}

        /* Background particles */
        body::before {{
            content: "";
            position: absolute;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.18) 1px, transparent 1px);
            background-size: 60px 60px;
            animation: move 20s linear infinite;
        }}

        @keyframes move {{
            from {{ transform: translate(0,0); }}
            to {{ transform: translate(-120px,-120px); }}
        }}

        .container {{
            position: relative;
            z-index: 1;
            width: 600px;
            padding: 40px;
            border-radius: 20px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            box-shadow: 0 0 50px rgba(0,0,0,0.6);
            text-align: center;
        }}

        h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}

        .user {{
            opacity: 0.8;
            margin-bottom: 20px;
        }}

        .grams {{
            font-size: 70px;
            color: #00ffd5;
            margin: 20px 0;
        }}

        .info {{
            margin: 10px 0;
        }}

        .status {{
            margin: 15px 0;
            color: #ffd700;
            font-weight: bold;
        }}

        hr {{
            margin: 20px 0;
            opacity: 0.3;
        }}

        /* Progress bar */
        .progress-container {{
            width: 100%;
            height: 10px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
        }}

        .progress {{
            height: 100%;
            width: 0%;
            background: #00ffd5;
            transition: width 2s ease;
        }}

        /* Buttons */
        .button-group {{
            margin-top: 25px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: center;
        }}

        .btn {{
            width: 220px;
            padding: 12px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            transition: 0.3s;
        }}

        .dispense {{
            background: #00ffd5;
            color: black;
        }}

        .dispense:hover {{
            transform: scale(1.05);
            background: #00c2a8;
        }}

        .back {{
            background: white;
            color: black;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            line-height: 40px;
        }}

        .back:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>

<body>

<div class="container">

    <h1>🍓 FRUCTUAL AI</h1>
    <p class="user">User: {name}</p>

    <div class="grams">{grams} g</div>

    <p class="info"><b>Fruit Blend:</b> {fruit}</p>
    <p class="status">{status}</p>

    <hr>

    <h3>📊 Adaptive Intelligence</h3>
    <p>Previous Avg: {previous_avg}</p>
    <p>Adjustment: {adjustment} g</p>

    <!-- Progress -->
    <div class="progress-container">
        <div class="progress" id="progressBar"></div>
    </div>

    <!-- Buttons -->
    <div class="button-group">

        <form action="/dispense" method="post">
            <button class="btn dispense"> Dispense Now</button>
        </form>

        <a href="/" class="btn back">⬅ Go Back</a>

    </div>

</div>

<script>
    let bar = document.getElementById("progressBar");
    setTimeout(() => {{
        bar.style.width = "100%";
    }}, 500);
</script>

</body>
</html>
"""
# -------------------------
# DISPENSE ROUTE
# -------------------------
@app.route('/dispense', methods=['POST'])
def dispense():

    global last_result

    grams = last_result.get("grams", 0)
    fruit = last_result.get("fruit", "Unknown")

    try:
        arduino = serial.Serial('COM5', 9600, timeout=1)
        time.sleep(2)

        print(f"Dispensing {grams}g...")
        print(f"Blend: {fruit}")

        for i in range(1, int(grams) + 1):
            arduino.write(f"{i}\n".encode())
            time.sleep(0.3)

        arduino.close()

        message = "✅ Dispensing Completed!"

    except Exception as e:
        message = f"❌ Arduino Error: {e}"

    return f"""
    <h2>{message}</h2>
    <br>
    <a href="/">Go Back</a>
    """


if __name__ == '__main__':
    app.run(debug=True)
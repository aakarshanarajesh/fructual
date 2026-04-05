def calculate_sugar(age, bmi, blood_sugar, activity, diabetic, previous_avg=None):

    base_dose = 5
    adjustment = 0

    age = int(age)
    bmi = float(bmi)
    blood_sugar = int(blood_sugar)

    # -------------------------
    # Immediate Diabetic Safety
    # -------------------------
    if diabetic:
        if blood_sugar > 180:
            return 0, "No Sugar - Unsafe", "🚫 Sugar Restricted (Blood sugar too high!)", previous_avg, 0
        elif blood_sugar > 140:
            base_dose = 2
        elif blood_sugar < 90:
            base_dose = 4

    # -------------------------
    # BMI Adjustment
    # -------------------------
    if bmi > 30:
        base_dose -= 1
    elif bmi < 18:
        base_dose += 1

    # -------------------------
    # Activity Adjustment
    # -------------------------
    if activity == "High":
        base_dose += 1
    elif activity == "Low":
        base_dose -= 1

    # -------------------------
    # 🔥 Historical Adaptive Logic
    # -------------------------
    if previous_avg is not None:
        if previous_avg > 160:
            base_dose -= 1
            adjustment = -1
        elif previous_avg < 95:
            base_dose += 1
            adjustment = +1

    # Ensure non-negative dose
    base_dose = max(base_dose, 0)

    # -------------------------
    # 🍓 4 Fruit Blend Selection
    # -------------------------
    if diabetic:
        if blood_sugar > 160:
            fruit = "Berry Fiber Blend (Ultra Low GI)"
        else:
            fruit = "Apple-Chia Metabolic Blend (Low GI)"
    else:
        if activity == "High":
            fruit = "Date-Oat Energy Blend"
        elif activity == "Medium":
            fruit = "Apple-Chia Metabolic Blend"
        else:
            fruit = "Banana-Cocoa Recovery Blend"

    # -------------------------
    # 🔥 Smart Status Message
    # -------------------------
    if base_dose == 0:
        status_msg = "🚫 Sugar Restricted (Unsafe)"
    elif base_dose <= 3:
        status_msg = "⚠️ Low Sugar Recommended"
    elif base_dose <= 6:
        status_msg = "✅ Safe Sugar Intake"
    else:
        status_msg = "⚡ High Energy Mode"

    # -------------------------
    # 🔥 Confidence Indicator (Bonus)
    # -------------------------
    if previous_avg is None:
        confidence = "Medium Confidence (No history)"
    else:
        confidence = "High Confidence"

    status_msg = status_msg + " | " + confidence

    return base_dose, fruit, status_msg, previous_avg, adjustment
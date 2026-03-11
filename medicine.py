from flask import Flask, request, render_template_string

app = Flask(__name__)

# Drug interaction database
drug_interactions = {
    ("Aspirin", "Ibuprofen"): "May cause stomach bleeding",
    ("Paracetamol", "Alcohol"): "Risk of severe liver damage",
    ("Amoxicillin", "Methotrexate"): "May increase toxic drug levels"
}

# HTML Page
html_page = """
<!DOCTYPE html>
<html>
<head>
<title>Medicine Reminder & Drug Interaction Alert</title>

<style>
body{
font-family: Arial;
background:#eef2f3;
text-align:center;
}

.container{
background:white;
width:400px;
margin:60px auto;
padding:30px;
border-radius:10px;
box-shadow:0px 0px 10px gray;
}

h2{
color:#333;
}

input{
width:80%;
padding:10px;
margin:8px;
border:1px solid #ccc;
border-radius:5px;
}

button{
padding:10px 20px;
background:#28a745;
color:white;
border:none;
border-radius:5px;
cursor:pointer;
}

button:hover{
background:#218838;
}

.alert{
color:red;
font-weight:bold;
margin-top:10px;
}

.safe{
color:green;
font-weight:bold;
}

</style>
</head>

<body>

<div class="container">

<h2>💊 Medicine Reminder & Drug Interaction Checker</h2>

<form method="POST">

<input type="text" name="medicine1" placeholder="Enter Medicine 1"><br>
<input type="text" name="medicine2" placeholder="Enter Medicine 2"><br>
<input type="text" name="medicine3" placeholder="Enter Medicine 3"><br>

<button type="submit">Check Interaction</button>

</form>

{% if alerts %}

<h3>⚠ Interaction Alerts</h3>

{% for alert in alerts %}
<p class="alert">{{alert}}</p>
{% endfor %}

{% elif checked %}
<p class="safe">✅ No harmful interactions detected</p>

{% endif %}

</div>

</body>
</html>
"""

# Function to check interactions
def check_interactions(meds):

    alerts = []

    for i in range(len(meds)):
        for j in range(i+1, len(meds)):

            pair = (meds[i], meds[j])
            reverse = (meds[j], meds[i])

            if pair in drug_interactions:
                alerts.append(f"{meds[i]} + {meds[j]} → {drug_interactions[pair]}")

            elif reverse in drug_interactions:
                alerts.append(f"{meds[j]} + {meds[i]} → {drug_interactions[reverse]}")

    return alerts


@app.route("/", methods=["GET","POST"])
def home():

    alerts = []
    checked = False

    if request.method == "POST":

        m1 = request.form.get("medicine1")
        m2 = request.form.get("medicine2")
        m3 = request.form.get("medicine3")

        medicines = [m for m in [m1,m2,m3] if m]

        alerts = check_interactions(medicines)

        checked = True

    return render_template_string(html_page, alerts=alerts, checked=checked)


if __name__ == "__main__":
    app.run(debug=True)
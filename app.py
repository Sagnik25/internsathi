from flask import Flask, render_template, request
import os
import pickle

app = Flask(__name__)

# Load your ML models (for now, placeholders)
try:
    with open("models/ml_model_normal.pkl", "rb") as f:
        ml_model_normal = pickle.load(f)
except:
    ml_model_normal = None

try:
    with open("models/ml_model_disabled.pkl", "rb") as f:
        ml_model_disabled = pickle.load(f)
except:
    ml_model_disabled = None

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        resume_text = request.form.get("resume_text", "")
        type_ = request.form.get("type", "normal")

        # Mock recommendation logic (replace with ML model later)
        if type_ == "normal":
            results = [
                {"company": "Solfyn International LLP", "internship": "Procurement Executive",
                 "place": "Mumbai", "exp": "0 year(s)", "salary": "₹2,40,000 - 3,00,000"},
                {"company": "Zedex Info Pvt Ltd", "internship": "Data Entry Associate",
                 "place": "Mumbai", "exp": "0 year(s)", "salary": "₹2,00,000"}
            ]
        else:  # Disabled-friendly
            results = [
                {"company": "GlobalCorp", "internship": "Data Analyst Intern",
                 "place": "Remote", "exp": "2 year(s)", "salary": "₹2,00,000 - 3,00,000", "accessible": "Yes", "women_friendly": "Yes"},
                {"company": "TechNova", "internship": "Data Analyst Intern",
                 "place": "Remote", "exp": "1 year(s)", "salary": "₹4,50,000 - 6,00,000", "accessible": "Yes", "women_friendly": "Yes"}
            ]

    return render_template("index.html", results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

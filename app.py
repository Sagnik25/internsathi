from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
import PyPDF2
import os

app = Flask(__name__)

# ---------------- Load Datasets ----------------
normal_jobs = pd.read_csv("models/internshala_jobs.csv")
disabled_jobs = pd.read_csv("models/internships_disabled_remote.csv")

# Create a 'combined' column for NLP search
def create_combined(df, columns):
    return df[columns].astype(str).apply(lambda x: ' '.join(x).lower(), axis=1)

normal_jobs["combined"] = create_combined(normal_jobs, ["job", "company", "place"])
disabled_jobs["combined"] = create_combined(disabled_jobs, ["internship", "company", "place", "mode", "accessible", "women_friendly"])

# ---------------- Utility Functions ----------------
def recommend_jobs(df, query, top_n=5):
    if not query.strip():
        return df.head(top_n).to_dict(orient="records")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df["combined"])
    query_vec = tfidf.transform([query.lower()])
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = sim_scores.argsort()[-top_n:][::-1]
    return df.iloc[top_indices].to_dict(orient="records")

def extract_text(file):
    # DOCX
    if file.filename.endswith(".docx"):
        return docx2txt.process(file)
    # PDF
    elif file.filename.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    else:
        return ""

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():
    if request.method == "POST":
        file = request.files.get("resume")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400
        text = extract_text(file)
        results = recommend_jobs(normal_jobs, text)
        return render_template("upload_resume.html", results=results)
    return render_template("upload_resume.html", results=None)

@app.route("/recommend-normal", methods=["POST"])
def recommend_normal():
    query = request.form.get("query", "")
    results = recommend_jobs(normal_jobs, query)
    return render_template("index.html", results=results)

@app.route("/recommend-disabled", methods=["POST"])
def recommend_disabled():
    query = request.form.get("query", "")
    results = recommend_jobs(disabled_jobs, query)
    return render_template("index.html", results_disabled=results)

@app.route("/employer-post", methods=["GET", "POST"])
def employer_post():
    if request.method == "POST":
        company = request.form.get("company")
        job = request.form.get("job")
        place = request.form.get("place")
        # For now we just append to CSV (mock MCA verification)
        new_row = pd.DataFrame([{
            "company": company,
            "job": job,
            "place": place,
            "combined": f"{job} {company} {place}".lower()
        }])
        global normal_jobs
        normal_jobs = pd.concat([normal_jobs, new_row], ignore_index=True)
        normal_jobs.to_csv("models/internshala_jobs.csv", index=False)
        return render_template("employer_post.html", success=True)
    return render_template("employer_post.html", success=False)

# ---------------- Run App ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

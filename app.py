from flask import Flask, render_template, request
import os
from utils.parser import extract_text_from_pdf, extract_info
from utils.scorer import calculate_score

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.files['resume']
        jobdesc = request.form['jobdesc']

        if resume.filename == '':
            return "No selected file"

        path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(path)

        resume_text = extract_text_from_pdf(path)
        extracted_info = extract_info(resume_text)
        score = calculate_score(resume_text, jobdesc)

        return render_template("result.html", info=extracted_info, score=score)

    return render_template("index.html")

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)

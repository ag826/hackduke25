import logging
from flask import Flask, request, jsonify, render_template
import os
from modules.genaimodell import get_summary, review_answers
from modules.voice2text import text_to_voice, mp3_to_text
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more verbose output
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to file
        logging.StreamHandler(),  # Log to console
    ],
)


@app.route("/")
def home():
    app.logger.info("Home route accessed.")
    return render_template("home.html")


@app.route("/<page>")
def render_page(page):
    valid_pages = ["interview", "results"]
    if page in valid_pages:
        app.logger.info(f"{page.capitalize()} route accessed.")
        return render_template(f"{page}.html")
    return render_template("404.html"), 404


# To read the question out loud
@app.route("/voice", methods=["POST"])
def read_question(text):
    try:
        text_to_voice(text)
        return 200
    except Exception as e:
        app.logger.error(f"Error reading question: {e}")
        return jsonify({"error": str(e)}), 500


# To convert the answers from .mp3 to text
def transcribe_answer(path):
    try:
        answer_text = mp3_to_text(path)
        return answer_text
    except Exception as e:
        app.logger.error(f"Error transcribing answer: {e}")
        return jsonify({"error": str(e)}), 500


# To get final feedback from Gemini
@app.route("/results", methods=["POST"])
def results(
    matrix,
    position,
    company_name,
    job_description,
    resume_pdf_path,
):
    try:
        response_matrix = matrix
        for row in response_matrix:
            question = row[0]
            answer = transcribe_answer(row[1])
            response_matrix[row][1] = answer
            feedback_review = review_answers(
                question,
                answer,
                position,
                company_name,
                job_description,
                resume_pdf_path,
            )
            for i in len(feedback_review):
                row[i + 2] = feedback_review[i]
        return jsonify(response_matrix)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Backend Processing
@app.route("/simulate", methods=["POST"])
def simulate_interview():
    """
    Simulate the interview process
    """
    app.logger.info("Simulating interview...")
    try:
        position = request.form.get("position")
        company = request.form.get("company")
        job_description = request.form.get("jobDescription")
        resume = request.files["resume"]  # This is a FileStorage object
        app.logger.info(position, company, job_description, resume)
        # Convert the resume file to a format compatible with genai
        resume_bytes = BytesIO(resume.read())
        app.logger.info(f"Received resume: {resume_bytes}, {type(resume_bytes)}")

        if not position or not company or not job_description or not resume:
            return jsonify({"error": "Missing required fields"}), 400

        # Get the interview questions`
        processed_data = get_summary(
            position,
            company,
            job_description,
            resume_bytes,
        )
        app.logger.info(processed_data)
        app.logger.info("Interview simulation successful.")

        app.logger.info(jsonify(processed_data))
        return jsonify(processed_data)
    except Exception as e:
        app.logger.error(f"Error simulating interview: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.logger.info("Starting Flask app...")
    app.run(debug=True, host="0.0.0.0", port=8080)  # host='0.0.0.0', port=8080

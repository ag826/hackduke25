import logging
from flask import Flask, request, jsonify, render_template
import os
from modules.genaimodell import get_summary
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

# Backend Processing
@app.route("/simulate", methods=["POST"])
def simulate_interview():
    """
    Simulate the interview process
    """
    app.logger.info("Simulating interview...")
    try:
        position = request.form.get("position")
        print(position)
        company = request.form.get("company")
        job_description = request.form.get("jobDescription")
        resume = request.files["resume"]  # This is a FileStorage object
        print(position, company, job_description, resume)
        # Convert the resume file to a format compatible with genai
        resume_bytes = BytesIO(resume.read())
        print(resume_bytes)
        
        if not position or not company or not job_description or not resume:
            return jsonify({"error": "Missing required fields"}), 400

        # Get the interview questions`
        processed_data = get_summary(
            position,
            company,
            job_description,
            resume_bytes,
            )

        app.logger.info("Interview simulation successful.")
        print(processed_data)
        #return jsonify(processed_data.split("|"))
    except Exception as e:
        app.logger.error(f"Error simulating interview: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.logger.info("Starting Flask app...")
    app.run(debug=True, host="0.0.0.0", port=8080)  # host='0.0.0.0', port=8080

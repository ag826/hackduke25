import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from modules.genaimodell import get_summary, review_answers, interview_profile
from modules.voice2text import text_to_voice, mp3_to_text
from io import BytesIO
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play  # To play the audio
import base64
import json
import pyttsx3

load_dotenv()
flask_key = os.environ["API_KEY"]
# Initialize Flask app
app = Flask(__name__)
app.secret_key = flask_key

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
    valid_pages = ["interview", "results_review"]
    if page in valid_pages:
        app.logger.info(f"{page.capitalize()} route accessed.")
        return render_template(f"{page}.html")
    return render_template("404.html"), 404


# To read the question out loud
@app.route("/voice", methods=["POST"])
def read_question():
    try:
        data = request.get_json()
        text = data.get("question")
        # text = request.form.get("question")
        # text_to_voice(text)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "", 200
    except Exception as e:
        app.logger.error(f"Error reading question: {e}")
        return jsonify({"error": str(e)}), 500


def webm_to_mp3(webm_file, output_path):
    """Converts WebM file to MP3 format"""
    audio = AudioSegment.from_file(webm_file, format="webm")
    audio.export(output_path, format="mp3")
    return output_path


# To convert the answers from .mp3 to text
def transcribe_answer(audio_file):
    try:
        temp_webm_path = "/tmp/uploaded_audio.webm"  # Temporary WebM file
        temp_mp3_path = "/tmp/uploaded_audio.mp3"  # Temporary MP3 file

        audio_file.save(temp_webm_path)  # Save the WebM file first

        # Convert WebM to MP3
        webm_to_mp3(temp_webm_path, temp_mp3_path)

        # Convert MP3 to text
        answer_text = mp3_to_text(temp_mp3_path)
        return answer_text
    except Exception as e:
        app.logger.error(f"Error transcribing answer: {e}")
        return None


# To get final feedback from Gemini
@app.route("/results", methods=["POST"])
def results():
    app.logger.info("Getting final feedback...")
    try:
        # Get the matrix of questions and answers
        matrix = []
        app.logger.info(request.form)
        i = 0
        for key in request.form.keys():
            if key.startswith("question-"):
                index = key.split("-")[1]
                question = request.form.get(f"question-{index}")
                app.logger.info(question)
                audio_file = request.files.get(f"audio-{index}")
                app.logger.info(audio_file)

                # Convert the audio file to text
                answer_text = transcribe_answer(audio_file)
                answer_text = answer_text if answer_text else "No answer provided"
                app.logger.info("Transcribed answers are: %s", answer_text)
                # Read from JSON file
                try:
                    with open("interview.json", "r") as jsonfile:
                        simulation_results = json.load(jsonfile)
                except Exception as e:
                    app.logger.error(f"Error reading JSON file: {e}")
                    return jsonify({"error": "Could not read simulation results"}), 500

                position = simulation_results.get("position", "Unknown Position")
                company = simulation_results.get("company", "Unknown Company")
                job_description = simulation_results.get(
                    "job_description", "Unknown Job Description"
                )
                resume = ""  # simulation_results.get("resume", "")

                # Retrieve the question from the JSON file using the index
                question = simulation_results["questions"][i]
                i += 1

                # Append the reviewed answers to the matrix
                matrix.append(
                    review_answers(
                        question, answer_text, position, company, job_description
                    )
                )
                # Delete the temporary "interview.json" file
        try:
            os.remove("interview.json")
            app.logger.info("Temporary interview.json file deleted.")
        except Exception as e:
            app.logger.error(f"Error deleting temporary interview.json file: {e}")
        return jsonify(matrix)
    except Exception as e:
        app.logger.error(f"Error processing results: {e}")
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
        profile = request.form.get("profile_type")
        resume = request.files["resume"]  # This is a FileStorage object
        app.logger.info(position, company, job_description, profile, resume)
        # Convert the resume file to a format compatible with genai
        resume_bytes = BytesIO(resume.read())
        app.logger.info(f"Received resume: {resume_bytes}, {type(resume_bytes)}")

        if not position or not company or not job_description or not resume:
            return jsonify({"error": "Missing required fields"}), 400

        # Get the interview questions`
        processed_data = get_summary(
            position,
            company,
            profile,
            job_description,
            resume_bytes,
        )
        interviewer_profile = interview_profile(
            position,
            company,
            profile,
            job_description,
        )
        app.logger.info(processed_data)
        app.logger.info("Interview simulation successful.")
        session["simulationResults"] = (
            processed_data  # Store in session for retrieval in the frontend
        )
        # Prepare data for JSON
        json_data = {
            "position": position,
            "company": company,
            "job_description": job_description,
            "profile": profile,
            "questions": processed_data,  # Directly use the array
        }

        # Write to JSON file
        with open("interview.json", "w") as jsonfile:
            json.dump(json_data, jsonfile, indent=4)
        return jsonify(processed_data)
    except Exception as e:
        app.logger.error(f"Error simulating interview: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.logger.info("Starting Flask app...")
    app.run(debug=True, host="0.0.0.0", port=8080)  # host='0.0.0.0', port=8080

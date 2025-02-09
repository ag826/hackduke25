import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
from modules.genaimodell import get_summary, review_answers
from modules.voice2text import text_to_voice, mp3_to_text
from io import BytesIO
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play  # To play the audio


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


def is_valid_audio(file_storage):
    try:
        # Read file and reset pointer for future use
        file_data = file_storage.read()
        file_storage.seek(0)  # Reset for saving or reprocessing

        # Detect file format
        mime_type = file_storage.content_type
        app.logger.info(f"Received file MIME type: {mime_type}")

        # Ensure correct format handling
        if "webm" in mime_type:
            audio = AudioSegment.from_file(BytesIO(file_data), format="webm")
        elif "mp3" in mime_type:
            audio = AudioSegment.from_file(BytesIO(file_data), format="mp3")
        else:
            raise ValueError(f"Unsupported audio format: {mime_type}")

        # Play the audio (Optional: Remove in production)
        play(audio)

        return True
    except Exception as e:
        app.logger.error(f"Invalid audio file: {e}")
        return False


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
        #return jsonify({"error": str(e)}), 500


# To get final feedback from Gemini
@app.route("/results", methods=["POST"])
def results():
    app.logger.info("Getting final feedback...")
    """
    try:
        # Get the matrix of questions and answers
        matrix = request.form.get("matrix")
        position = request.form.get("position")
        company = request.form.get("company")
        job_description = request.form.get("jobDescription")
        resume = request.files["resume"]
        app.logger.info(matrix, position, company, job_description, resume)

        if not matrix or not position or not company or not job_description or not resume:
            return jsonify({"error": "Missing required fields"}), 400

        # Convert the resume file to a format compatible with genai
        resume_bytes = BytesIO(resume.read())
        app.logger.info(f"Received resume: {resume_bytes}, {type(resume_bytes)}")

        # Get the final feedback from Gemini
        response_matrix = matrix
        for row in response_matrix:
            question = row[0]
            answer = transcribe_answer(row[1])
            response_matrix[row][1] = answer
            feedback_review = review_answers(
                question,
                answer,
                position,
                company,
                job_description,
                resume_bytes,
            )
            for i in len(feedback_review):
                row[i + 2] = feedback_review[i]
        app.logger.info("Final feedback received.")
        return jsonify(response_matrix)
    """
    try:
        # Get the matrix of questions and answers
        matrix = []
        app.logger.info(request.form)
        for key in request.form.keys():
            if key.startswith("question-"):
                index = key.split("-")[1]
                question = request.form.get(f"question-{index}")
                app.logger.info(question)
                audio_file = request.files.get(f"audio-{index}")
                app.logger.info(audio_file)

                # Validate and play the uploaded audio file
                if not is_valid_audio(audio_file):
                    return jsonify({"error": f"Invalid audio file: audio-{index}"}), 400
                
                # Convert the audio file to text
                answer_text = transcribe_answer(audio_file)
                app.logger.info("Transcribed answers are: %s", answer_text)
                matrix.append({"question": question, "answer": answer_text})
                #app.logger.info(matrix)
                #Question and answer
                #TODO retrieve:
                """
                position = request.form.get("position")
                company = request.form.get("company")
                job_description = request.form.get("jobDescription")
                resume = request.files["resume"]  # This is a FileStorage object
                """ 
        
        return jsonify({"status": "success", "matrix": matrix}), 200
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
        resume = request.files["resume"]  # This is a FileStorage object
        # TODO: profile-type 
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
        session["simulationResults"] = processed_data  # Store in session for retrieval in the frontend
        return jsonify(processed_data)
    except Exception as e:
        app.logger.error(f"Error simulating interview: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.logger.info("Starting Flask app...")
    app.run(debug=True, host="0.0.0.0", port=8080)  # host='0.0.0.0', port=8080

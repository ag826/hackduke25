import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel

load_dotenv()
# Directly set your API key
api_key = os.environ["API_KEY"]
# Replace with your actual API key
# Configure the API key
genai.configure(api_key=api_key)

gemini_client = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are playing the role of an interview assisstant to help prepare the candidate for an interview. Use all the information inputted to generate possible questions that can be asked in the final interview and be prepared to provide constructive feedback to the candidate as he answers.",
)


# Initial interview questions
def get_summary(
    position,
    company_name,
    job_description,
    resume_pdf_path,
    model=genai.GenerativeModel("gemini-1.5-flash"),
):
    resume = genai.upload_file(resume_pdf_path)
    response = model.generate_content(
        [
            "Based on the input shared below, generate interview questions for this candidate tailored to the role they are planning to interview for,"
            "the reference information shared is as follows: , "
            f"The position the candidate is applying for is: {position}"
            f"The company name the candidate is applying to is: {company_name}"
            f"The job description of the position the candidate is applying for is: {job_description}"
            "The resume of the candidate applying for this position is attached as a pdf below."
            "First understand the position the candidate is applying for based on the job description and your knowledge of the type of questions the company usually asks in interviews",
            "Then use the context from the resume to generate the 5 questions the candidate is most likely to recieve in an interview."
            "Return the 5 questions in a pipe '|' seperated format to me. Return only the five questions in this format, do not include anything else before or after the questions",
            resume,
        ]
    )
    return response.text


if __name__ == "__main__":
    # Default to the test resume for standalone testing

    resume_path = "C:\\Users\\asus\\Desktop\\DUKE\\INTERNSHIPS\\PROJ UPD\\Resume - Adil Keku Gazder.pdf"
    questions = get_summary(
        "Data Science Intern",
        "Amazon Web Services",
        "data science internship covering data engineering, SQL, python",
        resume_path,
    )
    print(f"LIKELY QUESTIONS ARE:{questions}")

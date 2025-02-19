import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import tempfile

load_dotenv()
api_key = os.environ["API_KEY"]
genai.configure(api_key=api_key)

gemini_client = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are playing the role of an interview assisstant to help prepare the candidate for an interview. Use all the information inputted to generate possible questions that can be asked in the final interview and be prepared to provide constructive feedback to the candidate as he answers.",
)


# Profiler of the interviewer
def interview_profile(
    position,
    company_name,
    profile,
    job_description,
    model=genai.GenerativeModel("gemini-1.5-flash"),
):
    response = model.generate_content(
        [
            "Based on the information given below for a candidate preparing for an interview, generate a fictional yet realistic description of a hypothetical interviewer who would conduct this interview"
            "Describe the critical background and profile of the interviewer in 3 sentences"
            f"The position the candidate is applying for is: {position}"
            f"The company name the candidate is applying to is: {company_name}"
            f"The job description of the position the candidate is applying for is: {job_description}"
            f"The type of interview the the candidate is preparing for is: {profile}"
            "Deliver your output in first person, and share details a candidate would only be able to find through public resources",
        ]
    )
    interviewer_desc = response.text
    return interviewer_desc


# Initial interview questions
def get_summary(
    position,
    company_name,
    profile,
    job_description,
    resume_pdf,
    model=genai.GenerativeModel("gemini-1.5-flash"),
):
    resume = genai.upload_file(
        resume_pdf, mime_type="application/pdf"
    )  # Corrected here

    response = model.generate_content(
        [
            "Based on the input shared below, generate interview questions for this candidate tailored to the role they are planning to interview for,"
            "the reference information shared is as follows: , "
            f"The position the candidate is applying for is: {position}"
            f"The company name the candidate is applying to is: {company_name}"
            f"The job description of the position the candidate is applying for is: {job_description}"
            f"The type of interview the the candidate is preparing for is: {profile}"
            "The resume of the candidate applying for this position is attached as a pdf below."
            "First understand the position the candidate is applying for based on the job description and your knowledge of the type of questions the company usually asks in interviews",
            "Then use the context from the resume to generate the 5 questions the candidate is most likely to recieve in an interview."
            "Return the 5 questions in a pipe '|' seperated format to me. Return only the five questions in this format, do not include anything else before or after the questions"
            "Ensure there is a flow to the questions that you ask",
            resume,
        ]
    )
    questions = response.text
    question_list = questions.split("|")
    final_questions = []
    for str in question_list:
        if str != "":
            final_questions.append(str)

    """
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".txt",
        dir="../tempfiles",
        prefix="question_bank",
    ) as temp_file:
        # Write the questions to the temporary file
        for question in question_list:
            temp_file.write(question + "\n")
    """
    return final_questions


def review_answers(
    question,
    answer,
    position,
    company_name,
    job_description,
    model=genai.GenerativeModel("gemini-1.5-flash"),
):
    # resume = genai.upload_file(resume_pdf, mime_type="application/pdf")  # Corrected here
    response = model.generate_content(
        [
            "For the candidate who is preparing for the interview, review his answer to the questions. Remember the following information about the candidate:",
            f"The position the candidate is applying for is: {position}"
            f"The company name the candidate is applying to is: {company_name}"
            f"The job description of the position the candidate is applying for is: {job_description}"
            "The resume of the candidate applying for this position is attached as a pdf below."
            f"This was the question that was asked to the candidate as part of this interview: {question}"
            f"This was the response that the candidate gave: {answer}"
            f"Review this answer from the perspective of someone who already is a {position} at {company_name} and give constructive feedback by answering the following questions:"
            "- What went well in the candidates answer"
            "- What could have been improved in the candidates answer"
            "- Sample of how the answer can be changed to best answer this question (Do not allucinate, use only information availale from the resume)"
            "- Score on a scale of 1-10 (in increments of 0.5) based on the most important parameters you would use to answer this question."
            "- Elaborate briefly on the parameters you used to evaluate this"
            "All your responses to the questions above should be in the second person only, output your answers in a pipe '|' delimited format.  Give only your answer and none of these grading parameters. Do not include any additional information before or after this. Be professional in all your responses"
            "Do not start your answer with the '|' operator",
            # resume,
        ]
    )

    review = response.text
    feedback_list = review.split("|")
    print(review)
    print("__________________________________________")
    # result = {
    #     "question": question,
    #     "abstract_response": feedback_list[0].strip(),
    #     "suggested_improvements": [
    #         feedback_list[i].strip() for i in range(1, len(feedback_list), 2)
    #     ],
    # }

    result = {
        "question": question,
        "what_worked": feedback_list[0].strip(),
        "what_improve": feedback_list[1].strip(),
        "alt_answer": feedback_list[2].strip(),
        "overall_score": feedback_list[3].strip(),
        "criteria": feedback_list[4].strip(),
    }
    return result


if __name__ == "__main__":

    # profile = interview_profile(
    #     "Data Science Intern",
    #     "Amazon Web Services",
    #     "Behavioural",
    #     "data science internship covering data engineering, SQL, python",
    # )
    # print(profile)

    resume_path = "C:\\Users\\asus\\Desktop\\DUKE\\INTERNSHIPS\\PROJ UPD\\Resume - Adil Keku Gazder.pdf"
    questions = get_summary(
        "Senior Data Scientist",
        "Amazon Web Services",
        "Behavioural",
        " ",
        resume_path,
    )

    review = review_answers(
        "Your resume highlights your work on a portfolio optimization algorithm. Can you describe the algorithm you used, the challenges you faced, and how you evaluated its performance?",
        "Yes I did a really cool project",
        "Data Science Intern",
        "Amazon Web Services",
        "data science internship covering data engineering, SQL, python",
        # resume_path,
    )
    # print(f"LIKELY QUESTIONS ARE:{questions}")
    # print("")
    print(f"FEEDBACK:{review}")

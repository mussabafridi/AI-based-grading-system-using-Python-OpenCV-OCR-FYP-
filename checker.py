
import re
from fastapi import FastAPI, HTTPException
import os
import json
import openai
from dotenv import load_dotenv

# ✅ Load OpenAI API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = FastAPI()

# ✅ Define folder paths
QUESTION_FOLDER = "./Question_data"
ANSWER_FOLDER = "./Answer_data"

# ✅ Function to load all JSON files from a folder
def load_json_from_folder(folder_path):
    data = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):  # Only process JSON files
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data.extend(json.load(f))  # Load JSON and append to list
                    except json.JSONDecodeError:
                        print(f"❌ Error reading {filename}")
    return data

# ✅ Function to delete only JSON files from a folder (keep the folder)
def delete_json_files(folder_path):
    """Deletes all JSON files in the given folder but keeps the folder itself."""
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):  # Only delete JSON files
                file_path = os.path.join(folder_path, filename)
                os.remove(file_path)  # Delete file
                print(f"🗑 Deleted: {file_path}")  # Log deleted files

# ✅ Function to extract JSON from GPT response using regex
def extract_json_from_text(text):
    """Extracts JSON from GPT response even if extra text is present."""
    match = re.search(r"\{.*\}", text, re.DOTALL)  # Find JSON in response
    if match:
        json_string = match.group(0)
        try:
            return json.loads(json_string)  # Convert to dict
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="GPT returned an invalid JSON structure.")
    else:
        raise HTTPException(status_code=500, detail="GPT did not return a valid JSON.")

# ✅ FastAPI Endpoint to Check Answers using GPT
@app.post("/check-answers/")
async def check_answers():
    """Loads full question and answer sheets and sends them to GPT for grading."""
    try:
        # ✅ Load questions and answers from folders
        question_data = load_json_from_folder(QUESTION_FOLDER)
        answer_data = load_json_from_folder(ANSWER_FOLDER)

        if not question_data:
            raise HTTPException(status_code=404, detail="No questions found in folder.")
        if not answer_data:
            raise HTTPException(status_code=404, detail="No answers found in folder.")

        # ✅ Prepare input for GPT
        prompt = (
            "You are an expert teacher checking a student's exam paper.\n"
            "Your task is to evaluate the student's answers, match each question with the corresponding answer, "
            "and provide a structured JSON response. Follow this format:\n\n"
            "{\n"
            '    "results": [\n'
            '        {\n'
            '            "question_number": 1,\n'
            '            "question": "What is Natural Language Processing (NLP), and what are its main applications?",\n'
            '            "answer": "NLP stands for Natural Language Processing and its main applications include sentiment analysis, text summarization, and speech recognition.",\n'
            '            "result": "Correct ✅ - 5/5"\n'
            "        }\n"
            "    ]\n"
            "}\n\n"
            "Ensure the output is **strictly valid JSON** with no additional text. If you cannot generate a JSON, return an empty object {}.\n"
            "Here is the **question paper**:\n\n"
            f"{json.dumps(question_data, indent=4)}\n\n"
            "Here is the **answer sheet**:\n\n"
            f"{json.dumps(answer_data, indent=4)}"
        )

        # ✅ Call OpenAI GPT API
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a strict AI grader. Return only valid JSON, nothing else."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        # ✅ Extract JSON from GPT's response
        response_content = response.choices[0].message.content.strip()
        grading_results = extract_json_from_text(response_content)  # Extract valid JSON

        # ✅ Delete JSON files after grading
        delete_json_files(QUESTION_FOLDER)
        delete_json_files(ANSWER_FOLDER)

        return {
            "message": "✅ AI Grading Complete! JSON files have been deleted.",
            "results": grading_results["results"]  # ✅ Fix here
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

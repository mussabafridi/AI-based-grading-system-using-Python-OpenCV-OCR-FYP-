

import streamlit as st
import requests

# ✅ FastAPI Endpoints
OCR_API_URL = "http://127.0.0.1:8000/extract-json"
CHECKER_API_URL = "http://127.0.0.1:8001/check-answers/"  # Ensure port 8001 is used

st.title("ANSWER SHEET CHECKING USING AI📄")

st.sidebar.header("📌 Features")
st.sidebar.write('''OCR Extraction: Converts scanned PDFs/images into structured JSON text. Automated Answer Checking: Matches extracted questions with answers and grades them. AI-Based Evaluation: Uses GPT to determine correctness, give marks, and provide explanations. FastAPI Backend: Provides endpoints for OCR extraction and AI grading. Streamlit UI: Simple interface to upload files, extract data, and check results. Auto-Cleanup: Deletes JSON files after processing while keeping folders.''')

# ✅ Three sections: Questions, Answers, AI Paper Checker
tab1, tab2, tab3 = st.tabs(["📌 Questions", "📌 Answers", "✅ AI Paper Checker"])

# ✅ Function to send file to FastAPI OCR API and retrieve extracted JSON
def extract_data(uploaded_file, data_type):
    """Sends file to FastAPI OCR API and retrieves extracted JSON."""
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    url = f"{OCR_API_URL}/{data_type}"  # Correct FastAPI endpoint

    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            st.success(f"✅ {data_type.capitalize()} Extracted Successfully!")
            st.json(response.json())  # Show extracted JSON
        else:
            st.error(f"❌ Extraction Failed: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI. Is it running?")

# ✅ Tab 1: Upload Questions
with tab1:
    st.subheader("Upload PDF/Image for Questions")
    file_question = st.file_uploader("Upload your file", type=["pdf", "jpg", "jpeg", "png"], key="question_uploader")
    if st.button("Extract Questions", key="extract_questions"):
        if file_question:
            extract_data(file_question, "question")

# ✅ Tab 2: Upload Answers
with tab2:
    st.subheader("Upload PDF/Image for Answers")
    file_answer = st.file_uploader("Upload your file", type=["pdf", "jpg", "jpeg", "png"], key="answer_uploader")
    if st.button("Extract Answers", key="extract_answers"):
        if file_answer:
            extract_data(file_answer, "answer")

# ✅ Tab 3: AI Paper Checker
with tab3:
    st.subheader("📄 AI Paper Checker")
    st.write("Click below to check and grade answers.")

    if st.button("Check Answers & Grade", key="check_answers"):
        with st.spinner("🔍 AI is grading... Please wait."):
            try:
                response = requests.post(CHECKER_API_URL)
                if response.status_code == 200:
                    st.success("✅ AI Grading Complete!")
                    results = response.json().get("results", [])

                    if results and isinstance(results, list):  # ✅ Check if results exist and are a list
                        for res in results:
                            if isinstance(res, dict):  # ✅ Ensure `res` is a dictionary before accessing keys
                                question_number = res.get("question_number", "N/A")
                                question_text = res.get("question", "N/A")
                                answer_text = res.get("answer", "N/A")
                                result_text = res.get("result", "N/A")

                                st.write(f"📄 **Question {question_number}**")
                                st.write(f"**Question:** {question_text}")
                                st.write(f"**Answer:** {answer_text}")
                                st.write(f"📝 **Result:** {result_text}")
                                st.markdown("---")  # Separator
                            else:
                                st.warning("⚠ Invalid response format received. Please check API output.")
                    else:
                        st.warning("⚠ No matching questions and answers found.")
                else:
                    st.error(f"❌ Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to FastAPI. Is it running?")
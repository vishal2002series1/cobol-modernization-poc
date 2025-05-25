import streamlit as st
import json
from agents.clarification_agent import ClarificationAgent

def update_answer():
    st.session_state.current_answer = st.session_state.user_answer

def get_predefined_questions():
    """Return a predefined sequence of clarification questions"""
    return [
        "Which target programming language do you prefer for the COBOL modernization? (Python, Java, C#, etc.)",
        "Do you want to use cloud platforms for deployment? If yes, which one? (AWS, Azure, GCP, or on-premises)",
        "What database system should we use for data storage? (PostgreSQL, MySQL, Oracle, etc.)",
        "Do you need real-time processing capabilities or is batch processing sufficient?",
        "What are your performance requirements? (throughput, response time, concurrent users)",
        "Do you need to maintain backward compatibility with existing COBOL interfaces?",
        "What logging and monitoring tools do you prefer?",
        "Do you need automated testing and CI/CD pipeline setup?"
    ]

def main():
    st.title("COBOL Modernization - Clarification Chatbot")

    # Initialize session state variables
    if "business_doc" not in st.session_state:
        st.session_state.business_doc = None
    if "technical_doc" not in st.session_state:
        st.session_state.technical_doc = None
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "current_answer" not in st.session_state:
        st.session_state.current_answer = ""
    if "predefined_questions" not in st.session_state:
        st.session_state.predefined_questions = get_predefined_questions()

    # Upload documents if not present
    if st.session_state.business_doc is None or st.session_state.technical_doc is None:
        st.header("Upload Documents")
        business_doc_file = st.file_uploader("Upload Business Document", type=["md", "txt"])
        technical_doc_file = st.file_uploader("Upload Technical Document", type=["md", "txt"])

        if business_doc_file and technical_doc_file:
            st.session_state.business_doc = business_doc_file.read().decode("utf-8")
            st.session_state.technical_doc = technical_doc_file.read().decode("utf-8")
            st.rerun()
        else:
            st.info("Please upload both business and technical documents to start.")
            return

    # Check if we've finished all questions
    if st.session_state.current_question_index >= len(st.session_state.predefined_questions):
        st.session_state.finished = True

    # Display conversation history
    st.subheader("Conversation")
    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"**Q{i+1}:** {q}")
        a = st.session_state.answers.get(q, None)
        if a:
            st.markdown(f"**A{i+1}:** {a}")

    # If finished, show preferences summary and confirmation
    if st.session_state.finished:
        st.subheader("Final Preferences Document")
        preferences_json = json.dumps(st.session_state.answers, indent=2)
        st.text_area("Preferences JSON", preferences_json, height=300)

        if st.button("Confirm and Finish"):
            st.success("Preferences confirmed. You can proceed to the next phase.")
            with open("preferences.json", "w") as f:
                f.write(preferences_json)
            st.stop()

        if st.button("Restart"):
            st.session_state.questions = []
            st.session_state.answers = {}
            st.session_state.current_question_index = 0
            st.session_state.finished = False
            st.session_state.current_answer = ""
            st.rerun()

        return

    # Show current question and input box for answer
    current_question = st.session_state.predefined_questions[st.session_state.current_question_index]

    st.subheader("Clarification Question")
    st.write(f"**Question {st.session_state.current_question_index + 1}:** {current_question}")

    user_answer = st.text_area(
        "Your Answer",
        key="user_answer",
        on_change=update_answer,
        value=""  # Always start with empty text area
    )

    # Debug: Show current answer state
    st.write(f"Debug - Current answer: '{st.session_state.current_answer}'")

    if st.button("Submit Answer"):
        if not st.session_state.current_answer.strip():
            st.warning("Please provide an answer before submitting.")
        else:
            # Store the question and answer
            st.session_state.questions.append(current_question)
            st.session_state.answers[current_question] = st.session_state.current_answer.strip()

            # Move to next question
            st.session_state.current_question_index += 1
            st.session_state.current_answer = ""

            st.rerun()

if __name__ == "__main__":
    main()
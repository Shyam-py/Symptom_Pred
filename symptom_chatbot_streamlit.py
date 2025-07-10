import streamlit as st
import requests

# Constants
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# Prompt template
PROMPT_TEMPLATE = """
You are a helpful medical assistant. A user has described the following symptoms:
"{symptoms}"

Based on these symptoms, list 3 to 5 possible diseases or conditions they might have. Give a short explanation for each. Clearly state that this is not a diagnosis and the user should consult a real doctor.
"""

# Function to query Ollama
def get_disease_prediction(symptoms):
    prompt = PROMPT_TEMPLATE.format(symptoms=symptoms)
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })

        if response.status_code == 200:
            return response.json().get("response", "No response generated.")
        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Make sure it's running locally."

# Streamlit UI
st.set_page_config(page_title="Symptom Checker Chatbot", page_icon="🩺")

st.title("🩺 Disease Prediction Chatbot (Local LLM)")
st.markdown("Enter your symptoms and get a list of possible conditions. **Powered by LLaMA3 via Ollama** (runs locally, no internet needed).")

# Input box
symptoms = st.text_area("Describe your symptoms here:", height=150, placeholder="e.g., sore throat, fever, cough")

# Button to process
if st.button("Analyze Symptoms"):
    if symptoms.strip():
        with st.spinner("Analyzing with LLaMA3..."):
            output = get_disease_prediction(symptoms)
        st.markdown("### 🧾 Possible Conditions:")
        st.markdown(output)
    else:
        st.warning("Please enter your symptoms.")

# Optional footer
st.markdown("---")
st.caption("This tool is for educational purposes only. It is not a medical diagnosis.")

import streamlit as st
import configparser
import google.generativeai as genai
import requests

generation_config = {
   "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 192,
    "response_mime_type": "text/plain",
}

st.set_page_config(page_title="Thematic Analysis tool", page_icon="📊", layout="centered")
ai_edu_url = "https://education4ai.github.io/ai-course-design-planning-framework/"

st.title("📊 Thematic Analysis using Generative AI")
st.markdown('''
    This tool is developed to analyze the [:blue[**AI Course Design Planning Frameworks**]](%s) dataset. 
         This framework provides structure for the development of domain-speciﬁc AI courses at the university level. 
         In this tool we use ***Generative AI (Gemini)*** to automate thematic analysis. \n  It extracts meaningful keywords, 
         clusters data by domain, and visualizes thematic insights to support AI curriculum design and filtering.

''' % ai_edu_url)
readme_url = "https://github.com/darshina2/AI_Thematic_analysis/blob/master/README.md"

st.markdown('You can found more about our project [here](%s)' % readme_url)

config = configparser.ConfigParser()
gemini_url = "https://aistudio.google.com/apikey"

st.subheader("🔑 API Key Setup")
st.write('''To facilate some features of this app, you need to have [Gemini API key](%s). 
Enter your Gemini API key to save it for future use.'''% gemini_url)

api_key = st.text_input("Enter API Key:", type="password")

def validate_api_key(api_key):
    API_VERSION = 'v1'
    api_url = f'https://generativelanguage.googleapis.com/{API_VERSION}/models?key={api_key}'
    
    response = requests.get(api_url, headers={'Content-Type': 'application/json'})
    

    if response.status_code != 200:
        error_message = response.json().get('error', {}).get('message', 'Invalid API key')
        return False
    else:
        return True


if st.button("Save API Key"):
    config["GEMINI"] = {"api_key": api_key}
    
    with open("config.ini", "w") as configfile:
        config.write(configfile)
        
    x = validate_api_key(api_key)

    if x == True:
        st.success("✅ API Key saved successfully!")
    else:
        st.warning("⚠️ API key is invalid. Please enter a valid Gemini API key.")

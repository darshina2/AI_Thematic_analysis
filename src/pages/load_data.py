import streamlit as st
import os
import zipfile
import tempfile
import pandas as pd
from dataloader import dataloader
from keyword_extraction import get_keywords
from save_embeddings import save_outputs
import configparser
import shutil

config = configparser.ConfigParser()
config.read("config.ini")

st.title("🗂️ Upload and Process a ZIP Folder")

uploaded_zip = st.file_uploader("Upload a ZIP file", type="zip")

local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
EXTRACT_FOLDER = os.path.join(local_dir, "uploads/unzipped_files")
target_folder = os.path.join(local_dir, "course_files")
os.makedirs(target_folder, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

if uploaded_zip is not None:
    zip_path = os.path.join(EXTRACT_FOLDER, uploaded_zip.name)

    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.getbuffer())

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)

    st.success("✅ ZIP file extracted successfully!")

    extracted_files = [f for f in os.listdir(EXTRACT_FOLDER) if f.endswith((".csv", ".txt", ".json"))]
    st.write("📂 Extracted Files:")
    st.write(extracted_files)

    os.remove(zip_path)

st.title("Save data in an excel file:")

course_data_file = os.path.join(local_dir, "Course_output_data.xlsx")
keyword_data_file = os.path.join(local_dir, "keywords_output_data.csv")
embeddings_data_file = os.path.join(local_dir, "output_embeddings.csv")

if st.button(label="Save Data to excel", key="save_and_process"):
    try:
        st.write("Saving course data...")
        
        df_new = dataloader(EXTRACT_FOLDER, course_data_file)
        st.success("New data saved in Course_output_data.xlsx.")
        st.dataframe(df_new)
    except Exception as e:
        st.error(f"❌ Error occurred while saving data: {e}")


if st.button(label = "Get keywords", key="generate_keyword"):
    try:
        st.write("Extracting keywords...")
        keyword_output = get_keywords(course_data_file, keyword_data_file)
        st.success("Keywords extracted to keywords_output_data.csv.")
        # st.dataframe(keyword_output)
    except Exception as e:
        st.error(f"❌ Error occurred while generating keywords: {e}")
        
if st.button(label = "Generate embeddings", key="generate_embeddings"):
    try:
        st.write("Generating embeddings... (this may take a while ⏳)")
        embeddings = save_outputs(keyword_data_file, embeddings_data_file, course_data_file)
        st.success("Embeddings generated and saved in output_embeddings.csv.")
        
        for file_name in os.listdir(EXTRACT_FOLDER):
            source_path = os.path.join(EXTRACT_FOLDER, file_name)
            target_path = os.path.join(target_folder, file_name)
            
            if os.path.isfile(source_path):
                shutil.move(source_path, target_path)

        st.success(f"Moved extracted files to {target_folder}")
        
    except Exception as e:
        st.error(f"❌ Error occurred while generating embeddings: {e}")
            


    


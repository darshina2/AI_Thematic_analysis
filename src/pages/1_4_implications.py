import streamlit as st
import pandas as pd
import plotly.express as px
import os, re
from collections import Counter


st.set_page_config(page_title="Implications of Using AI", layout="wide")

st.title("📊 Implications of Using AI ")
st.write('''
There are potential implications that could arise when using AI in the respective field. This mostly concerns ethical, legal and social implications across different domains and courses.
''')
st.markdown("**Source file:** view_implications.xlsx ")

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
implications_file = os.path.join(local_dir, "views","view_implications.xlsx")

df_common = pd.read_excel(implications_file, sheet_name="Common Implications")
df_domain = pd.read_excel(implications_file, sheet_name="Domain Implications")
df_course = pd.read_excel(implications_file, sheet_name="Course Implications")


tab1, tab2, tab3 = st.tabs(["Common Implications", "Domain wise","Course wise  "])

with tab1:
    st.subheader("Commom Implications across Domains")
    st.dataframe(df_common[["Common Implications", "Domains Most Affected"]])
    st.write(''' Disclaimer: Top three domains that are the most affected by the top common implications across different domains. ''')
    
with tab2:
    st.subheader("Types of Implications")
    st.dataframe(df_domain[["Domain", "Ethical Implications", "Legal Implications", "Social Implications"]])
    
    st.subheader("Impact of Implications")
    st.dataframe(df_domain[["Domain", "Positive Examples", "Negative Examples"]])

with tab3:
    st.subheader("🎓 Course-wise Implications")
    course_options = df_course["Course_name"].unique().tolist()
    default_courses = course_options[:2]  

    selected_courses = st.multiselect(
        "Search implications of using AI in a course",
        options=course_options,
        default=default_courses
    )

    filtered_df_course = df_course[df_course["Course_name"].isin(selected_courses)]
    
    st.subheader("Types of Implications")
    st.dataframe(filtered_df_course[["Course_name", "Ethical Implications", "Legal Implications", "Social Implications"]])
    
    st.subheader("Impact of Implications")
    st.dataframe(filtered_df_course[["Course_name", "Positive Examples", "Negative Examples"]])


    
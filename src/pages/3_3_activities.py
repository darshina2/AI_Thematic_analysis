import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

local_dir: str = os.path.abspath(os.path.join(__file__ ,"../../../data/"))
output_data_path = os.path.join(local_dir, "views",  "view_activities.csv")
df = pd.read_csv(output_data_path, delimiter=';')

domains = df['Cluster'].tolist()
factors = list(df)

data = {}
data["Domain"] = df['Cluster']

st.title("📊 Learning Activities")

st.write(''' The final step involves implementing learning activities to achieve desired objectives, focusing on pedagogical implementation of course design. Merrill principles of learning are considered, and domain-specific AI courses often use a combination of teaching methods. This overview forms the basis for detailed planning, including AI-based activities. ''')

st.markdown("**Source file:** view_activities.csv ")

factors = [col for col in df.columns if col != 'Cluster']
selected_domains = st.multiselect("Select Clusters to Display:", df['Cluster'].tolist(), default=df['Cluster'].tolist())


if selected_domains:
    filtered_df = df[df['Cluster'].isin(selected_domains)].copy()

    fig = go.Figure()

    for _, row in filtered_df.iterrows():
        theta = factors + [factors[0]]
        r = row[factors].tolist() + [row[factors].tolist()[0]]
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            name=row['Cluster']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=False)
    # st.dataframe(filtered_df)
else:
    st.warning("Please select at least one cluster.")
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
data = pd.read_csv('data.csv', delimiter=';')

# Sidebar for facilitator selection
st.sidebar.header('Filter Fasilitator')
fasilitator_options = ['Semua'] + sorted(data['Kelompok Fasilitator'].unique().tolist())
selected_fasilitator = st.sidebar.selectbox('Pilih Kelompok Fasilitator:', fasilitator_options)

# Filter data based on the selected facilitator
if selected_fasilitator != 'Semua':
    data = data[data['Kelompok Fasilitator'] == selected_fasilitator]

st.title('Visualisasi Kelulusan dan Progress Peserta')

# Tingkat kelulusan per course (Bar chart)
st.header('1. Tingkat Kelulusan per Course')

course_columns = [
    'Foundations of Cybersecurity', 
    'Play It Safe: Manage Security Risks', 
    'Connect and Protect: Networks and Network Security', 
    'Tools of the Trade: Linux and SQL', 
    'Assets, Threats, and Vulnerabilities', 
    'Sound the Alarm: Detection and Response', 
    'Automate Cybersecurity Tasks with Python', 
    'Put It to Work: Prepare for Cybersecurity Jobs'
]

# Calculate the number of participants who passed each course
kelulusan_data = {course: (data[course] == 'Lulus').sum() for course in course_columns}

fig_bar = px.bar(
    x=list(kelulusan_data.keys()),
    y=list(kelulusan_data.values()),
    labels={'x': 'Course', 'y': 'Jumlah Peserta Lulus'},
    title='Tingkat Kelulusan per Course'
)
st.plotly_chart(fig_bar)

# Tingkat penyelesaian semua peserta (Pie chart)
st.header('2. Tingkat Penyelesaian Semua Peserta')

# Calculate completion rates for participants
completion_counts = data['Total Course yang Sudah Diselesaikan'].value_counts().sort_index()
completion_labels = [f'{i} Course' for i in completion_counts.index]
fig_pie_completion = px.pie(
    names=completion_labels,
    values=completion_counts,
    title='Tingkat Penyelesaian Semua Peserta'
)
st.plotly_chart(fig_pie_completion)

# Distribusi status progress peserta (Pie chart)
st.header('3. Distribusi Status Progress Peserta')

# Calculate distribution of progress status
progress_counts = data['Status Progress'].value_counts()
fig_pie_progress = px.pie(
    names=progress_counts.index,
    values=progress_counts,
    title='Distribusi Status Progress Peserta'
)
st.plotly_chart(fig_pie_progress)

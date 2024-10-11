import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('data.csv', delimiter=';')

# Load dataset
data = pd.read_csv('data.csv', delimiter=';')

# Mapping dari kode fasilitator ke nama fasilitator
fasilitator_mapping = {
    'C01': 'Aditya Firman Nugroho',
    'C02': 'Adrianus Yoga Arsa Sadana',
    'C03': 'Affandy Murad',
    'C04': 'Dimas Pramudya Haqqi',
    'C05': 'Anggoro Yudho Nuswantoro',
    'C06': 'Cosmas Sakristiandio',
    'C07': 'Andrew Benedictus Jamesie',
    'C08': 'Heri Prastio',
    'C09': 'Jajang Jamaludin',
    'C10': 'Lutfi Kiki Fuadi',
    'C11': 'Mufti AlieSatriawan',
    'C12': 'Ricky Fahriza',
    'C13': 'Roby Ismail Adi Putraq',
    'C14': 'Yeheskiel Almasar Tampubolon'
}

# Gantikan kode fasilitator dengan nama fasilitator
data['Kelompok Fasilitator'] = data['Kelompok Fasilitator'].map(fasilitator_mapping)

# Pastikan semua nilai dalam kolom 'Kelompok Fasilitator' adalah tipe string
data['Kelompok Fasilitator'] = data['Kelompok Fasilitator'].astype(str)

# Sidebar for facilitator selection
st.sidebar.header('Filter Fasilitator')
fasilitator_options = ['Semua'] + sorted(data['Kelompok Fasilitator'].unique().tolist())
selected_fasilitator = st.sidebar.selectbox('Pilih Kelompok Fasilitator:', fasilitator_options)

# <Tambahan

# Menghitung persentase kelulusan per kelompok fasilitator (TIDAK dipengaruhi oleh pemilihan)
kelulusan_counts = data.groupby('Kelompok Fasilitator')['Total Course yang Sudah Diselesaikan'].apply(
    lambda x: (x == 8).sum()
)
total_counts = data.groupby('Kelompok Fasilitator')['Total Course yang Sudah Diselesaikan'].count()

# Menghitung persentase
persentase_kelulusan = (kelulusan_counts / total_counts * 100).fillna(0).round(2)

# Mengubah ke DataFrame untuk tampilan tabel
kelulusan_df = pd.DataFrame({
    'Nama Fasilitator': persentase_kelulusan.index,
    'Persentase Kelulusan (%)': persentase_kelulusan.values
}).reset_index(drop=True)

# Mengurutkan DataFrame dari persentase tertinggi ke terendah
# kelulusan_df.sort_values(by='Persentase Kelulusan (%)', ascending=False, inplace=True)

# Tambahan>

# Filter data based on the selected facilitator
if selected_fasilitator != 'Semua':
    data = data[data['Kelompok Fasilitator'] == selected_fasilitator]

st.title('Visualisasi Kelulusan dan Progress Peserta')

# Daftar peserta yang telah menyelesaikan seluruh course
st.header('Selamat kepada peserta berikut yang telah menyelesaikan seluruh course')

# Filter peserta yang telah menyelesaikan 8 course
completed_all_courses = data[data['Total Course yang Sudah Diselesaikan'] == 8]['Name'].tolist()

# Display the names of participants who completed all courses
if completed_all_courses:
    for name in completed_all_courses:
        st.write(f"- {name}")
else:
    st.write("Belum ada peserta yang menyelesaikan seluruh course.")

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

# Tingkat penyelesaian peserta (Pie chart)
st.header('2. Tingkat Penyelesaian Peserta')

# Calculate completion rates for participants based on the number of completed courses
completion_counts = data['Total Course yang Sudah Diselesaikan'].value_counts().sort_index()
completion_labels = [f'{i} Course' for i in completion_counts.index]

# Define color map to match each label
color_mapping = {
    '0 Course': '#FF0000',  # Merah untuk 0 course
    '1 Course': '#FF4500',  # Gradasi untuk 1 course
    '2 Course': '#FF7F00',  # Gradasi untuk 2 course
    '3 Course': '#FFFF00',  # Gradasi untuk 3 course
    '4 Course': '#7FFF00',  # Gradasi untuk 4 course
    '5 Course': '#00FF00',  # Gradasi untuk 5 course
    '6 Course': '#00FFFF',  # Gradasi untuk 6 course
    '7 Course': '#00BFFF',  # Gradasi untuk 7 course
    '8 Course': '#1E90FF'   # Kebiruan untuk 8 course
}

# Buat DataFrame dari names dan values
df_pie = pd.DataFrame({'names': completion_labels, 'values': completion_counts})

fig_pie_completion = px.pie(
    data_frame=df_pie,  # Gunakan DataFrame sebagai data_frame
    names='names',  # Kolom 'names' dalam DataFrame
    values='values',  # Kolom 'values' dalam DataFrame
    title='Tingkat Penyelesaian Semua Peserta',
    color='names',  # Gunakan 'names' sebagai kolom untuk pemetaan warna
    color_discrete_map=color_mapping
)
st.plotly_chart(fig_pie_completion)

# Distribusi status progress peserta (Pie chart)
st.header('3. Status Progress Peserta')

# Calculate distribution of progress status
progress_counts = data['Status Progress'].value_counts()
progress_labels = [f'{i}' for i in progress_counts.index]

# Define color map to match each label
color_mapping = {
    'Belum Terdaftar': '#FF0000', 
    'Belum Berprogress': '#FF4500',
    'Progress Dibawah Rekomendasi': '#FF7F00',
    'Progress Diatas/Sesuai Rekomendasi': '#00BFFF',
    'Sudah Lulus Spesialisasi': '#1E90FF',
}

# Buat DataFrame dari names dan values
df_pie = pd.DataFrame({'names': progress_labels, 'values': progress_counts})

fig_pie_completion = px.pie(
    data_frame=df_pie,  # Gunakan DataFrame sebagai data_frame
    names='names',  # Kolom 'names' dalam DataFrame
    values='values',  # Kolom 'values' dalam DataFrame
    title='Status Progress Peserta',
    color='names',  # Gunakan 'names' sebagai kolom untuk pemetaan warna
    color_discrete_map=color_mapping
)
st.plotly_chart(fig_pie_completion)

# Tampilkan daftar nama peserta dan tingkat penyelesaiannya
st.header('4. Daftar Peserta dan Tingkat Penyelesaian')

# Display a table with participants' names and their course completion status
completion_table = data[['Name', 'Total Course yang Sudah Diselesaikan']].sort_values(by='Total Course yang Sudah Diselesaikan', ascending=False)
completion_table = completion_table.rename(columns={'Name': 'Nama Peserta', 'Total Course yang Sudah Diselesaikan': 'Jumlah Course yang Diselesaikan'})
st.dataframe(completion_table)

# Menampilkan tabel
st.subheader('5. Persentase Kelulusan Per Kelompok Fasilitator')

st.write(kelulusan_df)

# Menyiapkan warna untuk grafik batang
colors = ['#4682B4'] * len(kelulusan_df)  # Warna Steel Blue
top_three_indices = kelulusan_df.nlargest(3, 'Persentase Kelulusan (%)').index.tolist()  # Indeks tiga teratas
for index in top_three_indices:
    colors[index] = '#1E90FF'  # Warna Dodger Blue untuk tiga teratas

# Membuat grafik batang menggunakan Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(kelulusan_df['Nama Fasilitator'], kelulusan_df['Persentase Kelulusan (%)'], color=colors)
plt.xlabel('Nama Fasilitator')
plt.ylabel('Persentase Kelulusan (%)')
plt.title('Persentase Kelulusan Per Kelompok Fasilitator')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 100)  # Mengatur batas y antara 0 dan 100

# Menambahkan garis horizontal
thresholds = [50, 72, 79, 86, 95]
for threshold in thresholds:
    plt.axhline(y=threshold, color='red', linestyle='--', linewidth=1)  # Garis horizontal merah putus-putus

# Menampilkan grafik di Streamlit
st.pyplot(plt)

# Add a footer or caption at the bottom of the app
st.markdown("""<hr style="border:1px solid gray">""", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2024 oleh Anggoro Yudho Nuswantoro</p>",
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv("../data/day.csv") 

# Sidebar for filters
st.sidebar.title("Filter Data")

# Filter season
season_filter = st.sidebar.multiselect("Select Season", options=df['season'].unique(), default=df['season'].unique())
df_filtered = df[df['season'].isin(season_filter)]


month_filter = st.sidebar.multiselect("Select Month", options=range(1, 13), default=range(1, 13))
df_filtered = df_filtered[df_filtered['mnth'].isin(month_filter)]


st.title("Bike Sharing Data Analysis")


st.header("Distribusi Peminjaman Berdasarkan Cuaca dan Musim")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_filtered, x="temp", y="cnt", hue="season", ax=ax)
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Suhu dan Musim")
st.pyplot(fig)


st.header("Perkembangan Penyewaan Sepeda Setiap Bulan")
df['mnth'] = pd.Categorical(df['mnth'], categories=range(1, 13))
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df[df['mnth'].isin(month_filter)], x="mnth", y="cnt", ax=ax)
ax.set_title("Jumlah Penyewaan Sepeda per Bulan")
st.pyplot(fig)


st.header("Pola Perubahan Pengguna Karena Bencana Alam (2012)")
cnt_in_2012_df = df.loc[df['yr'] == 1].groupby('mnth').agg({'cnt': 'mean'}).reset_index()
cnt_in_2012_df = cnt_in_2012_df.loc[cnt_in_2012_df['mnth'].isin([10, 11, 12])]


cnt_in_2012_df = cnt_in_2012_df[cnt_in_2012_df['mnth'].isin(month_filter)]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x=cnt_in_2012_df['mnth'], height=cnt_in_2012_df['cnt'])
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Jumlah Sewa Sepeda')
ax.set_title('Rata-rata Jumlah Sewa Sepeda per Bulan di Tahun 2012 (Bulan 10 - 12)')
ax.set_xticks(cnt_in_2012_df['mnth'])
st.pyplot(fig)


st.header("Perbandingan Penyewa Sepeda Registered vs Casual per Bulan")
user_df = df.groupby('mnth').agg({'registered': 'mean', 'casual': 'mean'}).reset_index()
user_df_melted = user_df.melt(id_vars='mnth', value_vars=['registered', 'casual'], 
                               var_name='user_type', value_name='ctd')


user_df_melted = user_df_melted[user_df_melted['mnth'].isin(month_filter)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=user_df_melted, x="mnth", y="ctd", hue="user_type", ax=ax, errorbar=None)
ax.set_title("Rata-rata Penyewa Sepeda (Registered vs Casual) per Bulan")
st.pyplot(fig)


st.sidebar.header("Insights")
st.sidebar.text("""
- Suhu dan musim berpengaruh besar terhadap jumlah penyewaan sepeda.
- Penyewaan sepeda meningkat setiap bulan, tetapi menurun di akhir tahun.
- Mayoritas pengguna yang menyewa sepeda adalah pengguna yang sudah terdaftar.
- Terdapat penurunan pengguna sepeda pada bulan 10-12 tahun 2012 akibat bencana alam.
""")

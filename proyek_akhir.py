import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Gathering data
hour_df = pd.read_csv("hour.csv", delimiter = ",")
day_df = pd.read_csv("day.csv", delimiter = ",")

# Cleaning data
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['season'] = hour_df.season.astype('category')
hour_df['yr'] = hour_df.yr.astype('category')
hour_df['mnth'] = hour_df.mnth.astype('category')
hour_df['hr'] = hour_df.hr.astype('category')
hour_df['holiday'] = hour_df['holiday'].astype(bool)
hour_df['weekday'] = hour_df.weekday.astype('category')
hour_df['workingday'] = hour_df.workingday.astype('category')
hour_df['weathersit'] = hour_df.weathersit.astype('category')

day_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['season'] = day_df.season.astype('category')
day_df['yr'] = day_df.yr.astype('category')
day_df['mnth'] = day_df.mnth.astype('category')
day_df['holiday'] = day_df['holiday'].astype(bool)
day_df['weekday'] = day_df.weekday.astype('category')
day_df['workingday'] = day_df.workingday.astype('category')
day_df['weathersit'] = day_df.weathersit.astype('category')

# Streamlit app title
with st.sidebar:
    st.image("bicycle.png", width=100)
    st.title("Proyek Akhir: Bike Sharing Dataset")
    with st.container():
        st.write("Dashboard ini merupakan hasil analisis terhadap Bike Sharing Dataset sebagai proyek akhir kelas Dicoding")

tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])

# Exploratory Data Analysis
with tab1:
    st.header("Analisis Pendahuluan")
    hourly_stats = hour_df.groupby('hr').agg(
        total_rentals=('cnt', 'sum'),
        average_rentals=('cnt', 'mean')
    ).reset_index()
    hourly_stats_sorted_avg = hourly_stats.sort_values(by='average_rentals', ascending=False)
    print("Hourly Rentals Stats Sorted by Average Rentals:")
    print(hourly_stats_sorted_avg)
    st.subheader("Statistik Penggunaan Sepeda per Jam")
    st.write(hourly_stats_sorted_avg)

    seasonal_stats = hour_df.groupby('season').agg(
        total_rentals=('cnt', 'sum'),
        average_rentals=('cnt', 'mean')
    ).reset_index()
    seasonal_stats_sorted_avg = seasonal_stats.sort_values(by='average_rentals', ascending=False)
    print("Seasonal Rentals Stats Sorted by Average Rentals:")
    print(seasonal_stats_sorted_avg)
    st.subheader("Statistik Penggunaan Sepeda per Musim")
    st.write(seasonal_stats_sorted_avg)

    weekday_stats = hour_df.groupby('weekday').agg(
        total_rentals=('cnt', 'sum'),
        average_rentals=('cnt', 'mean')
    ).reset_index()
    weekday_stats_sorted_avg = weekday_stats.sort_values(by='average_rentals', ascending=False)
    print("Weekday Rentals Stats Sorted by Average Rentals:")
    print(weekday_stats_sorted_avg)
    st.subheader("Statistik Penggunaan Sepeda per Hari dalam Seminggu")
    st.write(weekday_stats_sorted_avg)

    monthly_stats = hour_df.groupby('mnth').agg(
        total_rentals=('cnt', 'sum'),
        average_rentals=('cnt', 'mean')
    ).reset_index()
    monthly_stats_sorted_avg = monthly_stats.sort_values(by='average_rentals', ascending=False)
    print("Monthly Rentals Stats Sorted by Average Rentals:")
    print(monthly_stats_sorted_avg)
    st.subheader("Statistik Penggunaan Sepeda per Bulan")
    st.write(monthly_stats_sorted_avg)

with tab2:
    st.header("Explanatory Data Analysis")

    average_usage = hour_df.groupby('holiday')['cnt'].mean().reset_index()
    average_usage['holiday'] = average_usage['holiday'].replace({True: 'Holiday', False: 'Working Day'})

    print("Rata-rata Penggunaan Sepeda:")
    print(average_usage)

    st.subheader("Rata-rata Penggunaan Sepeda antara Hari Kerja dan Hari Libur")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=average_usage, x='holiday', y='cnt', palette='pastel', ax=ax1)
    ax1.set_title('Rata-rata Penggunaan Sepeda')
    ax1.set_xlabel('Kategori')
    ax1.set_ylabel('Rata-rata Penggunaan Sepeda')
    plt.ylim(0, average_usage['cnt'].max() + 10)
    st.pyplot(fig1)

    average_usage_season = hour_df.groupby('season')['cnt'].mean().reset_index()
    season_mapping = {
        1: 'Musim Semi',
        2: 'Musim Panas',
        3: 'Musim Gugur',
        4: 'Musim Dingin'
    }
    average_usage_season['season'] = average_usage_season['season'].map(season_mapping)

    st.subheader("Rata-rata Penggunaan Sepeda berdasarkan Musim")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=average_usage_season, x='season', y='cnt', palette='Set2', ax=ax2)
    ax2.set_title('Rata-rata Penggunaan Sepeda berdasarkan Musim')
    ax2.set_xlabel('Musim')
    ax2.set_ylabel('Rata-rata Penggunaan Sepeda')
    plt.ylim(0, average_usage_season['cnt'].max() + 10)
    st.pyplot(fig2)

    average_usage_weather_hour = hour_df.groupby(['hr', 'weathersit'])['cnt'].mean().reset_index()

    weather_mapping = {
        1: 'Clear, Few clouds, Partly cloudy',
        2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
        3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
        4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
    }
    average_usage_weather_hour['weathersit'] = average_usage_weather_hour['weathersit'].map(weather_mapping)

    st.subheader("Rata-rata Penggunaan Sepeda berdasarkan Jam dan Cuaca")
    fig3, ax3 = plt.subplots(figsize=(30, 18))
    sns.lineplot(data=average_usage_weather_hour, x='hr', y='cnt', hue='weathersit', marker='o', palette='tab10', ax=ax3)
    ax3.set_title('Rata-rata Penggunaan Sepeda berdasarkan Jam dan Cuaca', fontsize=40)
    ax3.set_xlabel('Jam', fontsize=25)
    ax3.set_ylabel('Rata-rata Penggunaan Sepeda', fontsize=25)
    plt.xticks(range(0, 24))
    plt.grid()
    plt.legend(title='Kondisi Cuaca', bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=4)
    st.pyplot(fig3)

    with st.container():
        st.write('''
                Conclusion
                
                Berdasarkan hasil analisis yang dilakukan, dapat disimpulkan bahwa:
                1. Penggunaan Sepeda Berdasarkan Hari: Rata-rata penggunaan sepeda lebih tinggi
                pada hari kerja dibandingkan dengan hari libur. Hal ini menunjukkan bahwa sepeda
                cenderung digunakan lebih banyak untuk keperluan aktivitas sehari-hari seperti
                pergi bekerja atau bersekolah.
                2. Penggunaan Sepeda Berdasarkan Musim: Rata-rata penggunaan sepeda paling tinggi
                terjadi di musim gugur, sementara penggunaan sepeda paling rendah tercatat pada
                musim dingin. Hal ini mengindikasikan bahwa kondisi cuaca dan lingkungan musim
                berpengaruh terhadap minat dan kenyamanan masyarakat dalam menggunakan sepeda.
                3. Penggunaan Sepeda Berdasarkan Waktu dan Cuaca: Penggunaan sepeda paling tinggi
                terjadi pada sore hari dengan cuaca cerah, sedangkan penggunaan paling rendah
                terjadi di dini hari ketika cuaca buruk, seperti hujan lebat. Temuan ini
                menunjukkan bahwa faktor waktu dan kondisi cuaca sangat mempengaruhi keputusan
                individu untuk menggunakan sepeda sebagai alat transportasi.
                ''')

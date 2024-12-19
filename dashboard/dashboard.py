import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='ticks')

# input data day_dataFrame
day_dataFrame = pd.read_csv("main_data.csv")

# membuat fungsi untuk pengguna kasual
def create_casual_user_df(df):
    casual_user_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_user_df

# membuat fungsi untuk pengguna terdaftar
def create_registered_user_df(df):
    registered_user_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_user_df

# membuat fungsi untuk total pengguna
def create_count_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Membuat rentang filter
min_date = pd.to_datetime(day_dataFrame['dateday']).dt.date.min()
max_date = pd.to_datetime(day_dataFrame['dateday']).dt.date.max()

def create_total_bikes_rented_by_month_and_year_df(day_dataFrame):
    # Mengubah 'month' menjadi kategori terurut
    day_dataFrame['month'] = pd.Categorical(day_dataFrame['month'], categories=
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        ordered=True)

    # Menghitung jumlah sepeda berdasarkan bulan dan tahun
    monthly_counts = day_dataFrame.groupby(by=["month", "year"]).agg({
        "count": "sum"
    }).reset_index()

    sns.set(style="whitegrid", palette="muted")
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(
        data=monthly_counts,
        x="month",
        y="count",
        hue="year",
        palette="deep",
        marker="o",
        linewidth=2.5,
        markersize=8,
        ax=ax
    )

    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Jumlah Sepeda", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title="Tahun", loc="upper right", fontsize=10, title_fontsize=12)
    return fig

def create_rent_bike_based_on_weather_conditions(df_day):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(
        x='weather_conditions',
        y='count',
        data=df_day,
        ax=ax
    )

    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Jumlah Pengguna Sepeda', fontsize=12)
    return fig

def create_rent_bike_based_on_season(df_day):
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        x='season',
        y='count',
        data=df_day,
        ax=ax
    )

    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Jumlah Pengguna Sepeda', fontsize=12)
    return fig

# Membuat sidebar
with st.sidebar:
    # judul
    st.title("Bike Sharing Dataset")
    # rentang
    start_date, end_date = st.date_input(
        label='Pilih Rentang Jarak',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_dataFrame[(day_dataFrame['dateday'] >= str(start_date)) & 
                (day_dataFrame['dateday'] <= str(end_date))]

# menyimpan fungsi pada variabel
daily_rent_df = create_count_rent_df(main_df)
casual_user_df = create_casual_user_df(main_df)
registered_user_df = create_registered_user_df(main_df)

st.header('Bike Sharing')

# Membuat tampilan awal dashboard
st.subheader('Rental harian')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = casual_user_df['casual'].sum()
    st.metric('Pengguna Kasual', value= daily_rent_casual)

with col2:
    daily_rent_registered = registered_user_df['registered'].sum()
    st.metric('Pengguna Terdaftar', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total Pengguna', value= daily_rent_total)
    
# Menampilkan plot untuk jumlah sepeda yang disewakan berdasarkan Bulan dan Tahun
st.subheader('Total Sepeda yang Disewakan berdasarkan Bulan dan Tahun')
total_bikes_rented_by_month_and_year_fig = create_total_bikes_rented_by_month_and_year_df(main_df)
st.pyplot(total_bikes_rented_by_month_and_year_fig)

# Menampilkan plot untuk jumlah pengguna sepeda yang disewakan berdasarkan kondisi cuaca
st.subheader('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
rent_bike_based_on_weather_conditions_fig = create_rent_bike_based_on_weather_conditions(main_df)
st.pyplot(rent_bike_based_on_weather_conditions_fig)

# Menampilkan plot untuk jumlah pengguna sepeda yang disewakan berdasarkan kondisi musim
st.subheader('Jumlah Pengguna Sepeda berdasarkan Musim')
bike_usage_by_season_fig = create_rent_bike_based_on_season(main_df)
st.pyplot(bike_usage_by_season_fig)

st.caption('Copyright (c) Ichsan Alam Fadillah 2024')
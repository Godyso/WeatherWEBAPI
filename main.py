import requests
import pandas as pd
import streamlit as st
import numpy as np

API_KEY = "e6bec0163bf29d88088cb3d22b06bbae"

@st.cache
def fetch_weather_data(city, unit):
    unit_code = 'metric' if unit == 'Celsius' else 'imperial'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={unit_code}&appid={API_KEY}"
    response = requests.get(url)
    weather_data = response.json()

    general = weather_data['weather'][0]['main']
    icon_id = weather_data['weather'][0]['icon']
    icon = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"

    return weather_data, general, icon

st.title("Weather App")

st.sidebar.header("Input Options")

city = st.sidebar.text_input("City name", "London")
unit = st.sidebar.radio('Unit of temperature', ('Celsius', 'Fahrenheit'))

button = st.sidebar.button("Fetch Weather Data")

if button:
    data, general, icon = fetch_weather_data(city, unit)
    if data['cod'] != 200:
        st.error("Failed to fetch the data. Please check if the city name is correct.")
    else:
        weather_data = {
            "Temperature": data['main']['temp'],
            "Feels Like": data['main']['feels_like'],
            "Temperature Min": data['main']['temp_min'],
            "Temperature Max": data['main']['temp_max'],
            "Pressure": data['main']['pressure'],
            "Humidity": data['main']['humidity'],
            "Wind Speed": data['wind']['speed'],
            "General": general
        }
        df = pd.DataFrame(weather_data, index=[0])

        # Display Weather Icon
        st.image(icon, caption='Current Weather Icon')

        # Interactive Table
        st.dataframe(df)

        # Bar chart
        st.bar_chart(df.drop(columns=['General']).T)  # Transpose the dataframe

        # Map
        coordinates_df = pd.DataFrame({'lat': [data['coord']['lat']], 'lon': [data['coord']['lon']]})
        st.map(coordinates_df)

        # Info Box
        st.info(f"This is the weather information for {city}.")

        # Success Box
        st.success("Weather data fetched successfully!")

        # Checkbox
        if st.checkbox('Show raw data'):
            st.write(df)

        # Selectbox
        selected_feature = st.selectbox('Select feature', list(df.columns))

        if selected_feature:
            st.line_chart(df[selected_feature])

        # Multiselect
        selected_features = st.multiselect('Select features', list(df.columns), default=list(df.columns))

        if len(selected_features) > 0:
            st.area_chart(df[selected_features])

        # Slider
        selected_temperature = st.slider('Select a range of temperature', 0, 100, (25, 75))

        # Select-slider
        hours = st.select_slider('Select a range of hours', options=range(24))

        # File Uploader
        file = st.file_uploader("Upload an image of the city (optional)")

        # Color Picker
        color = st.color_picker("Pick a color", "#00f900")

        # Text-area
        comment = st.text_area("Leave a comment here", "")

        # Progress Bar
        import time
        latest_iteration = st.empty()
        bar = st.progress(0)
        for i in range(100):
            latest_iteration.text(f'Progress {i+1}')
            bar.progress(i + 1)
            time.sleep(0.01)

        # Columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Good")
        with col2:
            st.button("Better")
        with col3:
            st.button("Best")

        # Expander
        with st.expander("See explanation"):
            st.write("""
            The data in the table is fetched from OpenWeatherMap API.
            It shows the current weather condition in the selected city.
            """)

st.header("Weather Data")

# Example time series data
time_index = pd.date_range('2023-01-01', periods=100)
time_series_df = pd.DataFrame(np.random.randn(100, 2), index=time_index, columns=['A', 'B'])

# Line chart
st.line_chart(time_series_df['A'])

# Area chart
st.area_chart(time_series_df)



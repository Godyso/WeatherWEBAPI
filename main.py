import requests
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import json

API_KEY = "e6bec0163bf29d88088cb3d22b06bbae"
API_KEY2 = "01dc97681afde3b1c3d14dfc74df1b7f"

@st.cache_data
def fetch_hourly_weather_data(city, unit):
    try:


        url = "https://weatherapi-com.p.rapidapi.com/current.json"

        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

        querystring = {"q": city , "days": "1"}

        headers = {
            "X-RapidAPI-Key": "3dd49efa65mshca76ca025d437f1p1e6586jsn4ad979d80758",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        hourly = response.json()
        print(hourly)

        st.write(hourly["forecast"])
    except Exception:
        st.write("Nope")

@st.cache_data
def fetch_current_weather_data(city, unit):
    try:
        unit_code = 'metric' if unit == 'Celsius' else 'imperial'
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={unit_code}&appid={API_KEY}"
        response = requests.get(url)
        weather_data = response.json()

        general = weather_data['weather'][0]['main']
        icon_id = weather_data['weather'][0]['icon']
        icon = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"

    except Exception:
        st.error("Failed to fetch the data. Please check if the city name is correct.")
        return None, None, None

    return weather_data, general, icon


st.title("Weather App")
fetch_hourly_weather_data("London", "imperial")
# st.sidebar.header("Input Options")
with st.form(key="my_form"):
    city = st.text_input("City name", "London") # find a way to detect states
    unit = st.radio('Unit of temperature', ('Celsius', 'Fahrenheit'))

    button = st.form_submit_button("Fetch Weather Data")

    # Color Picker
    clr = st.color_picker('Chart Color Selector', '#00f900')


    if button:
        data, general, icon = fetch_current_weather_data(city, unit)
        # if data['cod'] != 200:
        #    st.error("Failed to fetch the data. Please check if the city name is correct.")
        if data and general and icon is not None:
            # Success Box
            st.success("Weather data fetched successfully!")
            # Info Box
            #st.info(f"This is the weather information for {str.title(city)}.")

            st.header(str.title(city))
            temperature_data = {
                "Temperature": ["Temperature", "Feals Like", "Min", "Max"],
                "Degrees" : [data['main']['temp'],
                data['main']['feels_like'],
                data['main']['temp_min'],
                data['main']['temp_max']],
            }
            weather_data = {
                "Pressure": data['main']['pressure'],
                "Humidity": data['main']['humidity'],
                "Wind Speed": data['wind']['speed'],
                "General": general
            }
            df_other = pd.DataFrame(weather_data, index=[0])
            df_temperature = pd.DataFrame(temperature_data)

            col1, col2 = st.columns(2)
            with col1:
                # Display Weather Icon
                st.image(icon, caption='Current Weather Icon')
                st.subheader("Your Weather At A Glance")
                st.info("Current temperature: " + str(df_temperature["Degrees"][0]))
                st.info("Feels like: " + str(df_temperature["Degrees"][1]))
                st.info("Humidity: " + str(df_other["Humidity"][0]))
                st.info("Wind speed: " + str(df_other["Wind Speed"][0]))
                #st.info("Feels like:", df_temperature)

            with col2:
                # Map
                coordinates_df = pd.DataFrame({'lat': [data['coord']['lat']], 'lon': [data['coord']['lon']]})
                st.map(coordinates_df)

            # Interactive Table
            #st.dataframe(df_general)
            st.subheader("Today's weather in charts")
            #clr = st.color_picker("Pick a color", "#00f900")
            # Bar chart
            #st.bar_chart(df.drop(columns=['General']).T)  # Transpose the dataframe
            bar_chart = alt.Chart(df_temperature).mark_bar().encode(
                x = "Temperature",
                y = "Degrees",
                color = alt.value(clr)
            )
            st.altair_chart(bar_chart, use_container_width=True)

            # Checkbox
            if st.checkbox('The Days Ahead'):
                st.write("To be constructed")

            # Selectbox
            #selected_feature = st.selectbox('Select feature', list(df.columns))

            #if selected_feature:
                #st.line_chart(df[selected_feature])

            # Multiselect
            #selected_features = st.multiselect('Select features', list(df.columns), default=list(df.columns))

           # if len(selected_features) > 0:
                #st.area_chart(df[selected_features])

            # Slider
            selected_temperature = st.slider('Select a range of temperature', 0, 100, (25, 75))

            # Select-slider
            hours = st.select_slider('Select a range of hours', options=range(24))

            # File Uploader
            file = st.file_uploader("Upload an image of the city (optional)")

            # Text-area
            comment = st.text_area("Leave a comment here", "")

            # Progress Bar
            import time

            latest_iteration = st.empty()
            bar = st.progress(0)
            for i in range(100):
                latest_iteration.text(f'Progress {i + 1}')
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



# Example time series data
# time_index = pd.date_range('2023-01-01', periods=100)
# time_series_df = pd.DataFrame(np.random.randn(100, 2), index=time_index, columns=['A', 'B'])

# Line chart
# st.line_chart(time_series_df['A'])

# Area chart
# st.area_chart(time_series_df)

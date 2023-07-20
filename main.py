import requests
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import numpy as np
import json

API_KEY = "e6bec0163bf29d88088cb3d22b06bbae"
API_KEY2 = "01dc97681afde3b1c3d14dfc74df1b7f"

@st.cache_data
def fetch_hourly_weather_data(city, unit):
    try:

        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

        querystring = {"q": city , "days": "1"}

        headers = {
            "X-RapidAPI-Key": "3dd49efa65mshca76ca025d437f1p1e6586jsn4ad979d80758",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        all_data = response.json()
        hourly = all_data["forecast"]["forecastday"][0]["hour"]
        #print(hourly)


        #st.write(hourly)
    except Exception:
        st.write("Nope")
        return None
    if unit == "Celsius":
        return hourly, "temp_c"
    else:
        return hourly, "temp_f"

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
# Text box
city = st.text_input("City name", "London")
# Radio button
unit = st.radio('Unit of temperature', ('Celsius', 'Fahrenheit'))


# Display data to the user
if city:
    # Get current weather data
    data, general, icon = fetch_current_weather_data(city, unit)

    # Get hourly forecast
    hour_data, unit_key = fetch_hourly_weather_data(city, unit)

    if data and general and icon and hour_data is not None:
        # Success Box
        st.success("Weather data fetched successfully!")

        # Display city to user
        st.header(str.title(city))

        # Current Temperature Data Frame
        temperature_data = {
            "Temperature": ["Temperature", "Feals Like", "Min", "Max"],
            "Degrees" : [data['main']['temp'],
            data['main']['feels_like'],
            data['main']['temp_min'],
            data['main']['temp_max']],
        }

        # Other Current Weather Data Frame
        weather_data = {
            "Pressure": data['main']['pressure'],
            "Humidity": data['main']['humidity'],
            "Wind Speed": data['wind']['speed'],
            "Weather": data['weather'][0]['main'],
            "General": general
        }

        # Hourly Temperature Data Frame
        hourly_data = {
            "Hour" : ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
                      "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
                      "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
                      "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
            "Degrees": [hour_data[0][unit_key], hour_data[1][unit_key],
                        hour_data[2][unit_key], hour_data[3][unit_key],
                        hour_data[4][unit_key], hour_data[5][unit_key],
                        hour_data[6][unit_key], hour_data[7][unit_key],
                        hour_data[8][unit_key], hour_data[9][unit_key],
                        hour_data[10][unit_key], hour_data[11][unit_key],
                        hour_data[12][unit_key], hour_data[13][unit_key],
                        hour_data[14][unit_key], hour_data[15][unit_key],
                        hour_data[16][unit_key], hour_data[17][unit_key],
                        hour_data[18][unit_key], hour_data[19][unit_key],
                        hour_data[20][unit_key], hour_data[21][unit_key],
                        hour_data[22][unit_key], hour_data[23][unit_key]]
        }

        # Create data frames
        df_other = pd.DataFrame(weather_data, index=[0])
        df_temperature = pd.DataFrame(temperature_data)
        df_hour = pd.DataFrame(hourly_data)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Your Weather At A Glance")
            # Display Weather Icon
            st.image(icon, caption='Current Weather Icon')
            # Display weather data
            st.info("Current Weather: " + str(df_other["Weather"][0]))
            st.info("Current temperature: " + str(df_temperature["Degrees"][0]))
            st.info("Feels like: " + str(df_temperature["Degrees"][1]))
            st.info("Humidity: " + str(df_other["Humidity"][0]))
            st.info("Wind speed: " + str(df_other["Wind Speed"][0]))


        with col2:
            # Button
            button = st.button("Show me a map")
            if button:
                # Map
                coordinates_df = pd.DataFrame({'lat': [data['coord']['lat']], 'lon': [data['coord']['lon']]})
                st.map(coordinates_df)
            st.info("Pressure: " + str(df_other["Pressure"][0]))

        # Checkbox
        cbox = st.checkbox("Show me the weather in more detail")
        if cbox:
            # Selectbox
            options = st.selectbox("Select Charts",
                                   ("1: Daily Temperature Bar Chart", "2: Hourly Temperature Line Graph",
                                    "3: Both"))
            # Color Picker
            clr = st.color_picker('Chart Color Selector', '#00f900')
        # Interactive Table
        #st.dataframe(df_general)
        if cbox:
            st.subheader("Today's Weather In Charts")

            # Bar chart
            if options[0] == "1" or options[0] == "3":
                bar_chart = alt.Chart(df_temperature).mark_bar().encode(
                    x = "Temperature",
                    y = "Degrees",
                    color = alt.value(clr)
                )
                st.altair_chart(bar_chart, use_container_width=True)

            # Line chart
            if options[0] == "2" or options[0] == "3":
                st.subheader("Weather By The Hour")
                fig = px.line(df_hour,
                                  x=df_hour["Hour"],
                                  y=df_hour["Degrees"]
                                  )
                fig.update_traces(line_color=clr)
                st.plotly_chart(fig, use_container_width=True)
            sl = st.slider("Show tables", 0,1)
            col1, col2 = st.columns(2)
            with col1:
                if sl == 1:
                    st.dataframe(temperature_data, use_container_width=True)
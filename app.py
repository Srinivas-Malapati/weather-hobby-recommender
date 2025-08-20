import streamlit as st
import pandas as pd

# ===== Function to check if weather is good =====
def is_good_weather(description):
    description = description.lower()
    good_keywords = [
        "clear",
        "sunny",
        "few clouds",
        "scattered clouds",
        "partly cloudy",
        "mostly sunny"
    ]
    for keyword in good_keywords:
        if keyword in description:
            return True
    return False

# ===== Load datasets =====
df_weather = pd.read_csv("weather_data.csv")  # Columns: location, description
df_hobbies = pd.read_csv("hobbies_master.csv")  # Columns: hobby, type (indoor/outdoor)

# ===== Streamlit UI =====
st.title("🌤️ Weather-Based Hobby Recommender")

# Dropdown for city selection
city_options = df_weather["City"].unique()
user_city = st.selectbox("Select your city", city_options)

# Find weather for selected city
location_match = df_weather[df_weather["City"] == user_city]

if not location_match.empty:
    condition = location_match.iloc[0]["Description"]
    st.write(f"### Weather in {user_city}: {condition.capitalize()}")

    if is_good_weather(condition):
        st.success("Good weather for outdoor activities!")
        outdoor_hobbies = df_hobbies[df_hobbies["type"].str.lower() == "outdoor"]["hobby"].tolist()
        if outdoor_hobbies:
            st.write("**Suggested outdoor hobbies:**")
            for hobby in outdoor_hobbies:
                st.write(f"- {hobby}")
        else:
            st.write("No outdoor hobbies available.")
    else:
        st.warning("Weather not suitable for outdoor activities. Consider indoor hobbies.")
        indoor_hobbies = df_hobbies[df_hobbies["type"].str.lower() == "indoor"]["hobby"].tolist()
        if indoor_hobbies:
            st.write("**Suggested indoor hobbies:**")
            for hobby in indoor_hobbies:
                st.write(f"- {hobby}")
        else:
            st.write("No indoor hobbies available.")
else:
    st.error(f"No weather data available for '{user_city}'.")

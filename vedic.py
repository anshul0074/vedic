import streamlit as st
from vedicastro.VedicAstro import VedicHoroscopeData
import polars as pl

st.title("Vedic Horoscope Generator 💫")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    day = st.number_input("Birth Day", min_value=1, max_value=31, step=1)
    month = st.number_input("Birth Month", min_value=1, max_value=12, step=1)
    year = st.number_input("Birth Year", min_value=1900, max_value=2100, step=1)
with col2:
    hour = st.number_input("Birth Hour (24h format)", min_value=0, max_value=23, step=1)
    minute = st.number_input("Birth Minute", min_value=0, max_value=59, step=1)
latitude = st.number_input("Latitude", value=30.9084)
longitude = st.number_input("Longitude", value=77.0999)
utc = "5:30"

if st.button("Generate Horoscope"):
    ayan = "Lahiri"
    house_system = "Placidus"

    vhd = VedicHoroscopeData(
        year=year, month=month, day=day, hour=hour-2, minute=minute, second=0,
        utc=utc, latitude=latitude, longitude=longitude, ayanamsa=ayan, house_system=house_system
    )
    chart = vhd.generate_chart()
    planet_in_house = vhd.get_planet_in_house(houses_chart=chart, planets_chart=chart)
    planets_data = vhd.get_planets_data_from_chart(chart)
    planets_df = pl.DataFrame(planets_data).slice(1)  # Drop first row

    st.write(f"**Position of Saturn:** {planet_in_house['Saturn'] % 12}")
    st.write(f"**Position of Gulika:** {(planet_in_house['Saturn'] + 7) % 12}")
    st.dataframe(planets_df.to_pandas())

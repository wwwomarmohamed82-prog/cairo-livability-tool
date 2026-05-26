import osmnx
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

st.title("Livability Score Calculator")
st.text("Enter a city to calculate its livability score based on the presence of amenities such as hospitals, schools, banks, parking, and police stations.")
searchable = st.text_input("Enter your city")
@st.cache_data
def get_data(place):
    return osmnx.features.features_from_place(place, {"amenity": True})
if searchable:
    try:
        output = get_data(searchable)
        # rest of your code continues here
    except Exception as e:
        st.error(f"Could not find '{searchable}'...")
    output = get_data(searchable)
    maincount = output["amenity"].value_counts()
    weights = {"hospital": 3, "school": 3, "bank": 2, "parking": 1, "police": 1}
    filtered = output[output["amenity"].isin(weights.keys())]
    score = 0
    for item in weights:
        rawscore = maincount.get(item, 0) * weights[item]
        st.write(f"{item}: {rawscore}")
        score += rawscore
    final_score = (score / 1000) * 100
    st.metric("Livability Score", f"{final_score:.1f} / 100")
    locate=output["geometry"].centroid
    longmean= locate.x.mean()
    latmean=locate.y.mean()
    osmmap=folium.Map(location=[latmean, longmean])
    for index, row in filtered.iterrows():
        popup = row.get("name:en") or row.get("name:ar") or row.get("amenity") or "Unknown"
        folium.Marker(location=[locate[index].y, locate[index].x], popup=popup).add_to(osmmap)
    st_folium(osmmap, width=700)
import osmnx
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

st.title("Livability Score Calculator")
st.text("Enter a city to calculate its livability score based on the presence of amenities such as hospitals, schools, banks, parking, and police stations.")
searchable = st.text_input("Enter your city")
if searchable:
    output = osmnx.features.features_from_place(searchable, {"amenity":True})
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
        popup = row["name:en"] if pd.notna(row["name:en"]) else (row["name:ar"] if pd.notna(row["name:ar"]) else row["amenity"])
        folium.Marker(location=[locate[index].y, locate[index].x], popup=popup).add_to(osmmap)
    st_folium(osmmap, width=700)
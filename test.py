import osmnx
import pandas as pd
import folium
searchable=input("enter your city") 
output = osmnx.features.features_from_place(searchable, {"amenity":True})
maincount=output["amenity"].value_counts()
weights = {"hospital": 3, "school": 3, "bank": 2, "parking": 1, "police": 1}
score = 0
for item in weights:
    rawscore=maincount[item] * weights[item]
    print(f"{item}: {rawscore}")
    score = score + rawscore
final_score = (score / 1000) * 100
print(f"\n Livability Score for {searchable}: {final_score:.1f} / 100")
locate=output["geometry"].centroid
longmean= locate.x.mean()
latmean=locate.y.mean()
osmmap=folium.Map(location=[latmean, longmean])
for index, row in output.iterrows():
    popup = row["name:en"] if pd.notna(row["name:en"]) else (row["name:ar"] if pd.notna(row["name:ar"]) else row["amenity"])
    folium.Marker(location=[locate[index].y, locate[index].x], popup=popup).add_to(osmmap)
osmmap.save("index.html")
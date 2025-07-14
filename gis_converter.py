import streamlit as st
import geopandas as gpd
from shapely.geometry import Point

CRS_OPTIONS = {
    "WGS84 (Lat/Lon)": "EPSG:4326",
    "UTM Zone 38N": "EPSG:32638",
    "QND95 / Qatar National Grid": "EPSG:28600",
    "Web Mercator": "EPSG:3857"
}

st.set_page_config(page_title="GIS Coordinate Converter", layout="centered")
st.title("📍 GIS Coordinate Converter")

st.markdown("### ➤ Step 1: Select Input Coordinate Type")
input_crs_label = st.selectbox("Input Coordinate System", list(CRS_OPTIONS.keys()))
input_crs = CRS_OPTIONS[input_crs_label]

st.markdown("### ➤ Step 2: Select Output Coordinate Type")
output_crs_label = st.selectbox("Output Coordinate System", list(CRS_OPTIONS.keys()))
output_crs = CRS_OPTIONS[output_crs_label]

st.markdown("### ➤ Step 3: Enter Coordinates")
col1, col2 = st.columns(2)
with col1:
    lon = st.number_input("Longitude / X", value=51.531)
with col2:
    lat = st.number_input("Latitude / Y", value=25.285)

if st.button("Convert Coordinates"):
    try:
        gdf = gpd.GeoDataFrame(
            geometry=[Point(lon, lat)],
            crs=input_crs
        )
        gdf_converted = gdf.to_crs(output_crs)
        new_point = gdf_converted.geometry.iloc[0]

        st.success("✅ Conversion Successful!")
        st.markdown(f"**Converted Coordinates:**")
        st.code(f"X: {new_point.x:.6f}, Y: {new_point.y:.6f}", language="text")

    except Exception as e:
        st.error(f"⚠️ Conversion failed: {e}")

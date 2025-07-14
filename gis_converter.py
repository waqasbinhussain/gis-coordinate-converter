print ("hello word")
import streamlit as st
from pyproj import Transformer

# Predefined CRS codes (more can be added)
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
    lon = st.number_input("Longitude / X", value=51.531)  # Default: Doha
with col2:
    lat = st.number_input("Latitude / Y", value=25.285)

if st.button("Convert Coordinates"):
    try:
        transformer = Transformer.from_crs(input_crs, output_crs, always_xy=True)
        x_new, y_new = transformer.transform(lon, lat)

        st.success("✅ Conversion Successful!")
        st.markdown(f"**Converted Coordinates:**")
        st.code(f"X: {x_new:.6f}, Y: {y_new:.6f}", language="text")

    except Exception as e:
        st.error(f"⚠️ Conversion failed: {e}")

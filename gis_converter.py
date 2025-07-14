import streamlit as st
import requests
import re

st.set_page_config(page_title="GIS Coordinate Converter", layout="centered")
st.title("📍 GIS Coordinate Converter (via EPSG.io API)")

CRS_OPTIONS = {
    "WGS84 (EPSG:4326)": 4326,
    "Web Mercator (EPSG:3857)": 3857,
    "QND95 / Qatar (EPSG:28600)": 28600,
    "UTM Zone 38N (EPSG:32638)": 32638
}

input_crs_label = st.selectbox("Input Coordinate System", list(CRS_OPTIONS.keys()))
output_crs_label = st.selectbox("Output Coordinate System", list(CRS_OPTIONS.keys()))

input_epsg = CRS_OPTIONS[input_crs_label]
output_epsg = CRS_OPTIONS[output_crs_label]

col1, col2 = st.columns(2)
with col1:
    x = st.number_input("Longitude / Easting (X)", value=51.531)
with col2:
    y = st.number_input("Latitude / Northing (Y)", value=25.285)

if st.button("Convert Coordinates"):
    try:
        url = f"https://epsg.io/trans?x={x}&y={y}&s_srs={input_epsg}&t_srs={output_epsg}"
        response = requests.get(url)
        content = response.text

        # Extract from the HTML response
        match = re.search(r'<input[^>]*id="x"[^>]*value="([-.\d]+)"', content)
        x_out = match.group(1) if match else None

        match = re.search(r'<input[^>]*id="y"[^>]*value="([-.\d]+)"', content)
        y_out = match.group(1) if match else None

        if x_out and y_out:
            st.success("✅ Conversion Successful!")
            st.code(f"Converted X: {float(x_out):.6f}, Y: {float(y_out):.6f}")
        else:
            st.error("❌ Could not extract converted coordinates. Try different EPSG types.")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

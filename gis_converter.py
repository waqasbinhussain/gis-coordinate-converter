
import streamlit as st
import pandas as pd
from pyproj import Transformer

CRS_OPTIONS = {
    "WGS84 (Lat/Lon, EPSG:4326)": "EPSG:4326",
    "Web Mercator (EPSG:3857)": "EPSG:3857",
    "UTM Zone 38N (EPSG:32638)": "EPSG:32638",
    "QND95 / Qatar National Grid (EPSG:28600)": "EPSG:28600"
}

st.set_page_config(page_title="GIS Coordinate Converter", layout="centered")
st.title("📍 GIS Coordinate Converter")

input_label = st.selectbox("Input CRS", list(CRS_OPTIONS.keys()))
input_crs = CRS_OPTIONS[input_label]

output_label = st.selectbox("Output CRS", list(CRS_OPTIONS.keys()))
output_crs = CRS_OPTIONS[output_label]

st.divider()

st.markdown("### 📝 Convert a Single Coordinate")
col1, col2 = st.columns(2)
with col1:
    x = st.number_input("Longitude / Easting (X)", value=51.531)
with col2:
    y = st.number_input("Latitude / Northing (Y)", value=25.285)

if st.button("Convert Single Point"):
    try:
        transformer = Transformer.from_crs(input_crs, output_crs, always_xy=True)
        x_out, y_out = transformer.transform(x, y)
        st.success("✅ Converted Successfully")
        st.code(f"X: {x_out:.6f}, Y: {y_out:.6f}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

st.divider()

st.markdown("### 📤 Upload a CSV File (with columns: x, y)")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if not {'x', 'y'}.issubset(df.columns):
            st.error("CSV must contain 'x' and 'y' columns.")
        else:
            transformer = Transformer.from_crs(input_crs, output_crs, always_xy=True)
            df['x_converted'], df['y_converted'] = zip(*df.apply(
                lambda row: transformer.transform(row['x'], row['y']), axis=1))

            st.success("✅ File Converted Successfully")
            st.dataframe(df)

            csv_out = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Converted CSV", csv_out, file_name="converted_coordinates.csv", mime='text/csv')
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Developed by <b>Waqas Bin Hussain</b><br>"
    "<a href='https://www.linkedin.com/in/waqasbinhussain/' target='_blank' style='text-decoration: none; color: #0a66c2;'>🔗 Connect on LinkedIn</a></p>",
    unsafe_allow_html=True
)

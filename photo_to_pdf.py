import streamlit as st
from PIL import Image
import io

# 🎯 Target size (1 MB)
TARGET_SIZE = 1 * 1024 * 1024   
pdf_filename = "compressed_output.pdf"

st.title("📄 Image to Compressed PDF (≤1 MB)")
st.write("Upload an image and download it as a compressed PDF under 1 MB.")

# 1️⃣ Upload image
uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image
    img = Image.open(uploaded_file).convert("RGB")

    # 2️⃣ Compress & Save as PDF
    quality = 95
    step = 5
    compressed_pdf = None

    while quality > 5:
        buffer = io.BytesIO()
        img.save(buffer, "PDF", quality=quality, optimize=True)
        size = buffer.getbuffer().nbytes

        if size <= TARGET_SIZE:
            compressed_pdf = buffer.getvalue()
            break
        quality -= step

    if compressed_pdf is None:  # fallback if not under 1 MB
        buffer = io.BytesIO()
        img.save(buffer, "PDF", quality=5, optimize=True)
        compressed_pdf = buffer.getvalue()
        st.warning("⚠️ Could not reach target size. Downloading smallest possible file.")

    st.success(f"✅ PDF ready! Final size: {len(compressed_pdf)/2024:.1f} KB")

    # 3️⃣ Download button
    st.download_button(
        label="📥 Download Compressed PDF",
        data=compressed_pdf,
        file_name=pdf_filename,
        mime="application/pdf"
    )

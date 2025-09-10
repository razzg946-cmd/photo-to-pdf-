import streamlit as st
from PIL import Image
import io

# 🎯 Target size (2 MB)
TARGET_SIZE = 2 * 1024 * 1024   
pdf_filename = "compressed_output.pdf"

st.title("📄 Image to PDF (~2 MB, Clear Output)")
st.write("Upload an image. If it's small or blurry, the app will upscale it to produce a clear PDF around 2 MB.")

# 1️⃣ Upload image
uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open image
    img = Image.open(uploaded_file).convert("RGB")

    # 🔹 Step 1: Upscale small images
    min_size = 2000  # minimum width/height
    if img.width < min_size or img.height < min_size:
        scale = max(min_size / img.width, min_size / img.height)
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)
        st.info(f"🔍 Image upscaled to {new_size} for clarity.")

    # 🔹 Step 2: Save PDF & adjust quality
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

    # If still larger/smaller, force save with high quality
    if compressed_pdf is None:
        buffer = io.BytesIO()
        img.save(buffer, "PDF", quality=95, optimize=True)
        compressed_pdf = buffer.getvalue()

    st.success(f"✅ PDF ready! Final size: {len(compressed_pdf)/1024:.1f} KB")

    # 3️⃣ Download button
    st.download_button(
        label="📥 Download PDF (~2 MB)",
        data=compressed_pdf,
        file_name=pdf_filename,
        mime="application/pdf"
    )

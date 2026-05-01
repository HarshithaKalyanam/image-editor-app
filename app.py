import streamlit as st
from PIL import Image
import cv2
import filters
import utils
import io

st.set_page_config(page_title="Image Editor", page_icon="🖼️", layout="wide")

st.title("🖼️ Image Editing App")
st.markdown("### Upload an image and apply filters like blur, sharpness, edge detection, and more.")

st.markdown("## 🎨 Advanced Image Editor using Streamlit + OpenCV")

# Sidebar controls
st.sidebar.header("Controls")

blur_val = st.sidebar.slider("Blur", 1, 21, 1, step=2)
sharp_val = st.sidebar.slider("Sharpness", 0.0, 3.0, 0.0)
brightness_val = st.sidebar.slider("Brightness", -100, 100, 0)
contrast_val = st.sidebar.slider("Contrast", 0.5, 3.0, 1.0)

edge_toggle = st.sidebar.checkbox("Edge Detection")
t1 = st.sidebar.slider("Threshold 1", 0, 255, 100, disabled=not edge_toggle)
t2 = st.sidebar.slider("Threshold 2", 0, 255, 200, disabled=not edge_toggle)

gray_toggle = st.sidebar.checkbox("Grayscale")

rotate_val = st.sidebar.slider("Rotate Image", -180, 180, 0)
resize_val = st.sidebar.slider("Resize (%)", 10, 200, 100)
text = st.sidebar.text_input("Add Text on Image")

flip_option = st.sidebar.selectbox("Flip", ["None", "Horizontal", "Vertical"])
sepia_toggle = st.sidebar.checkbox("Sepia Filter")
cartoon_toggle = st.sidebar.checkbox("Cartoon Effect")

reset_btn = st.sidebar.button("🔄 Reset Image")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

# ================= MAIN =================
if uploaded_file:
    image = Image.open(uploaded_file)
    img = utils.pil_to_cv2(image)

    # ✅ Resize large image (performance)
    if img.shape[1] > 800:
        scale = 800 / img.shape[1]
        img = cv2.resize(img, None, fx=scale, fy=scale)

    # 🔄 Resize slider
    scale = resize_val / 100
    img = cv2.resize(img, None, fx=scale, fy=scale)

    # 🔄 Rotate
    if rotate_val != 0:
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, rotate_val, 1.0)
        img = cv2.warpAffine(img, M, (w, h))

    # 🔄 Flip
    if flip_option == "Horizontal":
        img = cv2.flip(img, 1)
    elif flip_option == "Vertical":
        img = cv2.flip(img, 0)

    # 🔄 Reset Logic
    if reset_btn:
        processed = img.copy()
    else:
        processed = img.copy()

        # 🎨 Basic Filters
        if blur_val > 1:
            processed = filters.apply_blur(processed, blur_val)

        if sharp_val > 0:
            processed = filters.apply_sharpness(processed, sharp_val)

        processed = filters.adjust_brightness(processed, brightness_val)
        processed = filters.adjust_contrast(processed, contrast_val)

        if gray_toggle:
            processed = filters.to_grayscale(processed)

        if edge_toggle:
            processed = filters.edge_detection(processed, t1, t2)

        # 🎨 Advanced Filters
        if sepia_toggle:
            processed = filters.sepia(processed)

        if cartoon_toggle:
            processed = filters.cartoon(processed)

        # 📝 Text
        if text:
            cv2.putText(processed, text, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)

    processed_pil = utils.cv2_to_pil(processed)

    # 🖼️ Display
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Original Image")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("✨ Edited Image")
        st.image(processed_pil, use_container_width=True)

    # 📥 Download
    buf = io.BytesIO()
    processed_pil.save(buf, format="PNG")

    st.download_button(
        label="⬇️ Download Image",
        data=buf.getvalue(),
        file_name="edited.png",
        mime="image/png"
    )
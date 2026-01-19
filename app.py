import streamlit as st
import os
import time
import json
from executable import extract_from_document

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
    .confidence-score {
        font-size: 1.2em;
        font-weight: bold;
        color: #FF9800;
    }
    .field-item {
        margin-bottom: 10px;
        padding: 5px;
        background-color: #ffffff;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Sidebar
st.sidebar.title("📋 Instructions")
st.sidebar.markdown("""
1. Upload a PNG, JPG, or JPEG image of a document.
2. The AI will extract key fields using OCR.
3. View the results below with confidence scores.
""")
st.sidebar.markdown("---")
st.sidebar.markdown("**Supported Formats:** PNG, JPG, JPEG")
st.sidebar.markdown("**Processing:** Automatic OCR and field extraction")

# Main content
st.markdown('<h1 class="main-header">🚀 Intelligent Document AI</h1>', unsafe_allow_html=True)
st.markdown("Upload your document image and let AI extract the key information automatically!")

uploaded_file = st.file_uploader("📤 Choose an image file", type=["png", "jpg", "jpeg"], help="Select a document image to process")

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📄 Uploaded Document")
        st.image(file_path, caption=f"File: {uploaded_file.name}", use_column_width=True)

    with col2:
        st.subheader("⚙️ Processing")
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("Initializing OCR...")
        progress_bar.progress(25)
        time.sleep(0.5)

        status_text.text("Running OCR analysis...")
        progress_bar.progress(50)
        time.sleep(0.5)

        status_text.text("Extracting fields...")
        progress_bar.progress(75)
        time.sleep(0.5)

        start_time = time.time()
        result = extract_from_document(file_path)
        processing_time = time.time() - start_time

        progress_bar.progress(100)
        status_text.text("✅ Processing complete!")
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()

        st.success(f"🎉 Processing completed in {processing_time:.2f} seconds!")

    # Results section
    st.markdown("---")
    st.subheader("📊 Extraction Results")

    # Confidence Score
    st.subheader("📈 Confidence Score")
    confidence = result["confidence_score"]
    
    if confidence >= 0.8:
        st.success(f"🟢 High Confidence: {confidence:.2f}")
    elif confidence >= 0.6:
        st.warning(f"🟡 Medium Confidence: {confidence:.2f}")
    else:
        st.error(f"🔴 Low Confidence: {confidence:.2f}")
    
    st.progress(confidence)
    st.caption("Visual confidence meter - filled portion shows reliability level")

    # Extracted Fields
    st.markdown('<div class="result-card"><h3>Extracted Fields</h3>', unsafe_allow_html=True)
    fields = result["fields"]
    st.json(fields)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download results
    result_json = json.dumps(result, indent=4)
    st.download_button(
        label="📥 Download Results as JSON",
        data=result_json,
        file_name=f"extraction_results_{uploaded_file.name}.json",
        mime="application/json"
    )

else:
    st.info("👆 Please upload an image file to get started!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and PaddleOCR")

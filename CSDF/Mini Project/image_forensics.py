import io
import json
import hashlib
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image, ExifTags, ImageChops, ImageEnhance, UnidentifiedImageError

st.set_page_config(page_title="Image Forensics Tool", page_icon="🔎", layout="wide")
st.title("🔎 Image Forensics Tool")
st.caption("A beginner-friendly Python mini project for examining image metadata and compression characteristics.")

st.warning(
    "Educational aid only. These checks cannot prove that an image is authentic or manipulated. "
    "Results depend on image format, editing history, and compression."
)

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "bmp", "tif", "tiff"])

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def safe_exif(image):
    output = {}
    try:
        exif = image.getexif()
        for key, value in exif.items():
            name = ExifTags.TAGS.get(key, str(key))
            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="replace")
            output[name] = str(value)
    except Exception:
        pass
    return output

def make_ela(image, quality=90):
    # ELA is most interpretable for JPEGs; for other formats, treat this as a rough recompression comparison.
    rgb = image.convert("RGB")
    buffer = io.BytesIO()
    rgb.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    recompressed = Image.open(buffer).convert("RGB")
    diff = ImageChops.difference(rgb, recompressed)
    extrema = diff.getextrema()
    max_diff = max(channel[1] for channel in extrema) or 1
    scale = 255.0 / max_diff
    return ImageEnhance.Brightness(diff).enhance(scale)

if uploaded is not None:
    raw = uploaded.getvalue()
    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except (UnidentifiedImageError, OSError):
        st.error("The uploaded file could not be read as a supported image.")
        st.stop()

    exif = safe_exif(image)
    width, height = image.size
    file_size = len(raw)

    st.subheader("1. Image overview")
    left, right = st.columns([1, 1])
    with left:
        st.image(image, caption="Uploaded image", use_container_width=True)
    with right:
        st.metric("Dimensions", f"{width} × {height}")
        st.metric("File size", f"{file_size / 1024:.1f} KB")
        st.write(f"**Format:** {image.format or 'Unknown'}")
        st.write(f"**Color mode:** {image.mode}")
        st.write(f"**SHA-256:** `{sha256_bytes(raw)}`")

    st.subheader("2. Metadata (EXIF)")
    if exif:
        st.dataframe(
            [{"Field": key, "Value": value} for key, value in exif.items()],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No EXIF metadata was found. Metadata may have been removed by an app, website, or export process; this alone does not indicate manipulation.")

    st.subheader("3. RGB color histogram")
    rgb = image.convert("RGB")
    pixels = np.asarray(rgb)
    fig, ax = plt.subplots()
    for channel, label in enumerate(("Red", "Green", "Blue")):
        histogram, bins = np.histogram(pixels[:, :, channel], bins=256, range=(0, 256))
        ax.plot(bins[:-1], histogram, label=label)
    ax.set_title("RGB intensity distribution")
    ax.set_xlabel("Pixel intensity")
    ax.set_ylabel("Pixel count")
    ax.legend()
    ax.grid(alpha=0.2)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("4. Error Level Analysis (ELA)")
    st.write(
        "The tool recompresses the image as JPEG and highlights pixel differences. "
        "Bright or uneven areas can be worth examining, but they may also come from textures, edges, resizing, "
        "or normal compression. ELA is not a definitive manipulation detector."
    )
    quality = st.slider("JPEG recompression quality", min_value=70, max_value=95, value=90)
    ela = make_ela(image, quality)
    st.image(ela, caption=f"ELA visualization (JPEG quality {quality})", use_container_width=True)

    st.subheader("5. Basic findings")
    findings = {
        "filename": Path(uploaded.name).name,
        "analysis_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "format": image.format,
        "width": width,
        "height": height,
        "color_mode": image.mode,
        "file_size_bytes": file_size,
        "sha256": sha256_bytes(raw),
        "exif_metadata": exif,
        "notes": [
            "No automated authenticity verdict is made.",
            "Missing EXIF data is not proof of tampering.",
            "ELA patterns are clues for human review, not proof of manipulation."
        ]
    }
    st.json(findings)
    report = json.dumps(findings, indent=2, ensure_ascii=False).encode("utf-8")
    st.download_button(
        "Download findings report (JSON)",
        data=report,
        file_name="image_forensics_report.json",
        mime="application/json",
    )
else:
    st.info("Upload an image above to begin the analysis.")
    st.markdown(
        """
        **What this mini project demonstrates**
        - Reading image properties and metadata
        - Computing a SHA-256 hash to identify the exact file analyzed
        - Plotting RGB intensity histograms
        - Creating an ELA visualization
        - Exporting a structured report
        """
    )

"""running process:
1. Create a virtual env: python -m venv .venv
2. Start venv venv\Scripts\activate
3. Install requirements: pip install -r requirements.txt
4. Run app: streamlit run image_forensics.py"""

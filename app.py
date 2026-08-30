import os
import json
import streamlit as st
from google import genai
from google.genai import types

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ArtisanLink AI",
    page_icon="🧵",
    layout="wide"
)

# ============================================================
# API CONFIG
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

# ============================================================
# AI PRODUCT ANALYSIS
# ============================================================

def analyze_product(image_bytes, mime_type):

    client = genai.Client(api_key=API_KEY)

    prompt = """
You are an AI assistant for an Indian artisan marketplace.

Analyze the uploaded product image carefully.

The product must be classified into ONE of these categories:

- Pottery
- Bamboo Handicraft
- Traditional Textile
- Jewellery
- Wooden Handicraft
- Leather Product
- Other

Return ONLY valid JSON.

Required format:

{
    "category": "Pottery",
    "product_name": "Traditional Handmade Clay Pot",
    "material": "Clay",
    "craft_type": "Traditional pottery",
    "description": "A short professional marketplace description.",
    "confidence": 95,
    "keywords": ["handmade", "pottery", "artisan"],
    "target_markets": ["Home Decor", "Tourist Market"],
    "suggested_price": 850
}

IMPORTANT:

1. Look at the actual image.
2. Do NOT randomly select a category.
3. If it is clearly bamboo, select Bamboo Handicraft.
4. If it is clearly pottery, select Pottery.
5. If it is clearly textile, select Traditional Textile.
6. Confidence must be between 0 and 100.
7. Price must be in Indian Rupees.
8. Keep the description suitable for an online marketplace.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            ),
            prompt
        ]
    )

    text = response.text.strip()

    # Remove markdown formatting if returned
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🧵 ArtisanLink AI")

    st.caption("SIH26090 Prototype")

    st.divider()

    st.subheader("AI Features")

    st.write("📸 Product Recognition")
    st.write("✨ AI Product Analysis")
    st.write("📝 Smart Catalogue")
    st.write("🌐 Multilingual Listing")
    st.write("💰 Dynamic Pricing")
    st.write("🎯 Market Linkage")
    st.write("🤝 Buyer Matching")

    st.divider()

    st.success("AI/ML Prototype Ready")


# ============================================================
# HEADER
# ============================================================

st.title("🧵 ArtisanLink AI")

st.subheader(
    "AI-Powered Digital Business Assistant for Artisans"
)

st.write(
    """
Transform a simple artisan product photo into a
professional digital marketplace listing using AI.
"""
)

st.divider()


# ============================================================
# DASHBOARD
# ============================================================

st.header("📊 Artisan Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Products Listed", "24")
c2.metric("Catalogue Ready", "18")
c3.metric("Markets", "7")
c4.metric("Potential Buyers", "126")

st.divider()


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.header("📸 Upload Artisan Product")

uploaded_file = st.file_uploader(
    "Upload a clear product image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:

    image_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type

    left, right = st.columns(2)

    with left:

        st.subheader("Product Image")

        st.image(
            image_bytes,
            use_container_width=True
        )

    with right:

        st.subheader("AI Recognition")

        st.write(
            "Click below to identify the artisan product."
        )

        analyze_button = st.button(
            "🤖 Analyze Product",
            type="primary",
            use_container_width=True
        )

    # ========================================================
    # ANALYZE
    # ========================================================

    if analyze_button:

        if not API_KEY:

            st.error(
                "GEMINI_API_KEY is missing."
            )

        else:

            with st.spinner(
                "AI is analyzing the product..."
            ):

                try:

                    result = analyze_product(
                        image_bytes,
                        mime_type
                    )

                    st.session_state["product"] = result

                    st.success(
                        "✅ Product analyzed successfully!"
                    )

                except json.JSONDecodeError:

                    st.error(
                        "AI returned an unexpected format. "
                        "Please try the image again."
                    )

                except Exception as e:

                    st.error(
                        f"AI analysis failed: {e}"
                    )


# ============================================================
# PRODUCT RESULT
# ============================================================

if "product" in st.session_state:

    product = st.session_state["product"]

    st.divider()

    st.header("🤖 AI Product Recognition")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Category",
            product.get("category", "Unknown")
        )

    with c2:

        st.metric(
            "Material",
            product.get("material", "Unknown")
        )

    with c3:

        confidence = product.get(
            "confidence",
            0
        )

        st.metric(
            "AI Confidence",
            f"{confidence}%"
        )

    st.success(
        f"Detected Product: **{product.get('product_name', 'Unknown')}**"
    )


    # ========================================================
    # CATALOGUE
    # ========================================================

    st.divider()

    st.header("📝 AI Generated Catalogue")

    st.subheader(
        product.get(
            "product_name",
            "Artisan Product"
        )
    )

    st.write(
        product.get(
            "description",
            ""
        )
    )

    c1, c2 = st.columns(2)

    with c1:

        st.write(
            "**Material:**",
            product.get(
                "material",
                "Unknown"
            )
        )

    with c2:

        st.write(
            "**Craft Type:**",
            product.get(
                "craft_type",
                "Traditional craft"
            )
        )

    st.write("### 🔎 Keywords")

    keywords = product.get(
        "keywords",
        []
    )

    if keywords:

        st.write(
            " • ".join(keywords)
        )


    # ========================================================
    # MULTILINGUAL
    # ========================================================

    st.divider()

    st.header("🌐 Multilingual Listing")

    language = st.selectbox(
        "Select language",
        [
            "English",
            "Hindi",
            "Kannada"
        ]
    )

    if language == "English":

        st.info(
            product.get(
                "description",
                ""
            )
        )

    elif language == "Hindi":

        st.info(
            "यह एक पारंपरिक हस्तनिर्मित उत्पाद है "
            "जिसे कुशल कारीगरों द्वारा बनाया गया है।"
        )

    elif language == "Kannada":

        st.info(
            "ಇದು ನುರಿತ ಕುಶಲಕರ್ಮಿಗಳು ತಯಾರಿಸಿದ "
            "ಸಾಂಪ್ರದಾಯಿಕ ಕೈಯಿಂದ ಮಾಡಿದ ಉತ್ಪನ್ನವಾಗಿದೆ."
        )


    # ========================================================
    # PRICING
    # ========================================================

    st.divider()

    st.header("💰 Dynamic Pricing Assistant")

    c1, c2 = st.columns(2)

    with c1:

        material_cost = st.number_input(
            "Raw Material Cost (₹)",
            min_value=0,
            value=300,
            step=50
        )

    with c2:

        labour_cost = st.number_input(
            "Labour Cost (₹)",
            min_value=0,
            value=400,
            step=50
        )

    c1, c2 = st.columns(2)

    with c1:

        profit_margin = st.slider(
            "Profit Margin (%)",
            10,
            100,
            30
        )

    with c2:

        demand_factor = st.slider(
            "Market Demand",
            0.8,
            1.5,
            1.0,
            0.1
        )

    base_cost = (
        material_cost +
        labour_cost
    )

    calculated_price = (
        base_cost *
        (1 + profit_margin / 100) *
        demand_factor
    )

    ai_price = product.get(
        "suggested_price",
        calculated_price
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "AI Suggested Price",
            f"₹{ai_price:,.0f}"
        )

    with c2:

        st.metric(
            "Cost + Margin Price",
            f"₹{calculated_price:,.0f}"
        )


    # ========================================================
    # MARKET LINKAGE
    # ========================================================

    st.divider()

    st.header("🎯 AI Market Linkage")

    st.write(
        "Recommended markets based on the product:"
    )

    markets = product.get(
        "target_markets",
        []
    )

    if markets:

        for market in markets:

            st.success(
                f"✓ {market}"
            )

    else:

        st.info(
            "No specific markets generated."
        )


    # ========================================================
    # BUYER MATCHING
    # ========================================================

    st.divider()

    st.header("🤝 Potential Buyer Matching")

    buyers = [
        (
            "Heritage Handicrafts",
            "Delhi",
            "92%"
        ),
        (
            "Indian Artisan Store",
            "Mumbai",
            "88%"
        ),
        (
            "EcoCraft Retail",
            "Bengaluru",
            "85%"
        )
    ]

    for buyer, city, score in buyers:

        c1, c2, c3 = st.columns(3)

        with c1:

            st.write(
                f"**{buyer}**"
            )

        with c2:

            st.write(city)

        with c3:

            st.success(
                f"Match {score}"
            )


    # ========================================================
    # FINAL LISTING
    # ========================================================

    st.divider()

    st.header("🚀 Marketplace Listing")

    if st.button(
        "Publish AI Generated Listing",
        type="primary",
        use_container_width=True
    ):

        st.success(
            "🎉 Product successfully prepared for marketplace publishing!"
        )

        st.balloons()

else:

    st.info(
        "👆 Upload an artisan product image to begin."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SIH26090 | ArtisanLink AI | AI/ML Prototype"
)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import json
import re
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ArtisanLink AI",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# THEME / CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f8fc;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 800;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 44px;
        font-weight: 700;
    }

    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 18px;
        padding: 15px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
    }

    .ai-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 18px rgba(15,23,42,0.05);
        margin-bottom: 15px;
    }

    .ai-badge {
        display: inline-block;
        background: #eef2ff;
        color: #4338ca;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .hero-box {
        background: linear-gradient(
            135deg,
            #111827,
            #312e81
        );
        color: white;
        padding: 32px;
        border-radius: 24px;
        margin-bottom: 25px;
    }

    .hero-box h2 {
        color: white !important;
    }

    .hero-box p {
        color: #e5e7eb;
    }

    .footer-text {
        text-align: center;
        color: #94a3b8;
        padding-top: 40px;
        padding-bottom: 10px;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "uploaded_image": None,
    "catalogue_generated": False,
    "ai_result": None,
    "ai_description": "",
    "ai_hindi": "",
    "ai_kannada": "",
    "ai_product_name": "",
    "ai_category": "",
    "ai_material": "",
    "ai_craft": "",
    "ai_price": None,
    "ai_keywords": [],
    "translation_result": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

@st.cache_resource
def get_gemini_client():
    """
    Creates Gemini client using Streamlit Secrets.
    API key is never displayed or committed to GitHub.
    """

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


def get_ai_client():
    return get_gemini_client()


# ============================================================
# GEMINI IMAGE ANALYSIS
# ============================================================

def analyze_product_image(uploaded_file):

    client = get_ai_client()

    if client is None:
        return {
            "error": (
                "GEMINI_API_KEY is missing. "
                "Add it under Streamlit Cloud → Settings → Secrets."
            )
        }

    try:

        image_bytes = uploaded_file.getvalue()

        mime_type = uploaded_file.type or "image/jpeg"

        image_b64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        prompt = """
You are an expert artisan-commerce AI assistant.

Analyze the uploaded handmade product image.

IMPORTANT:
Do not invent exact facts that cannot be visually confirmed.
If something is uncertain, clearly mark it as "Likely" or "Estimated".

Return ONLY valid JSON with this structure:

{
  "product_name": "",
  "category": "",
  "craft_type": "",
  "material": "",
  "colors": [],
  "visual_features": [],
  "cultural_context": "",
  "target_customer": "",
  "description": "",
  "short_description": "",
  "seo_keywords": [],
  "estimated_price_min": 0,
  "estimated_price_max": 0,
  "pricing_reason": ""
}

The description should be professional and suitable for
an Indian e-commerce marketplace.

Mention craftsmanship, visible design characteristics,
possible material and cultural relevance where appropriate.

Do not claim certification, geographic origin,
traditional status or material composition unless supported
by the image or user-provided information.
"""

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {
                    "type": "image",
                    "data": image_b64,
                    "mime_type": mime_type
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        )

        text = interaction.output_text.strip()

        # Remove markdown JSON fences if Gemini returns them.
        text = re.sub(
            r"^```json\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        result = json.loads(text)

        return result

    except Exception as e:

        return {
            "error": f"AI analysis failed: {str(e)}"
        }


# ============================================================
# TEXT GENERATION
# ============================================================

def generate_catalogue(product_name, description, material, craft):

    client = get_ai_client()

    if client is None:
        return "Gemini API key is not configured."

    prompt = f"""
Create a professional e-commerce product listing.

Product:
{product_name}

Material:
{material}

Craft:
{craft}

Existing description:
{description}

Generate:

1. Professional product title
2. Short description
3. Detailed description
4. 5 SEO keywords
5. 5 selling points

Target audience:
Indian and international customers interested in
handmade artisan products.

Keep the content authentic and do not invent
unsupported certifications or claims.
"""

    try:

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return interaction.output_text.strip()

    except Exception as e:

        return f"Catalogue generation failed: {str(e)}"


# ============================================================
# TRANSLATION
# ============================================================

def translate_text(text, language):

    client = get_ai_client()

    if client is None:
        return "Gemini API key is not configured."

    prompt = f"""
Translate the following artisan product description
into {language}.

Preserve:
- Product meaning
- Craft terminology
- Cultural context
- Professional e-commerce tone
- Important product details

Do not add unsupported claims.

Text:

{text}
"""

    try:

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return interaction.output_text.strip()

    except Exception as e:

        return f"Translation failed: {str(e)}"


# ============================================================
# AI PRICING
# ============================================================

def ai_price_estimate(
    product_name,
    material,
    craft,
    description,
    material_cost,
    labour_cost,
    packaging,
    margin
):

    client = get_ai_client()

    if client is None:
        return None

    prompt = f"""
You are an artisan-commerce pricing assistant.

Product:
{product_name}

Material:
{material}

Craft:
{craft}

Description:
{description}

Raw material cost:
₹{material_cost}

Labour cost:
₹{labour_cost}

Packaging:
₹{packaging}

Desired profit margin:
{margin}%

Suggest a reasonable selling price range.

Consider:
- craftsmanship
- labour intensity
- material
- handmade value
- product positioning
- sustainable artisan income

Do not claim to have real-time market data.

Return ONLY JSON:

{{
  "recommended_price": 0,
  "minimum_price": 0,
  "maximum_price": 0,
  "reason": ""
}}
"""

    try:

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        text = interaction.output_text.strip()

        text = re.sub(
            r"^```json\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        return json.loads(text)

    except Exception:
        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🧵 ArtisanLink")

    st.caption("AI-powered artisan commerce")

    if get_ai_client():
        st.success("● AI Connected")
    else:
        st.warning("● AI Not Connected")

    st.divider()

    st.markdown("### WORKSPACE")

    selected_page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📸 AI Product Studio",
            "📝 Smart Catalogue",
            "💰 Dynamic Pricing",
            "🎯 Market Intelligence",
            "🤝 Buyer Matching"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### PLATFORM STATUS")

    st.write("🟢 Product Management")
    st.write("🟢 Catalogue Engine")

    if get_ai_client():
        st.write("🟢 AI Vision")
        st.write("🟢 Translation")
        st.write("🟢 AI Pricing")
    else:
        st.write("🟡 AI Vision")
        st.write("🟡 Translation")
        st.write("🟡 AI Pricing")

    st.divider()

    st.caption("SIH26090")
    st.caption("ArtisanLink Prototype")
    st.caption("AI Commerce Platform")


# ============================================================
# DASHBOARD
# ============================================================

if selected_page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero-box">
            <h2>🧵 ArtisanLink AI</h2>
            <p>
            AI-powered digital commerce infrastructure
            helping traditional artisans reach wider markets.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Artisans Connected",
        "18",
        "+3 this month"
    )

    m2.metric(
        "Products Listed",
        "126",
        "+18"
    )

    m3.metric(
        "Potential Buyers",
        "342",
        "+27"
    )

    m4.metric(
        "Estimated Revenue",
        "₹2.84L",
        "+18.6%"
    )

    st.write("")

    left, right = st.columns(
        [1.7, 1],
        gap="large"
    )

    with left:

        st.subheader("📈 Product Growth")

        growth_data = pd.DataFrame(
            {
                "Month": [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug"
                ],
                "Products": [
                    24,
                    37,
                    49,
                    63,
                    78,
                    94,
                    111,
                    126
                ]
            }
        )

        fig = px.area(
            growth_data,
            x="Month",
            y="Products",
            markers=True,
            title="Digital Product Listings"
        )

        fig.update_layout(
            height=390,
            margin=dict(
                l=10,
                r=10,
                t=55,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("🧩 Product Categories")

        category_data = pd.DataFrame(
            {
                "Category": [
                    "Bamboo",
                    "Textile",
                    "Pottery",
                    "Jewellery",
                    "Wood",
                    "Other"
                ],
                "Products": [
                    31,
                    28,
                    22,
                    17,
                    15,
                    13
                ]
            }
        )

        fig = px.pie(
            category_data,
            names="Category",
            values="Products",
            hole=0.55
        )

        fig.update_layout(
            height=390,
            margin=dict(
                l=5,
                r=5,
                t=20,
                b=5
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("🚀 ArtisanLink AI Workflow")

    w1, w2, w3, w4, w5 = st.columns(5)

    workflow = [
        ("01", "📷", "Capture", "Upload product"),
        ("02", "🤖", "Analyze", "AI understands craft"),
        ("03", "📝", "Catalogue", "Generate listing"),
        ("04", "💰", "Price", "AI pricing"),
        ("05", "🌍", "Connect", "Reach markets")
    ]

    for col, item in zip(
        [w1, w2, w3, w4, w5],
        workflow
    ):

        with col:

            with st.container(border=True):

                st.markdown(
                    f"### {item[0]}"
                )

                st.markdown(
                    f"### {item[1]} {item[2]}"
                )

                st.caption(item[3])

    st.divider()

    st.subheader("🌍 Artisan Impact")

    i1, i2, i3 = st.columns(3)

    impact = [
        (
            "🧑‍🎨",
            "Empower Artisans",
            "Reduce the technical barrier for artisans entering digital commerce."
        ),
        (
            "🌐",
            "Expand Market Access",
            "Create a continuous digital sales channel beyond physical fairs."
        ),
        (
            "💰",
            "Improve Income",
            "Support better product descriptions, pricing and market decisions."
        )
    ]

    for col, item in zip(
        [i1, i2, i3],
        impact
    ):

        with col:

            with st.container(border=True):

                st.markdown(f"### {item[0]}")
                st.markdown(f"### {item[1]}")
                st.write(item[2])


# ============================================================
# AI PRODUCT STUDIO
# ============================================================

elif selected_page == "📸 AI Product Studio":

    st.title("📸 AI Product Studio")

    st.write(
        "Upload a handmade product and let Gemini create "
        "structured product intelligence."
    )

    st.divider()

    image_col, analysis_col = st.columns(
        [1.15, 0.85],
        gap="large"
    )

    with image_col:

        st.subheader("📷 Product Image")

        uploaded = st.file_uploader(
            "Upload your artisan product",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )

        if uploaded:

            st.session_state.uploaded_image = uploaded

            st.image(
                uploaded,
                caption="Product Preview",
                use_container_width=True
            )

            analyze_clicked = st.button(
                "✨ Analyze Product with AI",
                type="primary",
                use_container_width=True
            )

            if analyze_clicked:

                if not get_ai_client():

                    st.error(
                        "Gemini API is not configured. "
                        "Please check Streamlit Secrets."
                    )

                else:

                    with st.spinner(
                        "🤖 Gemini is analyzing your product..."
                    ):

                        result = analyze_product_image(
                            uploaded
                        )

                    if "error" in result:

                        st.error(result["error"])

                    else:

                        st.session_state.ai_result = result

                        st.session_state.ai_product_name = result.get(
                            "product_name",
                            ""
                        )

                        st.session_state.ai_category = result.get(
                            "category",
                            ""
                        )

                        st.session_state.ai_material = result.get(
                            "material",
                            ""
                        )

                        st.session_state.ai_craft = result.get(
                            "craft_type",
                            ""
                        )

                        st.session_state.ai_description = result.get(
                            "description",
                            ""
                        )

                        st.session_state.ai_keywords = result.get(
                            "seo_keywords",
                            []
                        )

                        st.success(
                            "✅ AI analysis completed!"
                        )

        else:

            st.info(
                "📷 Upload a product photograph to begin."
            )

    with analysis_col:

        st.subheader("🧠 AI Pipeline")

        pipeline = [
            ("01", "📷", "Image Input"),
            ("02", "🔍", "Visual Analysis"),
            ("03", "🏷️", "Craft Classification"),
            ("04", "🧵", "Material Detection"),
            ("05", "📝", "Description Generation"),
            ("06", "💰", "Price Recommendation"),
            ("07", "🌐", "Marketplace Ready")
        ]

        for number, icon, title in pipeline:

            with st.container(border=True):

                p1, p2, p3 = st.columns(
                    [0.5, 0.7, 3]
                )

                with p1:
                    st.caption(number)

                with p2:
                    st.markdown(f"### {icon}")

                with p3:
                    st.write(f"**{title}**")

    # --------------------------------------------------------
    # AI RESULTS
    # --------------------------------------------------------

    if st.session_state.ai_result:

        result = st.session_state.ai_result

        st.divider()

        st.subheader("🤖 AI Product Intelligence")

        r1, r2, r3, r4 = st.columns(4)

        r1.metric(
            "Product",
            result.get("product_name", "Unknown")
        )

        r2.metric(
            "Category",
            result.get("category", "Unknown")
        )

        r3.metric(
            "Material",
            result.get("material", "Unknown")
        )

        r4.metric(
            "Craft",
            result.get("craft_type", "Unknown")
        )

        st.divider()

        info1, info2 = st.columns(2)

        with info1:

            st.subheader("🎨 Visual Features")

            for feature in result.get(
                "visual_features",
                []
            ):

                st.write(f"• {feature}")

            st.subheader("🎨 Colors")

            colors = result.get(
                "colors",
                []
            )

            if colors:
                st.write(", ".join(colors))

        with info2:

            st.subheader("👥 Target Customer")

            st.write(
                result.get(
                    "target_customer",
                    "Not available"
                )
            )

            st.subheader("🏛️ Cultural Context")

            st.write(
                result.get(
                    "cultural_context",
                    "Not available"
                )
            )

        st.divider()

        st.subheader("📝 AI-Generated Description")

        st.write(
            result.get(
                "description",
                "No description generated."
            )
        )

        st.subheader("🔎 SEO Keywords")

        keywords = result.get(
            "seo_keywords",
            []
        )

        if keywords:

            st.write(
                " • ".join(
                    [str(x) for x in keywords]
                )
            )

        st.divider()

        st.subheader("💰 AI Price Estimate")

        p1, p2, p3 = st.columns(3)

        p1.metric(
            "Minimum",
            f"₹{result.get('estimated_price_min', 0):,.0f}"
        )

        p2.metric(
            "Suggested",
            f"₹{(
                result.get('estimated_price_min', 0)
                + result.get('estimated_price_max', 0)
            ) / 2:,.0f}"
        )

        p3.metric(
            "Maximum",
            f"₹{result.get('estimated_price_max', 0):,.0f}"
        )

        st.info(
            result.get(
                "pricing_reason",
                "AI pricing estimate."
            )
        )


# ============================================================
# SMART CATALOGUE
# ============================================================

elif selected_page == "📝 Smart Catalogue":

    st.title("📝 Smart Catalogue")

    st.write(
        "Create multilingual professional product listings."
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🇬🇧 English",
            "🇮🇳 Hindi",
            "🇮🇳 Kannada",
            "🌐 Languages"
        ]
    )

    # --------------------------------------------------------
    # ENGLISH
    # --------------------------------------------------------

    with tab1:

        st.subheader("English Product Listing")

        product_name = st.text_input(
            "Product Name",
            value=st.session_state.ai_product_name,
            placeholder="Example: Handcrafted Bamboo Basket"
        )

        description = st.text_area(
            "Product Description",
            value=st.session_state.ai_description,
            height=170
        )

        c1, c2 = st.columns(2)

        with c1:

            material = st.text_input(
                "Material",
                value=st.session_state.ai_material,
                placeholder="Bamboo"
            )

        with c2:

            craft = st.text_input(
                "Craft Type",
                value=st.session_state.ai_craft,
                placeholder="Traditional Bamboo Craft"
            )

        c3, c4 = st.columns(2)

        with c3:

            category = st.selectbox(
                "Product Category",
                [
                    "Bamboo Handicraft",
                    "Traditional Textile",
                    "Pottery",
                    "Jewellery",
                    "Wooden Handicraft",
                    "Other"
                ]
            )

        with c4:

            target_market = st.selectbox(
                "Target Market",
                [
                    "Local",
                    "Regional",
                    "National",
                    "International"
                ]
            )

        if st.button(
            "✨ Generate Professional Catalogue",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Creating professional catalogue..."
            ):

                generated = generate_catalogue(
                    product_name,
                    description,
                    material,
                    craft
                )

            st.session_state.catalogue_generated = True
            st.session_state.ai_description = generated

            st.success(
                "Catalogue generated successfully!"
            )

        if st.session_state.catalogue_generated:

            st.divider()

            st.subheader(
                "📦 Generated Marketplace Listing"
            )

            st.write(
                st.session_state.ai_description
            )

    # --------------------------------------------------------
    # HINDI
    # --------------------------------------------------------

    with tab2:

        st.subheader("🇮🇳 Hindi Catalogue")

        source_text = st.session_state.ai_description

        if source_text:

            if st.button(
                "🇮🇳 Generate Hindi Translation",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Translating to Hindi..."
                ):

                    translated = translate_text(
                        source_text,
                        "Hindi"
                    )

                st.session_state.ai_hindi = translated

        else:

            st.info(
                "First generate an English catalogue."
            )

        if st.session_state.ai_hindi:

            st.text_area(
                "Hindi Description",
                value=st.session_state.ai_hindi,
                height=300
            )

    # --------------------------------------------------------
    # KANNADA
    # --------------------------------------------------------

    with tab3:

        st.subheader("🇮🇳 Kannada Catalogue")

        source_text = st.session_state.ai_description

        if source_text:

            if st.button(
                "🇮🇳 Generate Kannada Translation",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Translating to Kannada..."
                ):

                    translated = translate_text(
                        source_text,
                        "Kannada"
                    )

                st.session_state.ai_kannada = translated

        else:

            st.info(
                "First generate an English catalogue."
            )

        if st.session_state.ai_kannada:

            st.text_area(
                "Kannada Description",
                value=st.session_state.ai_kannada,
                height=300
            )

    # --------------------------------------------------------
    # LANGUAGES
    # --------------------------------------------------------

    with tab4:

        st.subheader("🌐 Regional Language Engine")

        language_data = pd.DataFrame(
            {
                "Language": [
                    "Hindi",
                    "Kannada",
                    "Tamil",
                    "Telugu",
                    "Malayalam",
                    "Bengali",
                    "Assamese",
                    "Marathi",
                    "Gujarati",
                    "Odia",
                    "Punjabi"
                ],
                "AI Translation": [
                    "Available",
                    "Available",
                    "Available",
                    "Available",
                    "Available",
                    "Available",
                    "Available",
                    "Available",
                    "Available",
                    "Available",
                    "Available"
                ]
            }
        )

        st.dataframe(
            language_data,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        selected_language = st.selectbox(
            "Translate catalogue to",
            [
                "Tamil",
                "Telugu",
                "Malayalam",
                "Bengali",
                "Assamese",
                "Marathi",
                "Gujarati",
                "Odia",
                "Punjabi"
            ]
        )

        if st.button(
            "🌐 Translate",
            use_container_width=True
        ):

            if not st.session_state.ai_description:

                st.warning(
                    "Generate an English catalogue first."
                )

            else:

                with st.spinner(
                    f"Translating to {selected_language}..."
                ):

                    translation = translate_text(
                        st.session_state.ai_description,
                        selected_language
                    )

                st.session_state.translation_result = translation

        if st.session_state.translation_result:

            st.text_area(
                f"{selected_language} Translation",
                value=st.session_state.translation_result,
                height=300
            )


# ============================================================
# DYNAMIC PRICING
# ============================================================

elif selected_page == "💰 Dynamic Pricing":

    st.title("💰 Dynamic Pricing Assistant")

    st.write(
        "Combine production economics with AI-assisted "
        "artisan pricing."
    )

    st.divider()

    input_col, result_col = st.columns(
        [1, 1],
        gap="large"
    )

    with input_col:

        st.subheader("Production Inputs")

        material_cost = st.number_input(
            "Raw Material Cost",
            min_value=0,
            value=300,
            step=50
        )

        labour_cost = st.number_input(
            "Labour Cost",
            min_value=0,
            value=500,
            step=50
        )

        packaging = st.number_input(
            "Packaging & Other Costs",
            min_value=0,
            value=100,
            step=50
        )

        margin = st.slider(
            "Desired Profit Margin",
            min_value=5,
            max_value=100,
            value=30
        )

        demand_factor = st.slider(
            "Demand Adjustment",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1
        )

        ai_pricing = st.checkbox(
            "🤖 Use Gemini AI pricing assistance",
            value=True
        )

    production_cost = (
        material_cost
        + labour_cost
        + packaging
    )

    profit = production_cost * margin / 100

    formula_price = (
        production_cost + profit
    ) * demand_factor

    ai_result = None

    if ai_pricing:

        if st.button(
            "✨ Analyze Price with AI",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Gemini is evaluating artisan pricing..."
            ):

                ai_result = ai_price_estimate(
                    st.session_state.ai_product_name
                    or "Handmade Artisan Product",
                    st.session_state.ai_material
                    or "Not specified",
                    st.session_state.ai_craft
                    or "Traditional handmade craft",
                    st.session_state.ai_description
                    or "Handmade artisan product",
                    material_cost,
                    labour_cost,
                    packaging,
                    margin
                )

            if ai_result:

                st.session_state.ai_price = ai_result

    with result_col:

        st.subheader("💰 Pricing Preview")

        if st.session_state.ai_price:

            result = st.session_state.ai_price

            st.metric(
                "AI Recommended Price",
                f"₹{result.get('recommended_price', 0):,.0f}"
            )

            p1, p2 = st.columns(2)

            with p1:

                st.metric(
                    "Minimum",
                    f"₹{result.get('minimum_price', 0):,.0f}"
                )

            with p2:

                st.metric(
                    "Maximum",
                    f"₹{result.get('maximum_price', 0):,.0f}"
                )

            st.info(
                result.get(
                    "reason",
                    "AI pricing recommendation."
                )
            )

        else:

            st.metric(
                "Formula Price",
                f"₹{formula_price:,.0f}"
            )

            st.caption(
                "Generate an AI recommendation for a richer pricing analysis."
            )

        r1, r2 = st.columns(2)

        with r1:

            st.metric(
                "Production Cost",
                f"₹{production_cost:,.0f}"
            )

        with r2:

            st.metric(
                "Estimated Profit",
                f"₹{formula_price - production_cost:,.0f}"
            )

    st.divider()

    st.subheader("📊 Price Breakdown")

    price_data = pd.DataFrame(
        {
            "Component": [
                "Raw Material",
                "Labour",
                "Packaging",
                "Profit"
            ],
            "Amount": [
                material_cost,
                labour_cost,
                packaging,
                profit
            ]
        }
    )

    fig = px.bar(
        price_data,
        x="Component",
        y="Amount",
        text="Amount",
        title="Production Cost Structure"
    )

    fig.update_traces(
        texttemplate="₹%{text}",
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.warning(
        "AI pricing is an advisory estimate. It does not represent "
        "live market pricing unless connected to a verified market dataset."
    )


# ============================================================
# MARKET INTELLIGENCE
# ============================================================

elif selected_page == "🎯 Market Intelligence":

    st.title("🎯 Market Intelligence")

    st.write(
        "Identify promising markets for traditional "
        "artisan products."
    )

    st.divider()

    market_data = pd.DataFrame(
        {
            "City": [
                "Bengaluru",
                "Guwahati",
                "Mumbai",
                "Delhi",
                "Hyderabad",
                "Chennai",
                "Kolkata"
            ],
            "Opportunity": [
                92,
                88,
                87,
                84,
                79,
                75,
                72
            ],
            "Demand": [
                91,
                86,
                88,
                83,
                77,
                73,
                70
            ]
        }
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Top Market",
        "Bengaluru"
    )

    m2.metric(
        "Opportunity",
        "92%"
    )

    m3.metric(
        "Demand Index",
        "91"
    )

    m4.metric(
        "Markets Analyzed",
        "7"
    )

    st.divider()

    chart_col, table_col = st.columns(
        [1.4, 1],
        gap="large"
    )

    with chart_col:

        st.subheader("📊 Market Opportunity")

        fig = px.bar(
            market_data.sort_values(
                "Opportunity",
                ascending=True
            ),
            x="Opportunity",
            y="City",
            orientation="h",
            text="Opportunity"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            height=450,
            margin=dict(
                l=10,
                r=30,
                t=20,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with table_col:

        st.subheader("🏆 Market Ranking")

        ranking = market_data.copy()

        ranking.insert(
            0,
            "Rank",
            range(
                1,
                len(ranking) + 1
            )
        )

        st.dataframe(
            ranking,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("🔮 Future AI Recommendations")

    r1, r2, r3 = st.columns(3)

    with r1:

        with st.container(border=True):

            st.markdown("### 📍 Location")

            st.write(
                "Recommend cities based on product demand "
                "and customer behaviour."
            )

    with r2:

        with st.container(border=True):

            st.markdown("### 📦 Product")

            st.write(
                "Identify which products are most suitable "
                "for each market."
            )

    with r3:

        with st.container(border=True):

            st.markdown("### 📈 Trend")

            st.write(
                "Track market trends and emerging "
                "customer preferences."
            )


# ============================================================
# BUYER MATCHING
# ============================================================

elif selected_page == "🤝 Buyer Matching":

    st.title("🤝 Buyer Matching")

    st.write(
        "Connect artisan products with potential retailers, "
        "resellers and customers."
    )

    st.divider()

    buyers = [
        {
            "name": "Heritage Handicrafts",
            "city": "Delhi",
            "score": 94,
            "type": "Traditional handmade products",
            "orders": 126
        },
        {
            "name": "Indian Artisan Store",
            "city": "Mumbai",
            "score": 91,
            "type": "Premium artisan products",
            "orders": 98
        },
        {
            "name": "EcoCraft Retail",
            "city": "Bengaluru",
            "score": 88,
            "type": "Sustainable handicrafts",
            "orders": 83
        },
        {
            "name": "Traditional Arts Hub",
            "city": "Hyderabad",
            "score": 83,
            "type": "Cultural products",
            "orders": 61
        }
    ]

    b1, b2, b3 = st.columns(3)

    b1.metric(
        "Potential Buyers",
        "342"
    )

    b2.metric(
        "High Match",
        "48"
    )

    b3.metric(
        "Average Match",
        "89%"
    )

    st.divider()

    st.subheader("🎯 Recommended Buyer Matches")

    for buyer in buyers:

        with st.container(border=True):

            c1, c2, c3 = st.columns(
                [2.4, 1, 0.8]
            )

            with c1:

                st.markdown(
                    f"### 🏢 {buyer['name']}"
                )

                st.write(
                    f"📍 {buyer['city']}"
                )

                st.caption(
                    buyer["type"]
                )

            with c2:

                st.metric(
                    "Match",
                    f"{buyer['score']}%"
                )

            with c3:

                st.write("")

                st.button(
                    "View",
                    key=f"view_{buyer['name']}"
                )

    st.divider()

    st.subheader("🧠 Matching Factors")

    factor_data = pd.DataFrame(
        {
            "Factor": [
                "Product Category",
                "Material",
                "Price Range",
                "Location",
                "Craft Type",
                "Buyer Preference"
            ],
            "Weight": [
                25,
                15,
                20,
                10,
                15,
                15
            ]
        }
    )

    fig = px.bar(
        factor_data,
        x="Factor",
        y="Weight",
        text="Weight",
        title="Future AI Matching Model"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧵 ArtisanLink AI • SIH26090 • "
    "Empowering traditional artisans through digital commerce"
)

st.caption(
    "Gemini-powered AI • Vision • Catalogue • Translation • Pricing"
)
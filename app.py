import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

    /* ---------- GENERAL ---------- */

    .stApp {
        background-color: #f7f8fc;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    /* ---------- HEADINGS ---------- */

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

    /* ---------- METRICS ---------- */

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

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 12px;
        min-height: 44px;
        font-weight: 700;
    }

    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 18px;
        padding: 15px;
    }

    /* ---------- DATAFRAME ---------- */

    [data-testid="stDataFrame"] {
        border-radius: 14px;
    }

    /* ---------- FOOTER ---------- */

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

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "catalogue_generated" not in st.session_state:
    st.session_state.catalogue_generated = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🧵 ArtisanLink")

    st.caption("AI-powered artisan commerce")

    st.success("● Prototype Online")

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
    st.write("🟡 AI Vision")
    st.write("🟡 Translation")
    st.write("🟡 Market Intelligence")
    st.write("🟡 Buyer Matching")

    st.divider()

    st.caption("SIH26090")
    st.caption("ArtisanLink Prototype")
    st.caption("Phase 1 • UI")


# ============================================================
# DASHBOARD
# ============================================================

if selected_page == "🏠 Dashboard":

    st.title("🧵 ArtisanLink")

    st.write(
        "Digital commerce infrastructure for traditional artisans."
    )

    st.divider()

    # --------------------------------------------------------
    # TOP METRICS
    # --------------------------------------------------------

    st.subheader("Platform Overview")

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

    # --------------------------------------------------------
    # MAIN DASHBOARD
    # --------------------------------------------------------

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
            ),
            showlegend=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    st.divider()

    st.subheader("🚀 ArtisanLink Workflow")

    w1, w2, w3, w4, w5 = st.columns(5)

    with w1:
        with st.container(border=True):
            st.markdown("### 01")
            st.markdown("📷 **Capture**")
            st.caption("Upload product image")

    with w2:
        with st.container(border=True):
            st.markdown("### 02")
            st.markdown("🤖 **Analyze**")
            st.caption("AI understands the craft")

    with w3:
        with st.container(border=True):
            st.markdown("### 03")
            st.markdown("📝 **Catalogue**")
            st.caption("Create digital listing")

    with w4:
        with st.container(border=True):
            st.markdown("### 04")
            st.markdown("💰 **Price**")
            st.caption("Estimate selling price")

    with w5:
        with st.container(border=True):
            st.markdown("### 05")
            st.markdown("🌍 **Connect**")
            st.caption("Reach new markets")

    # --------------------------------------------------------
    # IMPACT
    # --------------------------------------------------------

    st.divider()

    st.subheader("🌍 Artisan Impact")

    i1, i2, i3 = st.columns(3)

    with i1:

        with st.container(border=True):

            st.markdown("### 🧑‍🎨")

            st.markdown("### Empower Artisans")

            st.write(
                "Reduce the technical barrier for artisans "
                "entering digital commerce."
            )

    with i2:

        with st.container(border=True):

            st.markdown("### 🌐")

            st.markdown("### Expand Market Access")

            st.write(
                "Create a continuous digital sales channel "
                "beyond physical fairs."
            )

    with i3:

        with st.container(border=True):

            st.markdown("### 💰")

            st.markdown("### Improve Income")

            st.write(
                "Help artisans make better pricing and "
                "market decisions."
            )


# ============================================================
# AI PRODUCT STUDIO
# ============================================================

elif selected_page == "📸 AI Product Studio":

    st.title("📸 AI Product Studio")

    st.write(
        "Transform a simple product photograph into "
        "structured digital product intelligence."
    )

    st.divider()

    # --------------------------------------------------------
    # IMAGE AREA
    # --------------------------------------------------------

    image_col, analysis_col = st.columns(
        [1.15, 0.85],
        gap="large"
    )

    with image_col:

        st.subheader("Product Image")

        uploaded = st.file_uploader(
            "Upload your artisan product",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            help="Upload a clear photograph of your handmade product."
        )

        if uploaded:

            st.session_state.uploaded_image = uploaded

            st.image(
                uploaded,
                caption="Product Preview",
                use_container_width=True
            )

            st.button(
                "✨ Analyze Product",
                type="primary",
                use_container_width=True,
                disabled=True
            )

            st.caption(
                "AI Vision will be activated in Phase 2."
            )

        else:

            st.info(
                "📷 Upload a product photograph to begin."
            )

    # --------------------------------------------------------
    # AI PIPELINE
    # --------------------------------------------------------

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
    # FEATURES
    # --------------------------------------------------------

    st.divider()

    st.subheader("✨ Product Intelligence")

    f1, f2, f3 = st.columns(3)

    with f1:

        with st.container(border=True):

            st.markdown("### 🔎 Recognition")

            st.write(
                "Identify product category, craft type and "
                "visible materials."
            )

            st.progress(0.95)

            st.caption("Vision capability • Planned")

    with f2:

        with st.container(border=True):

            st.markdown("### 📝 Content")

            st.write(
                "Automatically create professional "
                "e-commerce descriptions."
            )

            st.progress(0.90)

            st.caption("NLP capability • Planned")

    with f3:

        with st.container(border=True):

            st.markdown("### 🛒 Marketplace")

            st.write(
                "Prepare products for digital marketplaces "
                "and online discovery."
            )

            st.progress(0.85)

            st.caption("Commerce capability • Planned")


# ============================================================
# SMART CATALOGUE
# ============================================================

elif selected_page == "📝 Smart Catalogue":

    st.title("📝 Smart Catalogue")

    st.write(
        "Create structured product listings and prepare "
        "them for multilingual digital commerce."
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
            placeholder="Example: Handcrafted Bamboo Basket"
        )

        description = st.text_area(
            "Product Description",
            placeholder=(
                "Describe the product, materials, "
                "craftsmanship and cultural significance..."
            ),
            height=170
        )

        c1, c2 = st.columns(2)

        with c1:

            st.text_input(
                "Material",
                placeholder="Bamboo"
            )

        with c2:

            st.text_input(
                "Craft Type",
                placeholder="Traditional Bamboo Craft"
            )

        c3, c4 = st.columns(2)

        with c3:

            st.selectbox(
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

            st.selectbox(
                "Target Market",
                [
                    "Local",
                    "Regional",
                    "National",
                    "International"
                ]
            )

        st.button(
            "✨ Generate Professional Catalogue",
            type="primary",
            use_container_width=True,
            disabled=True
        )

        st.caption(
            "AI catalogue generation will be connected in Phase 2."
        )

    # --------------------------------------------------------
    # HINDI
    # --------------------------------------------------------

    with tab2:

        st.subheader("🇮🇳 Hindi Catalogue")

        st.info(
            "Hindi AI translation will be connected in Phase 2."
        )

        st.text_input(
            "Hindi Product Name",
            placeholder="AI-generated Hindi name"
        )

        st.text_area(
            "Hindi Description",
            placeholder="AI-generated Hindi description",
            height=180
        )

    # --------------------------------------------------------
    # KANNADA
    # --------------------------------------------------------

    with tab3:

        st.subheader("🇮🇳 Kannada Catalogue")

        st.info(
            "Kannada AI translation will be connected in Phase 2."
        )

        st.text_input(
            "Kannada Product Name",
            placeholder="AI-generated Kannada name"
        )

        st.text_area(
            "Kannada Description",
            placeholder="AI-generated Kannada description",
            height=180
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
                "Translation": [
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned"
                ],
                "E-Commerce Ready": [
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes",
                    "Yes"
                ]
            }
        )

        st.dataframe(
            language_data,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# DYNAMIC PRICING
# ============================================================

elif selected_page == "💰 Dynamic Pricing":

    st.title("💰 Dynamic Pricing Assistant")

    st.write(
        "Estimate a sustainable selling price using "
        "production cost, labour and desired margin."
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

    production_cost = (
        material_cost
        + labour_cost
        + packaging
    )

    profit = production_cost * margin / 100

    recommended_price = (
        production_cost + profit
    ) * demand_factor

    with result_col:

        st.subheader("AI Pricing Preview")

        st.metric(
            "Recommended Selling Price",
            f"₹{recommended_price:,.0f}"
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
                f"₹{recommended_price - production_cost:,.0f}"
            )

        st.success(
            "✓ Material considered\n\n"
            "✓ Labour considered\n\n"
            "✓ Packaging considered\n\n"
            "✓ Desired margin considered"
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
        "Prototype calculation. Live market prices and "
        "ML-based pricing will be connected in Phase 2."
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
    "Phase 1 UI Prototype • AI integration will be added next"
)
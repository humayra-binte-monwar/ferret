import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Ferret",
    page_icon="🦡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #D68C29;
        color: #252422;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .hero {
        background-color: #D8D3C9;
        border: 3px solid #252422;
        border-radius: 4px;
        padding: 3rem 2rem;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 6px 6px 0px #252422;
        color: #252422;
    }
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 900;
        color: #252422;
        margin: 0.5rem 0;
        letter-spacing: -1px;
        text-transform: uppercase;
    }
    .hero p {
        font-size: 1.15rem;
        color: #4A4844;
        margin: 0;
        font-weight: 600;
    }
    
    .diamond-divider {
        color: #D68C29;
        font-size: 0.8rem;
        letter-spacing: 12px;
        margin: 0.5rem 0;
        font-weight: bold;
    }

    .answer-card {
        background-color: #D8D3C9;
        border: 3px solid #252422;
        border-radius: 4px;
        padding: 1.75rem;
        margin: 1.5rem 0 2.5rem 0;
        font-size: 1.1rem;
        line-height: 1.8;
        color: #252422;
        box-shadow: 6px 6px 0px #252422;
    }

    .source-card {
        background-color: #D8D3C9;
        border: 2px solid #252422;
        border-radius: 4px;
        padding: 1.35rem;
        margin-bottom: 1.25rem;
        box-shadow: 4px 4px 0px #252422;
        transition: all 0.15s ease-in-out;
    }
    .source-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px #252422;
    }
    .source-label {
        font-size: 0.85rem;
        font-weight: 800;
        color: #B46F17;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
    }
    .source-excerpt {
        font-size: 0.95rem;
        color: #4A4844;
        line-height: 1.6;
    }

    .section-heading {
        font-size: 0.9rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #252422;
        margin: 2.5rem 0 1rem 0;
        display: flex;
        align-items: center;
    }
    .section-heading::after {
        content: "";
        flex: 1;
        margin-left: 1rem;
        height: 3px;
        background-color: #252422;
    }

    [data-testid="stSidebar"] {
        background-color: #252422 !important;
        border-right: 3px solid #1A1917;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #D68C29 !important;
        font-weight: 800;
        text-transform: uppercase;
    }
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] .stMarkdown span {
        color: #D8D3C9 !important;
    }
    [data-testid="stSidebar"] .stFileUploader label {
        color: #D8D3C9 !important;
        font-weight: 700;
    }

    .stTextInput input {
        background-color: #D8D3C9 !important;
        border: 3px solid #252422 !important;
        color: #252422 !important;
        border-radius: 4px !important;
        padding: 0.85rem 1.25rem !important;
        font-size: 1.05rem !important;
        box-shadow: inset 2px 2px 0px rgba(0,0,0,0.08);
        transition: all 0.15s;
    }
    .stTextInput input:focus {
        background-color: #E2DDD5 !important;
        box-shadow: 5px 5px 0px #252422 !important;
    }

    .stButton > button[kind="primary"] {
        background: #252422 !important;
        color: #D8D3C9 !important;
        border: 3px solid #252422 !important;
        border-radius: 4px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        padding: 0.8rem 1.5rem !important;
        height: auto;
        box-shadow: 4px 4px 0px #D8D3C9 !important;
        transition: all 0.1s ease-in-out;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #D8D3C9 !important;
        background: #1A1917 !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #D8D3C9 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"] label {
        color: #D8D3C9 !important;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.8rem;
    }
    .st-at, .st-b1, .st-b2, .st-b3, .st-b4 {
        background-color: #D68C29 !important;
    }

    hr {
        border-color: #252422 !important;
        border-width: 3px !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🦡 Ferret")
    st.markdown("Upload PDFs to build your knowledge base, then ask questions instantly.")
    st.divider()

    st.markdown("**Upload a PDF**")
    uploaded_file = st.file_uploader(
        "Drop a PDF here or click to browse",
        type="pdf",
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.caption(f"📄 {uploaded_file.name}")
        if st.button("Upload & Index", type="primary", use_container_width=True):
            with st.spinner("Indexing document..."):
                resp = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
                )
            if resp.ok:
                st.success("Indexed successfully!")
            else:
                st.error(resp.json().get("detail", "Upload failed."))

    st.divider()
    
    st.markdown("**Search Settings**")
    top_k = st.slider(
        "Chunks to retrieve", 
        min_value=1, 
        max_value=10, 
        value=4,
        help="Higher values give the model more context, but processing may take longer."
    )

    st.divider()
    st.markdown(
        "<small style='color:#D8D3C9;'>Powered by ChromaDB · Groq · Llama 3.3</small>",
        unsafe_allow_html=True,
    )


st.markdown("""
<div class="hero">
    <div class="diamond-divider">◆ &nbsp; ◆ &nbsp; ◆ &nbsp; ◆ &nbsp; ◆</div>
    <h1>Ferret</h1>
    <p>A grounded, structural approach to reading your documents.</p>
    <div class="diamond-divider">◆ &nbsp; ◆ &nbsp; ◆ &nbsp; ◆ &nbsp; ◆</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1], vertical_alignment="bottom")
with col1:
    question = st.text_input(
        "Your question",
        placeholder="Type your question here...",
        label_visibility="collapsed",
    )
with col2:
    ask_clicked = st.button("Ask →", type="primary", use_container_width=True, disabled=not question)

st.divider()

if ask_clicked and question:
    with st.spinner("Retrieving knowledge..."):
        resp = requests.post(
            f"{API_URL}/ask",
            json={"question": question, "top_k": top_k},
        )

    if resp.ok:
        data = resp.json()

        st.markdown('<p class="section-heading">Answer</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="answer-card">{data["answer"]}</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<p class="section-heading">Sources</p>', unsafe_allow_html=True)
        for s in data["sources"]:
            st.markdown(f"""
            <div class="source-card">
                <div class="source-label">📄 {s['source']}</div>
                <div class="source-excerpt">{s['excerpt']}…</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error(resp.json().get("detail", "Something went wrong."))
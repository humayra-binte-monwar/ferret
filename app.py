import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.title("Ferret")
st.caption("Ask questions about your uploaded PDF documents.")

with st.sidebar:
    st.header("Upload a PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded_file and st.button("Upload & Index"):
        with st.spinner("Uploading and indexing..."):
            resp = requests.post(
                f"{API_URL}/upload",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
            )
        if resp.ok:
            st.success(resp.json()["message"])
        else:
            st.error(resp.json().get("detail", "Upload failed."))

st.divider()

question = st.text_input("Ask a question about your documents")
top_k = st.slider("Number of chunks to retrieve", min_value=1, max_value=10, value=4)

if st.button("Ask", disabled=not question):
    with st.spinner("Thinking..."):
        resp = requests.post(
            f"{API_URL}/ask",
            json={"question": question, "top_k": top_k},
        )
    if resp.ok:
        data = resp.json()
        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Sources")
        for s in data["sources"]:
            with st.expander(s["source"]):
                st.write(s["excerpt"] + "...")
    else:
        st.error(resp.json().get("detail", "Something went wrong."))

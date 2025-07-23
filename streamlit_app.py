import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# ====== PAGE CONFIG ======
st.set_page_config(
    page_title="E-commerce AI Agent",
    page_icon="🛒",
    layout="wide"
)

# ====== CUSTOM STYLES ======
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.hero {
    text-align: center;
    padding: 60px 20px 40px 20px;
}
.hero h1 {
    font-size: 3rem;
    background: linear-gradient(90deg,#ff6ec7,#7f5af0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
    margin-bottom: 10px;
}
.hero p {
    font-size: 1.2rem;
    color: #ccc;
    margin-bottom: 30px;
}
/* Custom input/button styles */
input[type="text"] {
    border: none !important;
    border-radius: 10px !important;
    padding: 0.8rem 1rem !important;
    font-size: 16px !important;
    background-color: #2a2a2a !important;
    color: white !important;
    box-shadow: none !important;
}
button[kind="primary"] {
    font-size: 16px !important;
    padding: 0.8rem 1.2rem !important;
    border-radius: 10px !important;
    background-color: #9147ff !important;
    color: white !important;
    border: none !important;
    transition: background-color 0.2s ease;
}
button[kind="primary"]:hover {
    background-color: #7c3aed !important;
}
</style>
<div class="hero">
    <h1>Breakthrough AI from Data to Deployment</h1>
    <p>Ask questions about your product sales, ads, and eligibility.</p>
</div>
""", unsafe_allow_html=True)

# ====== INPUT SECTION ======
st.markdown("### 💬 Ask a Question")

# Use columns for input and button
with st.form(key="query_form"):
    col_input, col_button = st.columns([5, 1])
    with col_input:
        question = st.text_input("Your Question", placeholder="Type your question here...", label_visibility="collapsed")
    with col_button:
        ask_button = st.form_submit_button("🚀 Ask Now")

# ====== PROCESSING ======
if ask_button and question.strip():
    with st.spinner("🤖 Thinking..."):
        try:
            response = requests.post("http://127.0.0.1:8000/ask", json={"question": question})
            if response.status_code == 200:
                data = response.json()
                q = question.lower()

                # Detect explicit plot type
                plot_type = None
                if "bar" in q:
                    plot_type = "bar"
                elif "line" in q:
                    plot_type = "line"
                elif "scatter" in q:
                    plot_type = "scatter"
                elif "histogram" in q:
                    plot_type = "histogram"
                elif "pie" in q:
                    plot_type = "pie"
                elif "column" in q:
                    plot_type = "column"
                elif "plot" in q or "graph" in q or "chart" in q:
                    plot_type = "bar"

                # Handle response
                if "table" in data:
                    df = pd.DataFrame(data["table"], columns=data.get("columns"))

                    if plot_type:
                        # Plot-only mode
                        if plot_type == "histogram":
                            col = df.columns[0]
                            if pd.api.types.is_numeric_dtype(df[col]):
                                st.subheader("📊 Histogram")
                                st.plotly_chart(
                                    px.histogram(df, x=col, title=f"Distribution of {col}"),
                                    use_container_width=True
                                )
                            else:
                                st.warning("⚠️ Cannot plot histogram: column not numeric.")
                        else:
                            if df.shape[1] >= 2:
                                x_col = df.columns[0]
                                y_col = df.columns[1]
                                if pd.api.types.is_numeric_dtype(df[y_col]):
                                    if plot_type == "bar":
                                        st.subheader("📊 Bar Chart")
                                        st.plotly_chart(px.bar(df, x=x_col, y=y_col), use_container_width=True)
                                    elif plot_type == "line":
                                        st.subheader("📈 Line Chart")
                                        st.plotly_chart(px.line(df, x=x_col, y=y_col), use_container_width=True)
                                    elif plot_type == "scatter":
                                        st.subheader("📌 Scatter Plot")
                                        st.plotly_chart(px.scatter(df, x=x_col, y=y_col), use_container_width=True)
                                    elif plot_type == "pie":
                                        st.subheader("🥧 Pie Chart")
                                        st.plotly_chart(px.pie(df, names=x_col, values=y_col), use_container_width=True)
                                    elif plot_type == "column":
                                        st.subheader("📊 Column Chart")
                                        st.plotly_chart(px.bar(df, x=x_col, y=y_col), use_container_width=True)
                                else:
                                    st.warning("⚠️ Cannot plot: second column not numeric.")
                            else:
                                st.warning("⚠️ Not enough columns to plot.")
                    else:
                        # Normal table + auto plot if meaningful
                        st.subheader("📋 Results")
                        st.dataframe(df, use_container_width=True)
                        if df.shape[0] > 1 and df.shape[1] >= 2:
                            x_col = df.columns[0]
                            y_col = df.columns[1]
                            if pd.api.types.is_numeric_dtype(df[y_col]):
                                st.subheader("📊 Visualization")
                                st.plotly_chart(px.bar(df, x=x_col, y=y_col), use_container_width=True)

                else:
                    # Single-value answer with typing effect
                    answer_text = data.get("answer", "")
                    if answer_text:
                        st.subheader("✅ Answer")
                        placeholder = st.empty()
                        typed = ""
                        for ch in answer_text:
                            typed += ch
                            placeholder.markdown(
                                f"<h3 style='text-align:center;'>{typed}</h3>",
                                unsafe_allow_html=True
                            )
                            time.sleep(0.03)
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"❌ Could not reach backend: {e}")
elif ask_button:
    st.warning("⚠️ Please type a question before asking.")

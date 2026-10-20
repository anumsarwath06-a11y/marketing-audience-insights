import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Marketing Audience Insights",
    page_icon="📊",
    layout="wide"
)

st.title("Marketing Audience Overlap & Ad Fatigue")
st.write(
    "A marketing decision-support tool for exploring audience exposure, "
    "engagement trends, and potential ad-fatigue signals."
)

# Upload the analysed results file
uploaded_file = st.file_uploader(
    "Upload marketing_audience_results.csv",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Audience Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Users Analysed", f"{df['uid'].nunique():,}")
    col2.metric(
        "High-Exposure Users",
        f"{(df['exposure_risk'] == 'High exposure').sum():,}"
    )
    col3.metric(
        "Potential Fatigue Flags",
        f"{(df['recommended_action'] == 'Investigate potential ad fatigue').sum():,}"
    )

    st.divider()

    st.subheader("Recommended Marketing Actions")

    action_counts = df["recommended_action"].value_counts()
    st.bar_chart(action_counts)

    st.subheader("Exposure Level Breakdown")

    exposure_counts = (
        df.groupby(["exposure_risk", "recommended_action"])
        .size()
        .unstack(fill_value=0)
    )

    st.dataframe(exposure_counts, use_container_width=True)

    st.subheader("Explore Individual User Results")

    exposure_options = ["All"] + sorted(df["exposure_risk"].dropna().unique().tolist())
    selected_exposure = st.selectbox(
        "Filter by exposure level",
        exposure_options
    )

    filtered_df = df.copy()

    if selected_exposure != "All":
        filtered_df = filtered_df[
            filtered_df["exposure_risk"] == selected_exposure
        ]

    st.dataframe(filtered_df, use_container_width=True)

    st.caption(
        "Exploratory analysis of a 100,000-row timestamp-sorted sample. "
        "A decline in click rate is a possible signal, not proof of ad fatigue."
    )

else:
    st.info("Upload your CSV file to view the dashboard.")

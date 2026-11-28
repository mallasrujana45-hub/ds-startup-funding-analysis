
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pathlib import Path


st.set_page_config(
    page_title="Startup Funding Insights",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "startup_funding_feature_engineered.csv"
)

df = pd.read_csv(DATA_PATH)

subvertical_counts = df["SubVertical_Cleaned"].value_counts()

df["SubVertical_Grouped"] = df["SubVertical_Cleaned"].apply(
    lambda x: x if x == "Unknown" or subvertical_counts.get(x, 0) >= 5 else "Other"
)



st.markdown("""
<style>

/* Main dashboard background */
.stApp {
    background-color: #F4F3FA;
}

/* Main headings */
h1, h2, h3 {
    color: #17213D;
    font-weight: 750;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #17213D;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #E7E5F0;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #E5E3EF;
    border-radius: 12px;
}

/* Horizontal divider */
hr {
    border-color: #E2E0EC;
}

</style>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
<div style="padding:10px 5px 25px 5px;">
    <h2 style="color:white; margin-bottom:5px;"> Startup Funding and Sector Investment</h2>
    <p style="color:#B8B9D2; font-size:13px;">
        Analytics Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #17213D;
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background-color: transparent;
    padding: 10px 12px;
    border-radius: 9px;
    margin-bottom: 5px;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background-color: #7952D6;
}
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Trends",
        "By Industry",
        "By City",
        "Top Investors",
        "Prediction",
        "Funding Explorer"
    ]
)



st.title("Startup Funding Insights")
st.write(
    "Explore trends, analyze investments and discover "
    "key patterns in startup funding."
)

st.divider()


st.subheader(page)


if page == "Overview":

    total_startups = df["Startup Name"].nunique()

    total_funding = df["Amount_Cleaned"].sum()

    total_investors = df["Investors_Cleaned"].nunique()

    total_industries = df[
        df["Industry_Grouped"] != "Unknown"
    ]["Industry_Grouped"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="background:#E8E2FF; padding:22px;
        border-radius:15px; text-align:center;">
            <p style="color:#51418C;">Total Startups</p>
            <h2 style="color:#29204F;">{total_startups:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:#DDF3F0; padding:22px;
        border-radius:15px; text-align:center;">
            <p style="color:#287A70;">Total Funding</p>
            <h2 style="color:#185B54;">${total_funding / 1_000_000_000:.2f}B</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:#FFEBD9; padding:22px;
        border-radius:15px; text-align:center;">
            <p style="color:#A65B20;">Investors Tracked</p>
            <h2 style="color:#784016;">{total_investors:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="background:#FCE2EB; padding:22px;
        border-radius:15px; text-align:center;">
            <p style="color:#A83F68;">Industries Covered</p>
            <h2 style="color:#782747;">{total_industries:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.divider()


    
    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("Year-wise Funding Trend")

        yearly_funding = (
            df.groupby("Year")["Amount_Cleaned"]
            .sum()
            .reset_index()
            .sort_values("Year")
        )

        yearly_funding["Amount_Cleaned"] = (
            yearly_funding["Amount_Cleaned"] / 1_000_000_000
        )

        st.line_chart(
            yearly_funding,
            x="Year",
            y="Amount_Cleaned",
            color="#7952D6"
        )

        st.caption("Total funding by year (Billions USD)")

    
    with chart2:
        st.subheader("Industry Investment Distribution")

        industry_funding = (
            df.groupby("Industry_Grouped")["Amount_Cleaned"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

        industry_funding = industry_funding[
            industry_funding["Amount_Cleaned"] > 0
        ]

        fig = px.pie(
            industry_funding,
            names="Industry_Grouped",
            values="Amount_Cleaned",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig.update_layout(
            showlegend=True,
            legend_title_text="Industry",
            margin=dict(t=20, b=20, l=10, r=10)
        )

        st.plotly_chart(fig, use_container_width=True)


    
    

    st.divider()

    st.subheader("Investment Type Distribution")

    investment_type_counts = (
        df["Investment_Type_Grouped"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    st.bar_chart(investment_type_counts)

    st.divider()
    city_funding = (
    df.groupby("City_Grouped")["Amount_Cleaned"]
    .sum()
    .nlargest(10)
    .reset_index()
)

    
    st.subheader("Top 10 Cities by Total Funding")

    fig = px.bar(
        city_funding,
        x="Amount_Cleaned",
        y="City_Grouped",
        orientation="h",
        color_discrete_sequence=["#4C8DDB"]
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Total Funding (USD)",
        yaxis_title="City",
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10)
    )

    st.plotly_chart(fig, use_container_width=True)

    
    st.divider()

    st.subheader("Recent Startup Funding Records")

    recent_records = df.copy()

    recent_records["Date_Sort"] = pd.to_datetime(
        recent_records["Date_Cleaned"],
        dayfirst=True,
        errors="coerce"
    )

    recent_records = (
        recent_records
        .sort_values("Date_Sort", ascending=False)
        .head(10)
    )

    
    display_records = recent_records[
        [
            "Startup Name",
            "Industry_Grouped",
            "City_Grouped",
            "Investment_Type_Grouped",
            "Amount_Cleaned",
            "Investors_Cleaned",
            "Year"
        ]
    ].rename(columns={
        "Industry_Grouped": "Industry",
        "City_Grouped": "City",
        "Investment_Type_Grouped": "Investment Type",
        "Amount_Cleaned": "Funding Amount (USD)",
        "Investors_Cleaned": "Investors"
    })

    st.dataframe(
        display_records,
        use_container_width=True,
        hide_index=True
    )



elif page == "Trends":


    st.subheader("Startup Funding Trends")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Year-wise Total Funding")

        yearly_funding = (
            df.groupby("Year")["Amount_Cleaned"]
            .sum()
            .reset_index()
        )

        yearly_funding["Funding (Billion USD)"] = (
            yearly_funding["Amount_Cleaned"] / 1_000_000_000
        )

        st.line_chart(
            yearly_funding,
            x="Year",
            y="Funding (Billion USD)"
        )

    with col2:
        st.write("Year-wise Number of Funding Records")

        yearly_records = (
            df.groupby("Year")
            .size()
            .reset_index(name="Number of Records")
        )

        st.bar_chart(
            yearly_records,
            x="Year",
            y="Number of Records"
        )

elif page == "By Industry":

    st.subheader("Industry-wise Funding Analysis")

    industry_funding = (
        df[df["Industry_Grouped"] != "Unknown"]
        .groupby("Industry_Grouped")["Amount_Cleaned"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.write("Top 10 Industries by Total Funding")

    st.bar_chart(
        industry_funding,
        x="Industry_Grouped",
        y="Amount_Cleaned"
    )
    
    st.divider()

    st.subheader("Number of Startups by Industry")

    industry_counts = (
        df[df["Industry_Grouped"] != "Unknown"]
        ["Industry_Grouped"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    st.bar_chart(industry_counts)
    
    st.divider()

    st.subheader("Industry Funding Summary")

    industry_summary = (
        df[df["Industry_Grouped"] != "Unknown"]
        .groupby("Industry_Grouped")
        .agg(
            Total_Funding=("Amount_Cleaned", "sum"),
            Startup_Records=("Startup Name", "count")
        )
        .reset_index()
        .sort_values("Total_Funding", ascending=False)
    )

    st.dataframe(
        industry_summary,
        use_container_width=True,
        hide_index=True
    )

elif page == "By City":

    st.subheader("City-wise Startup Funding Analysis")

    city_funding = (
        df[df["City_Grouped"] != "Unknown"]
        .groupby("City_Grouped")["Amount_Cleaned"]
        .sum()
        .nlargest(10)
        .sort_values()
        .reset_index()
    )

    
    st.subheader("Top 10 Cities by Total Funding")

    st.bar_chart(
        city_funding,
        x="City_Grouped",
        y="Amount_Cleaned"
    )
    
    st.divider()

    st.subheader("Number of Startups by City")

    city_counts = (
        df[df["City_Grouped"] != "Unknown"]
        ["City_Grouped"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    st.bar_chart(city_counts)
    
    st.divider()

    st.subheader("City-wise Funding Summary")

    city_summary = (
        df[df["City_Grouped"] != "Unknown"]
        .groupby("City_Grouped")
        .agg(
            Total_Funding=("Amount_Cleaned", "sum"),
            Startup_Records=("Startup Name", "count")
        )
        .reset_index()
        .sort_values("Total_Funding", ascending=False)
    )

    st.dataframe(
        city_summary,
        use_container_width=True,
        hide_index=True
    )

elif page == "Top Investors":

    st.subheader("Top Startup Investors Analysis")

    investor_counts = (
        df[df["Investors_Cleaned"] != "Undisclosed Investors"]
        ["Investors_Cleaned"]
        .dropna()
        .value_counts()
        .head(10)
        .sort_values()
    )

    st.subheader("Top 10 Investors by Number of Records")

    st.bar_chart(investor_counts)
    
    st.divider()

    st.subheader("Top 10 Investors by Total Funding")

    investor_funding = (
        df[df["Investors_Cleaned"] != "Undisclosed Investors"]
        .dropna(subset=["Investors_Cleaned"])
        .groupby("Investors_Cleaned")["Amount_Cleaned"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    st.bar_chart(investor_funding)
    
    st.divider()

   
    st.subheader("Investor Summary")

    investor_summary = (
        df[
            ~df["Investors_Cleaned"].isin([
                "Undisclosed Investors",
                "Unknown"
            ])
        ]
        .dropna(subset=["Investors_Cleaned"])
        .groupby("Investors_Cleaned")
        .agg(
            Funding_Records=("Startup Name", "count"),
            Total_Funding=("Amount_Cleaned", "sum")
        )
        .reset_index()
        .sort_values("Funding_Records", ascending=False)
        .head(20)
    )

    st.dataframe(
        investor_summary,
        use_container_width=True,
        hide_index=True
    )



elif page == "Prediction":

    st.subheader("Startup Industry Prediction")

    st.write(
        "Enter startup details to predict its likely industry sector."
    )

    MODEL_PATH = BASE_DIR / "models" / "random_forest_model.joblib"

    model = joblib.load(MODEL_PATH)
    

    

    st.write("Enter the following startup details:")

    with st.form("prediction_form"):

        year = st.number_input(
            "Funding Year",
            min_value=int(df["Year"].min()),
            max_value=int(df["Year"].max()),
            value=int(df["Year"].median()),
            step=1
        )

        month = st.selectbox(
            "Funding Month",
            list(range(1, 13))
        )

        city = st.selectbox(
            "Startup City",
            sorted(df["City_Grouped"].dropna().unique())
        )

        investment_type = st.selectbox(
            "Investment Type",
            sorted(df["Investment_Type_Grouped"].dropna().unique())
        )

        amount = st.number_input(
            "Funding Amount (USD)",
            min_value=0.0,
            value=1000000.0,
            step=100000.0
        )

        subvertical = st.selectbox(
    "Startup SubVertical",
    sorted(df["SubVertical_Cleaned"].dropna().unique())
)

        predict_button = st.form_submit_button(
            "Predict Industry"
        )

    if predict_button:

        input_data = pd.DataFrame({
            "Year": [year],
            "Month": [month],
            "City_Grouped": [city],
            "Investment_Type_Grouped": [investment_type],
            "Amount_Cleaned": [amount],
            "SubVertical_Cleaned": [subvertical]
        })

        prediction = model.predict(input_data)

        st.success(
            f"Predicted Industry: {prediction[0]}"
        )

elif page == "Funding Explorer":

    st.subheader("Startup Funding Explorer")

    st.write(
        "Search for startups and filter funding records "
        "based on different details."
    )

    
    search_name = st.text_input(
        "Search Startup Name",
        placeholder="Enter startup name..."
    )

    
    col1, col2 = st.columns(2)

    with col1:
        selected_city = st.selectbox(
            "Select City",
            ["All"] + sorted(df["City_Grouped"].dropna().unique().tolist())
        )

        selected_industry = st.selectbox(
            "Select Industry",
            ["All"] + sorted(df["Industry_Grouped"].dropna().unique().tolist())
        )

    with col2:
        selected_investment = st.selectbox(
            "Select Investment Type",
            ["All"] + sorted(df["Investment_Type_Grouped"].dropna().unique().tolist())
        )

        selected_year = st.selectbox(
            "Select Year",
            ["All"] + sorted(df["Year"].dropna().unique().tolist(), reverse=True)
        )

    
    filtered_df = df.copy()

    if search_name:
        filtered_df = filtered_df[
            filtered_df["Startup Name"].astype(str).str.contains(
                search_name, case=False, na=False
            )
        ]

    if selected_city != "All":
        filtered_df = filtered_df[
            filtered_df["City_Grouped"] == selected_city
        ]

    if selected_industry != "All":
        filtered_df = filtered_df[
            filtered_df["Industry_Grouped"] == selected_industry
        ]

    if selected_investment != "All":
        filtered_df = filtered_df[
            filtered_df["Investment_Type_Grouped"] == selected_investment
        ]

    if selected_year != "All":
        filtered_df = filtered_df[
            filtered_df["Year"] == selected_year
        ]

    st.write(f"Matching Records: {len(filtered_df)}")

    
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
 
   
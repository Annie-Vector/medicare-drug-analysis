import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Medicare Drug Spending Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/drug_spending_2023.csv")
    return df

df = load_data()
overall = df[df['Mftr_Name'] == 'Overall'].copy()

# Title
st.title("Medicare Drug Spending Analysis")
st.markdown("Analysis of Medicare Part D drug spending data (2019–2023)")

st.divider()

# Sidebar filters
st.sidebar.header("Filters")

drug_type = st.sidebar.selectbox(
    "Drug Type",
    ["All", "Brand", "Generic"]
)

top_n = st.sidebar.slider(
    "Top N Drugs to Display",
    min_value=5, max_value=20, value=10
)

# Filter data
if drug_type == "Brand":
    filtered = overall[overall['Brnd_Name'] != overall['Gnrc_Name']]
elif drug_type == "Generic":
    filtered = overall[overall['Brnd_Name'] == overall['Gnrc_Name']]
else:
    filtered = overall

# Metrics row
col1, col2, col3 = st.columns(3)

with col1:
    total = filtered['Tot_Spndng_2023'].sum()
    st.metric("Total Spending (2023)", f"${total/1e9:.1f}B")

with col2:
    avg = filtered['Tot_Spndng_2023'].mean()
    st.metric("Average Cost per Drug", f"${avg/1e6:.1f}M")

with col3:
    brand = overall[overall['Brnd_Name'] != overall['Gnrc_Name']]
    generic = overall[overall['Brnd_Name'] == overall['Gnrc_Name']]
    ratio = generic['Tot_Spndng_2023'].mean() / brand['Tot_Spndng_2023'].mean()
    savings = brand['Tot_Spndng_2023'].sum() * (1 - ratio)
    st.metric("Potential Savings", f"${savings/1e9:.1f}B")

st.divider()

# Charts row
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(f"Top {top_n} Drugs by Spending")
    top = filtered.nlargest(top_n, 'Tot_Spndng_2023')[['Brnd_Name', 'Tot_Spndng_2023']]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top['Brnd_Name'], top['Tot_Spndng_2023'], color='#3498DB')
    ax.set_xlabel('Total Spending ($)')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

with col_right:
    st.subheader("Brand vs Generic Average Spending")
    brand_avg = brand['Tot_Spndng_2023'].mean()
    generic_avg = generic['Tot_Spndng_2023'].mean()
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.bar(['Brand', 'Generic'], [brand_avg, generic_avg], color=['#E74C3C', '#2ECC71'])
    ax2.set_ylabel('Average Spending ($)')
    plt.tight_layout()
    st.pyplot(fig2)

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import zipfile

st.set_page_config(page_title='Supply Chain Intelligence', layout='wide')

@st.cache_data
def load_data():
    csv_name = 'APL_Logistics.csv'
    zip_name = 'APL_Logistics.zip'
    colab_path = '/content/sample_data/APL_Logistics.csv'

    # Priority 1: Check for ZIP (best for GitHub/Streamlit Cloud)
    if os.path.exists(zip_name):
        with zipfile.ZipFile(zip_name, 'r') as z:
            df = pd.read_csv(z.open(csv_name), encoding='latin1')
    # Priority 2: Check for raw CSV
    elif os.path.exists(csv_name):
        df = pd.read_csv(csv_name, encoding='latin1')
    # Priority 3: Local Colab Path
    else:
        df = pd.read_csv(colab_path, encoding='latin1')

    df = df[df['Sales'] > 0].copy()
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title('📊 APL Logistics Profitability Dashboard')
st.sidebar.header('Global Metrics')
total_rev = df['Sales'].sum()
st.sidebar.metric('Total Revenue', f'${total_rev:,.2f}')

# (Remaining dashboard logic stays the same...)


import streamlit as st
import pandas as pd
import plotly.express as px
import os
import zipfile

st.set_page_config(page_title='APL Logistics Intelligence', layout='wide')

@st.cache_data
def load_data():
    csv_name = 'APL_Logistics.csv'
    zip_name = 'APL_Logistics.zip'
    colab_path = '/content/sample_data/APL_Logistics.csv'
    if os.path.exists(zip_name):
        with zipfile.ZipFile(zip_name, 'r') as z:
            df = pd.read_csv(z.open(csv_name), encoding='latin1')
    elif os.path.exists(csv_name):
        df = pd.read_csv(csv_name, encoding='latin1')
    else:
        df = pd.read_csv(colab_path, encoding='latin1')
    df = df[df['Sales'] > 0].copy()
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Sidebar KPIs
st.sidebar.title('📊 Global KPIs')
total_rev = df['Sales'].sum()
total_prof = df['Order Profit Per Order'].sum()
avg_marg = (total_prof / total_rev) * 100

st.sidebar.metric('Total Revenue', f'${total_rev:,.2f}')
st.sidebar.metric('Total Profit', f'${total_prof:,.2f}')
st.sidebar.metric('Avg Margin', f'{avg_marg:.2f}%')

st.title('📦 Supply Chain Profitability Dashboard')

tab1, tab2, tab3, tab4 = st.tabs(['Market & Categories', 'Product Diagnostics', 'Customer Tiers', 'Discount Impact'])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Regional Profitability')
        mkt_df = df.groupby('Market')['Order Profit Per Order'].sum().reset_index().sort_values('Order Profit Per Order', ascending=False)
        st.plotly_chart(px.bar(mkt_df, x='Market', y='Order Profit Per Order', color='Market'), use_container_width=True)
    with col2:
        st.subheader('Top Categories by Profit')
        cat_df = df.groupby('Category Name')['Order Profit Per Order'].sum().reset_index().sort_values('Order Profit Per Order', ascending=False).head(10)
        st.plotly_chart(px.bar(cat_df, x='Order Profit Per Order', y='Category Name', orientation='h', color='Order Profit Per Order'), use_container_width=True)

with tab2:
    st.subheader('Product Margin Diagnostic')
    prod_df = df.groupby('Product Name').agg({'Sales':'sum', 'Order Profit Per Order':'sum'}).reset_index()
    prod_df['Margin (%)'] = (prod_df['Order Profit Per Order'] / prod_df['Sales']) * 100
    st.dataframe(prod_df.sort_values('Sales', ascending=False).head(20))
    st.plotly_chart(px.scatter(prod_df, x='Sales', y='Margin (%)', hover_name='Product Name', title='Sales vs Margin by Product'), use_container_width=True)

with tab3:
    st.subheader('Customer Value Segmentation')
    cust_df = df.groupby('Customer Id').agg({'Sales':'sum', 'Order Profit Per Order':'sum'}).reset_index()
    cust_df['Status'] = cust_df['Order Profit Per Order'].apply(lambda x: 'At Risk (Loss)' if x < 0 else 'Profitable')
    st.plotly_chart(px.pie(cust_df, names='Status', hole=0.4, title='Customer Base Health'), use_container_width=True)
    st.subheader('Top 10 Loss-Making Customers')
    st.table(cust_df.sort_values('Order Profit Per Order').head(10))

with tab4:
    st.subheader('Discount vs Profit Erosion')
    sample_df = df.sample(min(3000, len(df)))
    fig = px.scatter(sample_df, x='Order Item Discount Rate', y='Order Item Profit Ratio', trendline='ols', 
                     color='Order Item Profit Ratio', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True)

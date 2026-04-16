
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
# Set the layout to wide to accommodate multiple charts side-by-side
st.set_page_config(page_title='Supply Chain Intelligence', layout='wide')

@st.cache_data
def load_data():
    # Loads and cleans the logistics dataset for the dashboard.
    # Note: Update this path to a relative path or URL for production deployment
    df = pd.read_csv('/content/sample_data/APL_Logistics.csv', encoding='latin1')

    # Basic cleaning: Remove non-revenue records and strip column whitespace
    df = df[df['Sales'] > 0].copy()
    df.columns = df.columns.str.strip()
    return df

# Initialize data
df = load_data()

# --- Header Section ---
st.title('📊 APL Logistics Profitability Dashboard')
st.markdown('### Operational Intelligence & Margin Diagnostic')

# --- Sidebar KPIs ---
# Calculate high-level metrics for quick reference
total_rev = df['Sales'].sum()
total_prof = df['Order Profit Per Order'].sum()
avg_marg = (total_prof / total_rev) * 100 if total_rev != 0 else 0

st.sidebar.header('Global Metrics')
st.sidebar.metric('Total Revenue', f'${total_rev:,.2f}')
st.sidebar.metric('Total Profit', f'${total_prof:,.2f}')
st.sidebar.metric('Avg Margin', f'{avg_marg:.2f}%')

# --- Main Content: Analysis Tabs ---
tab1, tab2, tab3 = st.tabs(['Market Performance', 'Customer Segmentation', 'Discount Impact'])

with tab1:
    st.header('Regional Profitability')
    # Group by Market to visualize which regions drive the most profit
    mkt_df = df.groupby('Market')['Order Profit Per Order'].sum().reset_index().sort_values('Order Profit Per Order', ascending=False)
    fig_mkt = px.bar(mkt_df, x='Market', y='Order Profit Per Order', color='Market',
                     title='Total Profit by Region', labels={'Order Profit Per Order': 'Profit ($)'})
    st.plotly_chart(fig_mkt, use_container_width=True)

with tab2:
    st.header('Customer Value Tiers')
    # Segment customers into Profitable vs At-Risk based on cumulative profit
    cust_df = df.groupby('Customer Id').agg({'Sales':'sum', 'Order Profit Per Order':'sum'}).reset_index()
    cust_df['Status'] = cust_df['Order Profit Per Order'].apply(lambda x: 'At Risk' if x < 0 else 'Profitable')

    fig_seg = px.pie(cust_df, names='Status', title='Customer Profitability Split', hole=0.4)
    st.plotly_chart(fig_seg, use_container_width=True)
    st.info('At-Risk customers represent accounts where cumulative returns and discounts exceed total sales value.')

with tab3:
    st.header('Discount vs Margin Correlation')
    # Sample data for scatter plot performance
    fig_disc = px.scatter(df.sample(min(2000, len(df))), x='Order Item Discount Rate', y='Order Item Profit Ratio',
                          trendline='ols', opacity=0.5, title='Profit Erosion Diagnostic',
                          labels={'Order Item Discount Rate': 'Discount %', 'Order Item Profit Ratio': 'Profit Ratio'})
    st.plotly_chart(fig_disc, use_container_width=True)
    st.write('The downward trendline illustrates how increasing discount rates directly impact order-level profit ratios.')

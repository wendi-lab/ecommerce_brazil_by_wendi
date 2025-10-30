import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Konfigurasi page
st.set_page_config(
    page_title="Brazil E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1f77b4; text-align: center; margin-bottom: 1rem; }
    .metric-card { background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #1f77b4; margin: 0.5rem; }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load data dari GitHub"""
    try:
        # URL raw GitHub untuk file CSV Anda
        url = "https://raw.githubusercontent.com/username/repo-name/main/main_data_sample.csv"
        df = pd.read_csv(url)
        
        # Preprocessing dasar
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
        df['tahun'] = df['order_purchase_timestamp'].dt.year
        df['bulan'] = df['order_purchase_timestamp'].dt.month
        
        st.success(f"✅ Data loaded! {len(df):,} records")
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        # Fallback ke sample data
        return create_sample_data()

def create_sample_data():
    """Create sample data jika loading gagal"""
    st.warning("Using sample data for demonstration...")
    
    sample_size = 1000
    df = pd.DataFrame({
        'order_id': [f'order_{i}' for i in range(sample_size)],
        'customer_id': [f'customer_{i%100}' for i in range(sample_size)],
        'order_status': np.random.choice(['delivered', 'shipped'], sample_size),
        'order_purchase_timestamp': pd.date_range('2023-01-01', periods=sample_size, freq='H'),
        'customer_unique_id': [f'unique_{i%50}' for i in range(sample_size)],
        'customer_state': np.random.choice(['SP', 'RJ', 'MG', 'RS'], sample_size),
        'price': np.random.uniform(10, 500, sample_size),
        'freight_value': np.random.uniform(5, 50, sample_size),
        'product_category_name_english': np.random.choice(['Electronics', 'Home', 'Books'], sample_size),
        'review_score': np.random.randint(1, 6, sample_size),
        'payment_value': np.random.uniform(15, 550, sample_size)
    })
    
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['tahun'] = df['order_purchase_timestamp'].dt.year
    return df

def display_metrics(df):
    """Display key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['price'].sum()
        st.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
    
    with col2:
        avg_review = df['review_score'].mean()
        st.metric("Avg Review", f"{avg_review:.2f}/5.0")
    
    with col3:
        total_orders = df['order_id'].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col4:
        total_customers = df['customer_unique_id'].nunique()
        st.metric("Unique Customers", f"{total_customers:,}")

def main():
    st.markdown('<h1 class="main-header">📊 Brazil E-Commerce Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Filters
    st.sidebar.header("Filters")
    tahun_options = ['All'] + sorted(df['tahun'].unique())
    selected_year = st.sidebar.selectbox("Select Year", tahun_options)
    
    # Apply filter
    if selected_year != 'All':
        filtered_df = df[df['tahun'] == selected_year]
    else:
        filtered_df = df
    
    # Display metrics
    display_metrics(filtered_df)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "👥 Customers", "📦 Products"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Review distribution
            fig = px.histogram(filtered_df, x='review_score', title='Review Score Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Revenue by state
            state_revenue = filtered_df.groupby('customer_state')['price'].sum().reset_index()
            fig = px.bar(state_revenue, x='customer_state', y='price', title='Revenue by State')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Customer analysis
        customer_stats = filtered_df.groupby('customer_unique_id').agg({
            'order_id': 'nunique',
            'price': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(customer_stats, x='order_id', title='Orders per Customer')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(customer_stats, x='price', title='Spending per Customer')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Product analysis
        if 'product_category_name_english' in filtered_df.columns:
            category_stats = filtered_df.groupby('product_category_name_english').agg({
                'price': 'sum',
                'review_score': 'mean'
            }).reset_index()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(category_stats, x='product_category_name_english', y='price', 
                           title='Revenue by Category')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(category_stats, x='product_category_name_english', y='review_score',
                           title='Avg Review by Category')
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

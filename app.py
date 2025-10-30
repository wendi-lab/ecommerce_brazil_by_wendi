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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan yang clean
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .filter-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .ranking-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .top-ranking {
        border-left: 4px solid #28a745;
        background: linear-gradient(90deg, #d4edda, white);
    }
    .bottom-ranking {
        border-left: 4px solid #dc3545;
        background: linear-gradient(90deg, #f8d7da, white);
    }
</style>
""", unsafe_allow_html=True)

class BrazilEcommerceDashboard:
    def __init__(self):
        self.data_url = "https://raw.githubusercontent.com/username/repository-name/main/main_data_sample.csv"
        self.load_data()
        self.setup_brazil_coordinates()
        
    def setup_brazil_coordinates(self):
        """Setup koordinat manual untuk states Brazil dengan nama panjang"""
        self.brazil_states_coords = {
            'Acre': {'lat': -9.0238, 'lon': -70.8120},
            'Alagoas': {'lat': -9.5713, 'lon': -36.7820},
            'Amapá': {'lat': 1.4544, 'lon': -51.9482},
            'Amazonas': {'lat': -4.7936, 'lon': -64.6505},
            'Bahia': {'lat': -12.5797, 'lon': -41.7007},
            'Ceará': {'lat': -5.4984, 'lon': -39.3206},
            'Distrito Federal': {'lat': -15.7797, 'lon': -47.9297},
            'Espírito Santo': {'lat': -19.1834, 'lon': -40.3089},
            'Goiás': {'lat': -16.3291, 'lon': -49.8501},
            'Maranhão': {'lat': -4.9609, 'lon': -45.2744},
            'Mato Grosso': {'lat': -12.6819, 'lon': -56.9211},
            'Mato Grosso do Sul': {'lat': -20.7722, 'lon': -54.7852},
            'Minas Gerais': {'lat': -18.5122, 'lon': -44.5550},
            'Pará': {'lat': -3.8191, 'lon': -52.7630},
            'Paraíba': {'lat': -7.2399, 'lon': -36.7819},
            'Paraná': {'lat': -24.8932, 'lon': -51.5870},
            'Pernambuco': {'lat': -8.8137, 'lon': -36.9541},
            'Piauí': {'lat': -7.7183, 'lon': -42.7289},
            'Rio de Janeiro': {'lat': -22.3530, 'lon': -42.6960},
            'Rio Grande do Norte': {'lat': -5.4026, 'lon': -36.9541},
            'Rio Grande do Sul': {'lat': -30.0346, 'lon': -51.2177},
            'Rondônia': {'lat': -11.5057, 'lon': -63.5806},
            'Roraima': {'lat': 2.7376, 'lon': -62.0751},
            'Santa Catarina': {'lat': -27.2423, 'lon': -50.2189},
            'São Paulo': {'lat': -23.5505, 'lon': -46.6333},
            'Sergipe': {'lat': -10.5741, 'lon': -37.3857},
            'Tocantins': {'lat': -9.9725, 'lon': -48.1882}
        }
        
    def load_data(self):
        """Load dan preprocess data"""
        try:
            # Coba load dari GitHub
            self.df = pd.read_csv(self.data_url)
            st.success("✅ Data berhasil dimuat dari GitHub!")
        except:
            # Fallback ke sample data
            st.warning("⚠️ Menggunakan sample data...")
            self.create_sample_data()
        
        # Preprocessing data
        self.preprocess_data()
        
    def create_sample_data(self):
        """Buat sample data untuk testing"""
        np.random.seed(42)
        sample_size = 5000
        
        # State mapping untuk nama panjang
        state_mapping = {
            'SP': 'São Paulo', 'RJ': 'Rio de Janeiro', 'MG': 'Minas Gerais',
            'RS': 'Rio Grande do Sul', 'PR': 'Paraná', 'SC': 'Santa Catarina',
            'BA': 'Bahia', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
            'GO': 'Goiás', 'PE': 'Pernambuco', 'CE': 'Ceará',
            'PA': 'Pará', 'MA': 'Maranhão', 'MS': 'Mato Grosso do Sul',
            'MT': 'Mato Grosso', 'PB': 'Paraíba', 'RN': 'Rio Grande do Norte',
            'AL': 'Alagoas', 'SE': 'Sergipe', 'PI': 'Piauí',
            'RO': 'Rondônia', 'TO': 'Tocantins', 'AC': 'Acre',
            'AM': 'Amazonas', 'RR': 'Roraima', 'AP': 'Amapá'
        }
        
        states = list(state_mapping.keys())
        state_full_names = list(state_mapping.values())
        
        self.df = pd.DataFrame({
            'order_id': [f'order_{i}' for i in range(sample_size)],
            'customer_id': [f'customer_{i%500}' for i in range(sample_size)],
            'order_status': np.random.choice(['delivered', 'shipped', 'processing'], sample_size),
            'order_purchase_timestamp': pd.date_range('2022-01-01', periods=sample_size, freq='H'),
            'customer_unique_id': [f'unique_cust_{i%300}' for i in range(sample_size)],
            'customer_state': np.random.choice(states, sample_size),
            'customer_state_full': np.random.choice(state_full_names, sample_size),
            'price': np.random.lognormal(4, 1, sample_size),
            'freight_value': np.random.uniform(5, 50, sample_size),
            'product_category_name_english': np.random.choice([
                'Electronics', 'Home Appliances', 'Books', 'Sports', 'Fashion',
                'Health & Beauty', 'Toys', 'Automotive', 'Tools', 'Garden'
            ], sample_size),
            'review_score': np.random.choice([1, 2, 3, 4, 5], sample_size, p=[0.05, 0.1, 0.15, 0.3, 0.4]),
            'payment_value': np.random.lognormal(5, 1, sample_size)
        })
        
        # Ensure price consistency
        self.df['price'] = self.df['price'].clip(10, 2000)
        self.df['payment_value'] = self.df['payment_value'].clip(15, 2500)
    
    def preprocess_data(self):
        """Preprocess data"""
        # Convert timestamp
        self.df['order_purchase_timestamp'] = pd.to_datetime(
            self.df['order_purchase_timestamp'], errors='coerce'
        )
        
        # Extract time features
        self.df['tahun'] = self.df['order_purchase_timestamp'].dt.year
        self.df['bulan'] = self.df['order_purchase_timestamp'].dt.month
        
        # Handle missing state_full names
        if 'customer_state_full' not in self.df.columns:
            state_mapping = {
                'SP': 'São Paulo', 'RJ': 'Rio de Janeiro', 'MG': 'Minas Gerais',
                'RS': 'Rio Grande do Sul', 'PR': 'Paraná', 'SC': 'Santa Catarina',
                'BA': 'Bahia', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
                'GO': 'Goiás', 'PE': 'Pernambuco', 'CE': 'Ceará',
                'PA': 'Pará', 'MA': 'Maranhão', 'MS': 'Mato Grosso do Sul',
                'MT': 'Mato Grosso', 'PB': 'Paraíba', 'RN': 'Rio Grande do Norte',
                'AL': 'Alagoas', 'SE': 'Sergipe', 'PI': 'Piauí',
                'RO': 'Rondônia', 'TO': 'Tocantins', 'AC': 'Acre',
                'AM': 'Amazonas', 'RR': 'Roraima', 'AP': 'Amapá'
            }
            self.df['customer_state_full'] = self.df['customer_state'].map(state_mapping)
    
    def create_filters(self):
        """Membuat filter section di bawah header"""
        st.markdown("---")
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.subheader("🎛️ FILTER DATA")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Filter Tahun
            tahun_options = ['All Time'] + sorted(self.df['tahun'].dropna().unique())
            selected_year = st.selectbox(
                "**Pilih Tahun:**",
                options=tahun_options,
                index=0
            )
        
        with col2:
            # Filter State
            state_options = ['All States'] + sorted(self.df['customer_state_full'].dropna().unique())
            selected_state = st.selectbox(
                "**Pilih State:**",
                options=state_options,
                index=0
            )
        
        with col3:
            # Filter Kategori Produk
            if 'product_category_name_english' in self.df.columns:
                category_options = ['All Categories'] + sorted(self.df['product_category_name_english'].dropna().unique())
                selected_category = st.selectbox(
                    "**Pilih Kategori Produk:**",
                    options=category_options,
                    index=0
                )
            else:
                selected_category = 'All Categories'
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_data = self.df.copy()
        
        if selected_year != 'All Time':
            filtered_data = filtered_data[filtered_data['tahun'] == selected_year]
        
        if selected_state != 'All States':
            filtered_data = filtered_data[filtered_data['customer_state_full'] == selected_state]
        
        if selected_category != 'All Categories':
            filtered_data = filtered_data[filtered_data['product_category_name_english'] == selected_category]
        
        return filtered_data
    
    def create_brazil_map(self, data, metric_type='review'):
        """Membuat peta Brazil dengan nama state panjang"""
        if metric_type == 'review':
            # Aggregate review scores per state
            state_data = data.groupby('customer_state_full').agg({
                'review_score': 'mean'
            }).round(3).reset_index()
            state_data.columns = ['state', 'value']
            title = 'Rata-rata Review Score per State'
            colorscale = 'RdYlGn'
            colorbar_title = "Review Score"
            
        else:  # revenue
            # Aggregate revenue per state
            state_data = data.groupby('customer_state_full').agg({
                'price': 'sum'
            }).round(0).reset_index()
            state_data.columns = ['state', 'value']
            title = 'Total Revenue per State (R$)'
            colorscale = 'Blues'
            colorbar_title = "Revenue (R$)"
        
        # Add coordinates
        state_data['lat'] = state_data['state'].map(lambda x: self.brazil_states_coords.get(x, {}).get('lat', 0))
        state_data['lon'] = state_data['state'].map(lambda x: self.brazil_states_coords.get(x, {}).get('lon', 0))
        
        # Remove states without coordinates
        state_data = state_data[state_data['lat'] != 0]
        
        if len(state_data) == 0:
            st.warning("Tidak ada data state dengan koordinat yang valid.")
            return None, state_data
        
        # Create hover text
        if metric_type == 'review':
            hover_text = state_data.apply(
                lambda row: f"<b>{row['state']}</b><br>Review Score: {row['value']:.2f}", axis=1
            )
        else:
            hover_text = state_data.apply(
                lambda row: f"<b>{row['state']}</b><br>Revenue: R$ {row['value']:,.0f}", axis=1
            )
        
        # Create map
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon=state_data['lon'],
            lat=state_data['lat'],
            text=hover_text,
            hoverinfo='text',
            marker=dict(
                size=state_data['value'] / state_data['value'].max() * 50 + 20,
                color=state_data['value'],
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title, thickness=15),
                line=dict(width=1, color='white'),
            ),
            name=''
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                x=0.5,
                xanchor='center',
                font=dict(size=16)
            ),
            geo=dict(
                scope='south america',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)',
                showcountries=True,
                showsubunits=True,
                subunitcolor='rgb(255, 255, 255)',
                center=dict(lat=-14, lon=-55),
                projection_scale=3
            ),
            height=500,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        return fig, state_data
    
    def display_product_rankings(self, data):
        """Menampilkan ranking produk berdasarkan review dan revenue"""
        if 'product_category_name_english' not in data.columns:
            st.warning("Data kategori produk tidak tersedia")
            return
        
        # Filter kategori dengan cukup data
        category_counts = data.groupby('product_category_name_english').size()
        valid_categories = category_counts[category_counts >= 5].index
        filtered_data = data[data['product_category_name_english'].isin(valid_categories)]
        
        if len(valid_categories) == 0:
            st.warning("Tidak ada kategori dengan cukup data untuk analisis")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 RANKING BERDASARKAN REVIEW")
            
            # Review ranking
            review_ranking = filtered_data.groupby('product_category_name_english').agg({
                'review_score': ['mean', 'count']
            }).round(3)
            review_ranking.columns = ['avg_review', 'count']
            review_ranking = review_ranking.reset_index()
            review_ranking = review_ranking[review_ranking['count'] >= 5]  # Minimum 5 reviews
            
            if len(review_ranking) > 0:
                # Top 5 by review
                top_review = review_ranking.nlargest(5, 'avg_review')
                st.markdown("**🥇 TOP 5 KATEGORI - REVIEW TERTINGGI**")
                for i, (idx, row) in enumerate(top_review.iterrows(), 1):
                    st.markdown(f"""
                    <div class="ranking-card top-ranking">
                        <div style="display: flex; justify-content: between; align-items: center;">
                            <span style="font-weight: bold; color: #28a745;">#{i}</span>
                            <span style="flex: 1; margin: 0 1rem; font-weight: bold;">{row['product_category_name_english']}</span>
                            <span style="font-weight: bold; color: #28a745;">{row['avg_review']:.2f}/5.0</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.5rem;">
                            {row['count']} reviews
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Bottom 5 by review
                bottom_review = review_ranking.nsmallest(5, 'avg_review')
                st.markdown("**📉 BOTTOM 5 KATEGORI - REVIEW TERENDAH**")
                for i, (idx, row) in enumerate(bottom_review.iterrows(), 1):
                    st.markdown(f"""
                    <div class="ranking-card bottom-ranking">
                        <div style="display: flex; justify-content: between; align-items: center;">
                            <span style="font-weight: bold; color: #dc3545;">#{i}</span>
                            <span style="flex: 1; margin: 0 1rem; font-weight: bold;">{row['product_category_name_english']}</span>
                            <span style="font-weight: bold; color: #dc3545;">{row['avg_review']:.2f}/5.0</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.5rem;">
                            {row['count']} reviews
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💰 RANKING BERDASARKAN REVENUE")
            
            # Revenue ranking
            revenue_ranking = filtered_data.groupby('product_category_name_english').agg({
                'price': ['sum', 'count']
            }).round(0)
            revenue_ranking.columns = ['total_revenue', 'order_count']
            revenue_ranking = revenue_ranking.reset_index()
            
            if len(revenue_ranking) > 0:
                # Top 5 by revenue
                top_revenue = revenue_ranking.nlargest(5, 'total_revenue')
                st.markdown("**🥇 TOP 5 KATEGORI - REVENUE TERTINGGI**")
                for i, (idx, row) in enumerate(top_revenue.iterrows(), 1):
                    st.markdown(f"""
                    <div class="ranking-card top-ranking">
                        <div style="display: flex; justify-content: between; align-items: center;">
                            <span style="font-weight: bold; color: #28a745;">#{i}</span>
                            <span style="flex: 1; margin: 0 1rem; font-weight: bold;">{row['product_category_name_english']}</span>
                            <span style="font-weight: bold; color: #28a745;">R$ {row['total_revenue']:,.0f}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.5rem;">
                            {row['order_count']} orders
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Bottom 5 by revenue
                bottom_revenue = revenue_ranking.nsmallest(5, 'total_revenue')
                st.markdown("**📉 BOTTOM 5 KATEGORI - REVENUE TERENDAH**")
                for i, (idx, row) in enumerate(bottom_revenue.iterrows(), 1):
                    st.markdown(f"""
                    <div class="ranking-card bottom-ranking">
                        <div style="display: flex; justify-content: between; align-items: center;">
                            <span style="font-weight: bold; color: #dc3545;">#{i}</span>
                            <span style="flex: 1; margin: 0 1rem; font-weight: bold;">{row['product_category_name_english']}</span>
                            <span style="font-weight: bold; color: #dc3545;">R$ {row['total_revenue']:,.0f}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.5rem;">
                            {row['order_count']} orders
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    def display_customer_analysis(self, data):
        """Menampilkan analisis customer spending"""
        st.markdown("### 👥 ANALISIS SPENDING CUSTOMER")
        
        # Hitung spending per customer
        customer_spending = data.groupby('customer_unique_id').agg({
            'price': 'sum',
            'order_id': 'nunique',
            'customer_state_full': 'first'
        }).reset_index()
        
        customer_spending.columns = ['customer_id', 'total_spending', 'order_count', 'state']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 DISTRIBUSI SPENDING CUSTOMER")
            
            # Metrics
            avg_spending = customer_spending['total_spending'].mean()
            median_spending = customer_spending['total_spending'].median()
            max_spending = customer_spending['total_spending'].max()
            
            st.metric("Rata-rata Spending per Customer", f"R$ {avg_spending:,.2f}")
            st.metric("Median Spending per Customer", f"R$ {median_spending:,.2f}")
            st.metric("Spending Tertinggi", f"R$ {max_spending:,.2f}")
            
            # Histogram spending
            fig = px.histogram(
                customer_spending, 
                x='total_spending',
                title='Distribusi Total Spending per Customer',
                labels={'total_spending': 'Total Spending (R$)'},
                nbins=50
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🗺️ SPENDING PER CUSTOMER PER STATE")
            
            # Spending per customer per state
            state_spending = customer_spending.groupby('state').agg({
                'total_spending': 'mean',
                'customer_id': 'count'
            }).round(2).reset_index()
            
            state_spending.columns = ['state', 'avg_spending_per_customer', 'customer_count']
            state_spending = state_spending.nlargest(10, 'avg_spending_per_customer')
            
            fig = px.bar(
                state_spending,
                x='state',
                y='avg_spending_per_customer',
                title='Rata-rata Spending per Customer (Top 10 State)',
                labels={'avg_spending_per_customer': 'Rata-rata Spending (R$)', 'state': 'State'},
                color='avg_spending_per_customer',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Customer segments berdasarkan spending
            st.markdown("#### 🎯 SEGMENTASI CUSTOMER")
            
            def get_segment(spending):
                if spending < 100: return 'Low (< R$ 100)'
                elif spending < 500: return 'Medium (R$ 100-500)'
                elif spending < 2000: return 'High (R$ 500-2000)'
                else: return 'VIP (> R$ 2000)'
            
            customer_spending['segment'] = customer_spending['total_spending'].apply(get_segment)
            segment_stats = customer_spending['segment'].value_counts()
            
            fig_pie = px.pie(
                values=segment_stats.values,
                names=segment_stats.index,
                title='Distribusi Segment Customer Berdasarkan Spending'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    def create_dashboard(self):
        """Membuat dashboard utama"""
        # Header
        st.markdown('<h1 class="main-header">📊 BRAZIL E-COMMERCE DASHBOARD</h1>', unsafe_allow_html=True)
        
        # Filters
        filtered_data = self.create_filters()
        
        # Key metrics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = filtered_data['price'].sum()
            st.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
        
        with col2:
            avg_review = filtered_data['review_score'].mean()
            st.metric("Rata-rata Review", f"{avg_review:.2f}/5.0")
        
        with col3:
            total_orders = filtered_data['order_id'].nunique()
            st.metric("Total Orders", f"{total_orders:,}")
        
        with col4:
            total_customers = filtered_data['customer_unique_id'].nunique()
            st.metric("Unique Customers", f"{total_customers:,}")
        
        # Tabs utama
        st.markdown("---")
        tab1, tab2, tab3, tab4 = st.tabs([
            "⭐ REVIEW ANALYSIS", 
            "💰 REVENUE ANALYSIS", 
            "📦 PRODUCT ANALYSIS", 
            "👥 CUSTOMER ANALYSIS"
        ])
        
        with tab1:
            st.markdown("## ⭐ REVIEW ANALYSIS")
            fig_review, review_data = self.create_brazil_map(filtered_data, 'review')
            if fig_review:
                st.plotly_chart(fig_review, use_container_width=True)
            
            # Review statistics
            col1, col2 = st.columns(2)
            with col1:
                review_dist = px.histogram(
                    filtered_data, 
                    x='review_score', 
                    title='Distribusi Review Score',
                    nbins=5
                )
                st.plotly_chart(review_dist, use_container_width=True)
            
            with col2:
                state_review = filtered_data.groupby('customer_state_full')['review_score'].mean().round(2).reset_index()
                state_review = state_review.nlargest(10, 'review_score')
                fig_bar = px.bar(
                    state_review,
                    x='customer_state_full',
                    y='review_score',
                    title='Top 10 State dengan Review Tertinggi',
                    labels={'review_score': 'Rata-rata Review', 'customer_state_full': 'State'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab2:
            st.markdown("## 💰 REVENUE ANALYSIS")
            fig_revenue, revenue_data = self.create_brazil_map(filtered_data, 'revenue')
            if fig_revenue:
                st.plotly_chart(fig_revenue, use_container_width=True)
            
            # Revenue statistics
            col1, col2 = st.columns(2)
            with col1:
                state_revenue = filtered_data.groupby('customer_state_full')['price'].sum().reset_index()
                state_revenue = state_revenue.nlargest(10, 'price')
                fig_bar = px.bar(
                    state_revenue,
                    x='customer_state_full',
                    y='price',
                    title='Top 10 State dengan Revenue Tertinggi',
                    labels={'price': 'Total Revenue (R$)', 'customer_state_full': 'State'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                monthly_revenue = filtered_data.groupby(
                    filtered_data['order_purchase_timestamp'].dt.to_period('M')
                )['price'].sum().reset_index()
                monthly_revenue['order_purchase_timestamp'] = monthly_revenue['order_purchase_timestamp'].dt.to_timestamp()
                
                fig_line = px.line(
                    monthly_revenue,
                    x='order_purchase_timestamp',
                    y='price',
                    title='Trend Revenue Bulanan',
                    labels={'price': 'Revenue (R$)', 'order_purchase_timestamp': 'Bulan'}
                )
                st.plotly_chart(fig_line, use_container_width=True)
        
        with tab3:
            st.markdown("## 📦 PRODUCT ANALYSIS")
            self.display_product_rankings(filtered_data)
        
        with tab4:
            st.markdown("## 👥 CUSTOMER ANALYSIS")
            self.display_customer_analysis(filtered_data)

def main():
    # Initialize dan jalankan dashboard
    dashboard = BrazilEcommerceDashboard()
    dashboard.create_dashboard()

if __name__ == "__main__":
    main()

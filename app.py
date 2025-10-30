import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
import io

# Konfigurasi page
st.set_page_config(
    page_title="Brazil E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk tampilan minimalis
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .mini-metric {
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6c757d;
    }
    .ranking-item-top {
        background: linear-gradient(90deg, #d4edda, #f8f9fa);
        padding: 0.6rem;
        margin-bottom: 0.3rem;
        border-radius: 6px;
        border-left: 4px solid #28a745;
    }
    .ranking-item-bottom {
        background: linear-gradient(90deg, #f8d7da, #f8f9fa);
        padding: 0.6rem;
        margin-bottom: 0.3rem;
        border-radius: 6px;
        border-left: 4px solid #dc3545;
    }
    .ranking-number {
        font-weight: bold;
        font-size: 1rem;
        color: #495057;
    }
    .ranking-name {
        font-size: 0.9rem;
        color: #495057;
        margin: 0 0.5rem;
    }
    .ranking-score {
        font-weight: bold;
        font-size: 0.9rem;
        color: #28a745;
    }
    .ranking-score-bad {
        font-weight: bold;
        font-size: 0.9rem;
        color: #dc3545;
    }
    .segment-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .segment-low { border-left-color: #dc3545; background: linear-gradient(90deg, #f8d7da, white); }
    .segment-medium { border-left-color: #ffc107; background: linear-gradient(90deg, #fff3cd, white); }
    .segment-high { border-left-color: #007bff; background: linear-gradient(90deg, #cce7ff, white); }
    .segment-vip { border-left-color: #28a745; background: linear-gradient(90deg, #d4edda, white); }
    .repeat-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #6f42c1;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(90deg, #e2e3e5, white);
    }
</style>
""", unsafe_allow_html=True)

class BrazilEcommerceDashboard:
    def __init__(self, data_url):
        self.data_url = data_url
        self.load_data()
        self.setup_brazil_coordinates()
        
    def setup_brazil_coordinates(self):
        """Setup koordinat manual untuk states Brazil"""
        self.brazil_states_coords = {
            'AC': {'lat': -9.0238, 'lon': -70.8120},
            'AL': {'lat': -9.5713, 'lon': -36.7820},
            'AP': {'lat': 1.4544, 'lon': -51.9482},
            'AM': {'lat': -4.7936, 'lon': -64.6505},
            'BA': {'lat': -12.5797, 'lon': -41.7007},
            'CE': {'lat': -5.4984, 'lon': -39.3206},
            'DF': {'lat': -15.7797, 'lon': -47.9297},
            'ES': {'lat': -19.1834, 'lon': -40.3089},
            'GO': {'lat': -16.3291, 'lon': -49.8501},
            'MA': {'lat': -4.9609, 'lon': -45.2744},
            'MT': {'lat': -12.6819, 'lon': -56.9211},
            'MS': {'lat': -20.7722, 'lon': -54.7852},
            'MG': {'lat': -18.5122, 'lon': -44.5550},
            'PA': {'lat': -3.8191, 'lon': -52.7630},
            'PB': {'lat': -7.2399, 'lon': -36.7819},
            'PR': {'lat': -24.8932, 'lon': -51.5870},
            'PE': {'lat': -8.8137, 'lon': -36.9541},
            'PI': {'lat': -7.7183, 'lon': -42.7289},
            'RJ': {'lat': -22.3530, 'lon': -42.6960},
            'RN': {'lat': -5.4026, 'lon': -36.9541},
            'RS': {'lat': -30.0346, 'lon': -51.2177},
            'RO': {'lat': -11.5057, 'lon': -63.5806},
            'RR': {'lat': 2.7376, 'lon': -62.0751},
            'SC': {'lat': -27.2423, 'lon': -50.2189},
            'SP': {'lat': -23.5505, 'lon': -46.6333},
            'SE': {'lat': -10.5741, 'lon': -37.3857},
            'TO': {'lat': -9.9725, 'lon': -48.1882}
        }
        
    def load_data(self):
        """Load data dari URL GitHub"""
        try:
            # Jika URL adalah raw GitHub URL
            if self.data_url.startswith('https://raw.githubusercontent.com/'):
                self.df = pd.read_csv(self.data_url)
            else:
                # Untuk URL lain, gunakan requests
                response = requests.get(self.data_url)
                self.df = pd.read_csv(io.StringIO(response.text))
            
            # Data preprocessing
            self.preprocess_data()
            
            st.success(f"✅ Data berhasil dimuat! Total {len(self.df):,} records")
            
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.info("🔧 Menggunakan sample data sebagai fallback...")
            self.create_sample_data()
    
    def preprocess_data(self):
        """Preprocess data yang di-load"""
        # Convert timestamp
        self.df['order_purchase_timestamp'] = pd.to_datetime(
            self.df['order_purchase_timestamp'], errors='coerce'
        )
        
        # Extract time features
        self.df['tahun'] = self.df['order_purchase_timestamp'].dt.year
        self.df['bulan'] = self.df['order_purchase_timestamp'].dt.month
        
        # State mapping untuk display
        state_names = {
            'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
            'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 
            'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão',
            'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
            'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco',
            'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima',
            'SC': 'Santa Catarina', 'SP': 'São Paulo', 'SE': 'Sergipe',
            'TO': 'Tocantins'
        }
        
        self.df['nama_state'] = self.df['customer_state'].map(state_names)
        
        # Handle missing values untuk kolom penting
        if 'review_score' in self.df.columns:
            self.df['review_score'] = self.df['review_score'].fillna(3.0)
        else:
            self.df['review_score'] = 3.0  # Default value
            
        if 'price' in self.df.columns:
            self.df['price'] = self.df['price'].fillna(0)
        else:
            self.df['price'] = 0
    
    def create_sample_data(self):
        """Membuat sample data jika loading gagal"""
        st.warning("Membuat sample data untuk demonstrasi...")
        
        # Sample data structure berdasarkan kolom yang disebutkan
        sample_size = 1000
        self.df = pd.DataFrame({
            'order_id': [f'order_{i}' for i in range(sample_size)],
            'customer_id': [f'customer_{i%100}' for i in range(sample_size)],
            'order_status': np.random.choice(['delivered', 'shipped', 'processing'], sample_size),
            'order_purchase_timestamp': pd.date_range('2022-01-01', periods=sample_size, freq='H'),
            'customer_unique_id': [f'unique_cust_{i%50}' for i in range(sample_size)],
            'customer_zip_code_prefix': np.random.randint(1000, 9999, sample_size),
            'customer_city': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Brasilia'], sample_size),
            'customer_state': np.random.choice(['SP', 'RJ', 'MG', 'RS', 'PR'], sample_size),
            'order_item_id': range(1, sample_size + 1),
            'product_id': [f'product_{i%20}' for i in range(sample_size)],
            'seller_id': [f'seller_{i%10}' for i in range(sample_size)],
            'price': np.random.uniform(10, 500, sample_size),
            'freight_value': np.random.uniform(5, 50, sample_size),
            'product_category_name': np.random.choice(['electronics', 'home', 'books', 'sports'], sample_size),
            'product_category_name_english': np.random.choice(['Electronics', 'Home', 'Books', 'Sports'], sample_size),
            'review_score': np.random.randint(1, 6, sample_size),
            'payment_value': np.random.uniform(15, 550, sample_size),
            'purchase_hour': np.random.randint(0, 24, sample_size),
            'time_period': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], sample_size)
        })
        
        self.preprocess_data()
    
    def create_minimal_filters(self):
        """Membuat filter minimalis"""
        st.markdown("---")
        
        with st.expander("🎛️ **FILTER SETTINGS**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                # Filter Tahun
                tahun_options = ['All Time'] + sorted(self.df['tahun'].unique())
                selected_year = st.selectbox(
                    "**Pilih Periode Waktu:**",
                    options=tahun_options,
                    index=0
                )
            
            with col2:
                # Filter Periode Waktu
                if 'time_period' in self.df.columns:
                    time_period_options = ['All'] + sorted(self.df['time_period'].dropna().unique())
                    selected_time_period = st.selectbox(
                        "**Pilih Periode Hari:**",
                        options=time_period_options,
                        index=0
                    )
                else:
                    selected_time_period = 'All'
            
            # Apply filters
            filtered_data = self.df.copy()
            
            if selected_year != 'All Time':
                filtered_data = filtered_data[filtered_data['tahun'] == selected_year]
            
            if selected_time_period != 'All':
                filtered_data = filtered_data[filtered_data['time_period'] == selected_time_period]
            
            return filtered_data, selected_year
    
    def create_mini_metric(self, value, label, icon):
        """Membuat metric card minimalis"""
        st.markdown(f"""
        <div class="mini-metric">
            <div class="metric-value">{icon} {value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def display_minimal_review_metrics(self, data):
        """Menampilkan metric cards untuk review"""
        with st.expander("📊 **REVIEW METRICS**", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_review = data['review_score'].mean()
                self.create_mini_metric(f"{avg_review:.2f}/5.0", "Rata-rata Review", "⭐")
                
            with col2:
                positive_reviews = (data['review_score'] >= 4).sum()
                total_reviews = len(data)
                positive_pct = (positive_reviews / total_reviews * 100) if total_reviews > 0 else 0
                self.create_mini_metric(f"{positive_pct:.1f}%", "Review Positif (≥4)", "😊")
                
            with col3:
                negative_reviews = (data['review_score'] <= 2).sum()
                negative_pct = (negative_reviews / total_reviews * 100) if total_reviews > 0 else 0
                self.create_mini_metric(f"{negative_pct:.1f}%", "Review Negatif (≤2)", "😞")
                
            with col4:
                total_reviews_count = total_reviews
                self.create_mini_metric(f"{total_reviews_count:,}", "Total Review", "📝")
    
    def display_minimal_revenue_metrics(self, data):
        """Menampilkan metric cards untuk revenue"""
        with st.expander("💰 **REVENUE METRICS**", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_revenue = data['price'].sum()
                self.create_mini_metric(f"R$ {total_revenue:,.0f}", "Total Revenue", "💰")
                
            with col2:
                total_orders = data['order_id'].nunique()
                self.create_mini_metric(f"{total_orders:,}", "Total Orders", "📦")
                
            with col3:
                total_customers = data['customer_unique_id'].nunique()
                self.create_mini_metric(f"{total_customers:,}", "Unique Customers", "👥")
                
            with col4:
                avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
                self.create_mini_metric(f"R$ {avg_order_value:.2f}", "Avg Order Value", "📊")
    
    def display_customer_spending_metrics(self, data):
        """Menampilkan metric cards untuk customer spending"""
        with st.expander("👥 **CUSTOMER SPENDING METRICS**", expanded=False):
            customer_spending = data.groupby('customer_unique_id').agg({
                'price': 'sum'
            }).reset_index()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_spending = customer_spending['price'].mean()
                self.create_mini_metric(f"R$ {avg_spending:.2f}", "Rata-rata Spending/Customer", "💰")
                
            with col2:
                median_spending = customer_spending['price'].median()
                self.create_mini_metric(f"R$ {median_spending:.2f}", "Median Spending/Customer", "📊")
                
            with col3:
                total_customers = customer_spending['customer_unique_id'].nunique()
                self.create_mini_metric(f"{total_customers:,}", "Total Unique Customers", "👥")
                
            with col4:
                total_revenue = customer_spending['price'].sum()
                self.create_mini_metric(f"R$ {total_revenue:,.0f}", "Total Customer Spending", "💎")
    
    def create_simple_map(self, data, score_type='review'):
        """Membuat peta Brazil sederhana"""
        # Aggregate data per state
        state_col = 'customer_state'
        
        if score_type == 'review':
            state_data = data.groupby(state_col)['review_score'].mean().round(3).reset_index()
            state_data.columns = ['state', 'score']
        else:
            state_data = data.groupby(state_col).agg({'price': 'sum'}).round(0).reset_index()
            state_data.columns = ['state', 'score']
        
        # Tambahkan koordinat
        state_data['lat'] = state_data['state'].map(lambda x: self.brazil_states_coords.get(x, {}).get('lat', 0))
        state_data['lon'] = state_data['state'].map(lambda x: self.brazil_states_coords.get(x, {}).get('lon', 0))
        state_data = state_data[state_data['lat'] != 0]
        
        if score_type == 'review':
            z_col = 'score'
            title = 'Rata-rata Review Score'
            colorscale = 'RdYlGn'
            colorbar_title = "Review Score"
            
            hover_texts = []
            for idx, row in state_data.iterrows():
                text = f"{row['state']}<br>Review: {row[z_col]:.2f}"
                hover_texts.append(text)
                
        else:
            z_col = 'score'
            title = 'Total Revenue (R$)'
            colorscale = 'Blues'
            colorbar_title = "Revenue (R$)"
            
            hover_texts = []
            for idx, row in state_data.iterrows():
                text = f"{row['state']}<br>Revenue: R$ {row[z_col]:,.0f}"
                hover_texts.append(text)
        
        # Buat peta
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon = state_data['lon'],
            lat = state_data['lat'],
            text = hover_texts,
            hoverinfo = 'text',
            marker = dict(
                size = 25,
                color = state_data[z_col],
                colorscale = colorscale,
                colorbar = dict(title=colorbar_title, thickness=15),
                line = dict(width=1, color='white'),
            )
        ))
        
        fig.update_layout(
            title = dict(text=f"<b>{title}</b>", x=0.5, xanchor='center'),
            geo = dict(
                scope = 'south america',
                showland = True,
                landcolor = 'rgb(243, 243, 243)',
                countrycolor = 'rgb(204, 204, 204)',
                showcountries = True,
                center=dict(lat=-14, lon=-55),
                projection_scale=3
            ),
            height = 400,
            margin = dict(l=0, r=0, t=40, b=0)
        )
        
        return fig, state_data
    
    def create_customer_spending_map(self, data):
        """Membuat peta spending per customer"""
        state_data = data.groupby('customer_state').agg({
            'price': 'sum',
            'customer_unique_id': 'nunique'
        }).round(2)
        
        state_data.columns = ['total_revenue', 'unique_customers']
        state_data['spending_per_customer'] = (state_data['total_revenue'] / state_data['unique_customers']).round(2)
        state_data = state_data.reset_index()
        
        # Tambahkan koordinat
        state_data['lat'] = state_data['customer_state'].map(lambda x: self.brazil_states_coords.get(x, {}).get('lat', 0))
        state_data['lon'] = state_data['customer_state'].map(lambda x: self.brazil_states_coords.get(x, {}).get('lon', 0))
        state_data = state_data[state_data['lat'] != 0]
        
        # Format hover text
        hover_texts = []
        for idx, row in state_data.iterrows():
            text = f"{row['customer_state']}<br>Spending/Customer: R$ {row['spending_per_customer']:.2f}<br>Total Customers: {row['unique_customers']:,}"
            hover_texts.append(text)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon = state_data['lon'],
            lat = state_data['lat'],
            text = hover_texts,
            hoverinfo = 'text',
            marker = dict(
                size = 25,
                color = state_data['spending_per_customer'],
                colorscale = 'Viridis',
                colorbar = dict(title="Spending/Customer (R$)", thickness=20),
                line = dict(width=2, color='white'),
            )
        ))
        
        fig.update_layout(
            title = dict(text="<b>Average Spending per Customer by State</b>", x=0.5),
            geo = dict(
                scope = 'south america',
                showland = True,
                landcolor = 'rgb(243, 243, 243)',
                countrycolor = 'rgb(204, 204, 204)',
                center=dict(lat=-14, lon=-55),
                projection_scale=3
            ),
            height = 500,
            margin = dict(l=0, r=0, t=50, b=0)
        )
        
        return fig, state_data
    
    def display_spending_segments(self, data):
        """Menampilkan segmentasi spending customer"""
        customer_spending = data.groupby('customer_unique_id').agg({
            'price': 'sum'
        }).reset_index()
        
        total_customers = len(customer_spending)
        
        def get_spending_segment(spending):
            if spending < 100: return 'Low (< R$ 100)'
            elif spending < 500: return 'Medium (R$ 100-500)'
            elif spending < 2000: return 'High (R$ 500-2000)'
            else: return 'VIP (> R$ 2000)'
        
        customer_spending['segment'] = customer_spending['price'].apply(get_spending_segment)
        
        segment_stats = customer_spending.groupby('segment').agg({
            'customer_unique_id': 'count',
            'price': ['sum', 'mean']
        }).round(2)
        
        segment_stats.columns = ['customer_count', 'total_spending', 'avg_spending']
        segment_stats = segment_stats.reset_index()
        segment_stats['percentage'] = (segment_stats['customer_count'] / total_customers * 100).round(1)
        
        segment_order = ['Low (< R$ 100)', 'Medium (R$ 100-500)', 'High (R$ 500-2000)', 'VIP (> R$ 2000)']
        segment_stats['segment'] = pd.Categorical(segment_stats['segment'], categories=segment_order, ordered=True)
        segment_stats = segment_stats.sort_values('segment')
        
        st.markdown("### 🎯 CUSTOMER SPENDING SEGMENTS")
        
        for idx, row in segment_stats.iterrows():
            segment_class = {
                'Low (< R$ 100)': 'segment-low',
                'Medium (R$ 100-500)': 'segment-medium', 
                'High (R$ 500-2000)': 'segment-high',
                'VIP (> R$ 2000)': 'segment-vip'
            }[row['segment']]
            
            st.markdown(f"""
            <div class="segment-card {segment_class}">
                <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">
                    {row['segment']} <span style="font-size: 0.9rem; color: #6c757d;">({row['percentage']}%)</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Customers</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">{row['customer_count']:,}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Total Spending</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">R$ {row['total_spending']:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Avg/Person</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">R$ {row['avg_spending']:.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def display_repeat_purchase_analysis(self, data):
        """Menampilkan analisis repeat purchase"""
        customer_orders = data.groupby('customer_unique_id').agg({
            'order_id': 'nunique',
            'price': 'sum'
        }).reset_index()
        
        customer_orders.columns = ['customer_id', 'order_count', 'total_spending']
        total_customers = len(customer_orders)
        
        def get_repeat_segment(order_count):
            if order_count == 1: return 'One-time'
            elif order_count <= 3: return 'Occasional (2-3)'
            elif order_count <= 10: return 'Regular (4-10)'
            else: return 'Frequent (>10)'
        
        customer_orders['repeat_segment'] = customer_orders['order_count'].apply(get_repeat_segment)
        
        repeat_stats = customer_orders.groupby('repeat_segment').agg({
            'customer_id': 'count',
            'order_count': 'mean',
            'total_spending': ['sum', 'mean']
        }).round(2)
        
        repeat_stats.columns = ['customer_count', 'avg_orders', 'total_spending', 'avg_spending']
        repeat_stats = repeat_stats.reset_index()
        repeat_stats['percentage'] = (repeat_stats['customer_count'] / total_customers * 100).round(1)
        
        repeat_order = ['One-time', 'Occasional (2-3)', 'Regular (4-10)', 'Frequent (>10)']
        repeat_stats['repeat_segment'] = pd.Categorical(repeat_stats['repeat_segment'], categories=repeat_order, ordered=True)
        repeat_stats = repeat_stats.sort_values('repeat_segment')
        
        st.markdown("### 🔄 REPEAT PURCHASE SEGMENTS")
        
        for idx, row in repeat_stats.iterrows():
            st.markdown(f"""
            <div class="repeat-card">
                <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">
                    {row['repeat_segment']} <span style="font-size: 0.9rem; color: #6c757d;">({row['percentage']}%)</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem;">
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Customers</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">{row['customer_count']:,}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Avg Orders</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">{row['avg_orders']:.1f}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Total Spending</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">R$ {row['total_spending']:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9

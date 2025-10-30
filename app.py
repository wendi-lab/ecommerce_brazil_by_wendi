import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

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
    .full-width-map {
        width: 100%;
        height: 600px;
    }
</style>
""", unsafe_allow_html=True)

class FinalCleanBrazilEcommerceDashboard:
    def __init__(self, data_path="main_data.csv"):
        self.data_path = data_path
        self.load_data()
        self.setup_brazil_coordinates()
        
    def setup_brazil_coordinates(self):
        """Setup koordinat manual untuk states Brazil"""
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
            # Cek apakah file ada
            if not os.path.exists(self.data_path):
                st.error(f"❌ File '{self.data_path}' tidak ditemukan. Pastikan file berada dalam folder yang sama dengan script ini.")
                st.stop()
            
            self.df = pd.read_csv(self.data_path)
            
            # Convert timestamp
            self.df['order_purchase_timestamp'] = pd.to_datetime(
                self.df['order_purchase_timestamp'], errors='coerce'
            )
            
            # Extract time features
            self.df['tahun'] = self.df['order_purchase_timestamp'].dt.year
            self.df['bulan'] = self.df['order_purchase_timestamp'].dt.month
            
            # State mapping
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
            
            st.success(f"✅ Data berhasil dimuat! Total {len(self.df):,} records")
            
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.stop()
    
    def create_minimal_filters(self):
        """Membuat filter minimalis di bawah header"""
        st.markdown("---")
        
        with st.expander("🎛️ **FILTER SETTINGS**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                # Filter Tahun dengan opsi All Time
                tahun_options = ['All Time'] + sorted(self.df['tahun'].unique())
                selected_year = st.selectbox(
                    "**Pilih Periode Waktu:**",
                    options=tahun_options,
                    index=0
                )
            
            with col2:
                # Filter Periode Waktu
                if 'time_period' in self.df.columns:
                    time_period_options = sorted(self.df['time_period'].dropna().unique())
                    selected_time_period = st.multiselect(
                        "**Pilih Periode Hari:**",
                        options=time_period_options,
                        default=time_period_options
                    )
                else:
                    selected_time_period = None
            
            # Apply filters
            filtered_data = self.df.copy()
            
            if selected_year != 'All Time':
                filtered_data = filtered_data[filtered_data['tahun'] == selected_year]
            
            if selected_time_period:
                filtered_data = filtered_data[filtered_data['time_period'].isin(selected_time_period)]
            
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
        """Menampilkan metric cards minimalis untuk review"""
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
        """Menampilkan metric cards minimalis untuk revenue"""
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
            # Hitung spending per customer per state
            customer_spending = data.groupby('customer_unique_id').agg({
                'price': 'sum',
                'nama_state': 'first'
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
        """Membuat peta Brazil sederhana yang pasti work"""
        # Aggregate data per state
        if 'customer_state_full' in data.columns:
            state_col = 'customer_state_full'
        else:
            state_col = 'nama_state'
        
        state_data = data.groupby(state_col).agg({
            'review_score': 'mean',
            'price': 'sum'
        }).round(3)
        
        state_data.columns = ['avg_review', 'total_revenue']
        state_data = state_data.reset_index()
        
        # Tambahkan koordinat
        state_data['lat'] = state_data[state_col].map(lambda x: self.brazil_states_coords.get(x, {}).get('lat', 0))
        state_data['lon'] = state_data[state_col].map(lambda x: self.brazil_states_coords.get(x, {}).get('lon', 0))
        state_data = state_data[state_data['lat'] != 0]
        
        if score_type == 'review':
            z_col = 'avg_review'
            title = 'Rata-rata Review Score'
            colorscale = 'RdYlGn'
            color_min = 3.0
            color_max = 5.0
            colorbar_title = "Review Score"
            
            # Format hover text dengan aman
            hover_texts = []
            for idx, row in state_data.iterrows():
                text = f"{row[state_col]}<br>Review: {row[z_col]:.2f}"
                hover_texts.append(text)
                
        else:
            z_col = 'total_revenue'
            title = 'Total Revenue (R$)'
            colorscale = 'Blues'
            color_min = state_data[z_col].min()
            color_max = state_data[z_col].max()
            colorbar_title = "Revenue (R$)"
            
            # Format hover text dengan aman
            hover_texts = []
            for idx, row in state_data.iterrows():
                text = f"{row[state_col]}<br>Revenue: R$ {row[z_col]:,.0f}"
                hover_texts.append(text)
        
        # Buat peta dengan scattergeo
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon = state_data['lon'],
            lat = state_data['lat'],
            text = hover_texts,
            hoverinfo = 'text',
            marker = dict(
                size = 20,
                color = state_data[z_col],
                colorscale = colorscale,
                cmin = color_min,
                cmax = color_max,
                colorbar = dict(
                    title = colorbar_title,
                    thickness = 15
                ),
                line = dict(width=1, color='white'),
            )
        ))
        
        fig.update_layout(
            title = dict(
                text = f"<b>{title}</b>",
                x = 0.5,
                xanchor = 'center',
                font = dict(size=14)
            ),
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
        """Membuat peta spending per customer dengan ukuran maksimal"""
        # Aggregate data per state - revenue dan unique customers
        if 'customer_state_full' in data.columns:
            state_col = 'customer_state_full'
        else:
            state_col = 'nama_state'
        
        state_data = data.groupby(state_col).agg({
            'price': 'sum',
            'customer_unique_id': 'nunique'
        }).round(2)
        
        state_data.columns = ['total_revenue', 'unique_customers']
        
        # Hitung spending per customer
        state_data['spending_per_customer'] = (state_data['total_revenue'] / state_data['unique_customers']).round(2)
        state_data = state_data.reset_index()
        
        # Tambahkan koordinat
        state_data['lat'] = state_data[state_col].map(lambda x: self.brazil_states_coords.get(x, {}).get('lat', 0))
        state_data['lon'] = state_data[state_col].map(lambda x: self.brazil_states_coords.get(x, {}).get('lon', 0))
        state_data = state_data[state_data['lat'] != 0]
        
        # Format hover text
        hover_texts = []
        for idx, row in state_data.iterrows():
            text = f"{row[state_col]}<br>Spending/Customer: R$ {row['spending_per_customer']:.2f}<br>Total Customers: {row['unique_customers']:,}<br>Total Revenue: R$ {row['total_revenue']:,.0f}"
            hover_texts.append(text)
        
        # Buat peta dengan ukuran lebih besar
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon = state_data['lon'],
            lat = state_data['lat'],
            text = hover_texts,
            hoverinfo = 'text',
            marker = dict(
                size = 25,  # Ukuran marker lebih besar
                color = state_data['spending_per_customer'],
                colorscale = 'Viridis',
                cmin = state_data['spending_per_customer'].min(),
                cmax = state_data['spending_per_customer'].max(),
                colorbar = dict(
                    title = "Spending/Customer (R$)",
                    thickness = 20,
                    len = 0.8
                ),
                line = dict(width=2, color='white'),
            )
        ))
        
        fig.update_layout(
            title = dict(
                text = "<b>Average Spending per Customer by State</b>",
                x = 0.5,
                xanchor = 'center',
                font = dict(size=16)
            ),
            geo = dict(
                scope = 'south america',
                showland = True,
                landcolor = 'rgb(243, 243, 243)',
                countrycolor = 'rgb(204, 204, 204)',
                showcountries = True,
                showocean = True,
                oceancolor = 'rgb(204, 229, 255)',
                center=dict(lat=-14, lon=-55),
                projection_scale=3.2,  # Zoom level lebih besar
                lonaxis_range=[-75, -30],  # Batas longitude
                lataxis_range=[-35, 5],    # Batas latitude
            ),
            height = 600,  # Tinggi peta lebih besar
            margin = dict(l=0, r=0, t=50, b=0)
        )
        
        return fig, state_data
    
    def display_spending_segments(self, data):
        """Menampilkan segmentasi spending customer dengan % distribusi"""
        # Hitung spending per customer
        customer_spending = data.groupby('customer_unique_id').agg({
            'price': 'sum'
        }).reset_index()
        
        total_customers = len(customer_spending)
        
        # Definisikan segmentasi
        def get_spending_segment(spending):
            if spending < 100:
                return 'Low (< R$ 100)'
            elif spending < 500:
                return 'Medium (R$ 100-500)'
            elif spending < 2000:
                return 'High (R$ 500-2000)'
            else:
                return 'VIP (> R$ 2000)'
        
        # Terapkan segmentasi
        customer_spending['segment'] = customer_spending['price'].apply(get_spending_segment)
        
        # Hitung statistik per segment
        segment_stats = customer_spending.groupby('segment').agg({
            'customer_unique_id': 'count',
            'price': ['sum', 'mean', 'median']
        }).round(2)
        
        segment_stats.columns = ['customer_count', 'total_spending', 'avg_spending', 'median_spending']
        segment_stats = segment_stats.reset_index()
        
        # Hitung persentase
        segment_stats['percentage'] = (segment_stats['customer_count'] / total_customers * 100).round(1)
        
        # Urutkan berdasarkan segment
        segment_order = ['Low (< R$ 100)', 'Medium (R$ 100-500)', 'High (R$ 500-2000)', 'VIP (> R$ 2000)']
        segment_stats['segment'] = pd.Categorical(segment_stats['segment'], categories=segment_order, ordered=True)
        segment_stats = segment_stats.sort_values('segment')
        
        # Tampilkan segment cards dengan persentase
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
        """Menampilkan analisis repeat purchase berdasarkan segment"""
        # Hitung jumlah order per customer
        customer_orders = data.groupby('customer_unique_id').agg({
            'order_id': 'nunique',
            'price': 'sum'
        }).reset_index()
        
        customer_orders.columns = ['customer_id', 'order_count', 'total_spending']
        
        total_customers = len(customer_orders)
        
        # Definisikan segment repeat purchase
        def get_repeat_segment(order_count):
            if order_count == 1:
                return 'One-time'
            elif order_count <= 3:
                return 'Occasional (2-3)'
            elif order_count <= 10:
                return 'Regular (4-10)'
            else:
                return 'Frequent (>10)'
        
        # Terapkan segmentasi repeat purchase
        customer_orders['repeat_segment'] = customer_orders['order_count'].apply(get_repeat_segment)
        
        # Hitung statistik per segment repeat
        repeat_stats = customer_orders.groupby('repeat_segment').agg({
            'customer_id': 'count',
            'order_count': 'mean',
            'total_spending': ['sum', 'mean']
        }).round(2)
        
        repeat_stats.columns = ['customer_count', 'avg_orders', 'total_spending', 'avg_spending']
        repeat_stats = repeat_stats.reset_index()
        
        # Hitung persentase
        repeat_stats['percentage'] = (repeat_stats['customer_count'] / total_customers * 100).round(1)
        
        # Urutkan berdasarkan order count (bukan alphabet)
        repeat_order = ['One-time', 'Occasional (2-3)', 'Regular (4-10)', 'Frequent (>10)']
        repeat_stats['repeat_segment'] = pd.Categorical(repeat_stats['repeat_segment'], categories=repeat_order, ordered=True)
        repeat_stats = repeat_stats.sort_values('repeat_segment')
        
        # Tampilkan repeat purchase segments
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
                        <div style="font-size: 0.9rem; color: #6c757d;">Avg/Person</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">R$ {row['avg_spending']:.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def display_state_ranking_vertical(self, data, score_type='review'):
        """Menampilkan ranking state secara vertikal"""
        # Aggregate data per state
        if 'customer_state_full' in data.columns:
            state_col = 'customer_state_full'
        else:
            state_col = 'nama_state'
        
        if score_type == 'review':
            state_scores = data.groupby(state_col)['review_score'].mean().round(3).reset_index()
            state_scores.columns = ['state', 'score']
        else:  # revenue
            state_scores = data.groupby(state_col).agg({'price': 'sum'}).round(0).reset_index()
            state_scores.columns = ['state', 'score']
        
        # Top 5 dan Bottom 5
        top_5 = state_scores.nlargest(5, 'score')
        bottom_5 = state_scores.nsmallest(5, 'score')
        
        # Display TOP 1 dengan besar
        if len(top_5) > 0:
            st.markdown(f"**🥇 {top_5.iloc[0]['state']}**")
            if score_type == 'review':
                st.markdown(f"<div style='font-size: 1.5rem; font-weight: bold; color: #28a745; text-align: center;'>{top_5.iloc[0]['score']:.2f}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='font-size: 1.5rem; font-weight: bold; color: #28a745; text-align: center;'>R$ {top_5.iloc[0]['score']:,.0f}</div>", unsafe_allow_html=True)
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**TOP 2-5**")
            for i in range(1, min(5, len(top_5))):
                state = top_5.iloc[i]
                score_display = f"{state['score']:.2f}" if score_type == 'review' else f"R$ {state['score']:,.0f}"
                st.markdown(f"<div class='ranking-item-top'>"
                           f"<span class='ranking-number'>#{i+1}</span>"
                           f"<span class='ranking-name'>{state['state']}</span>"
                           f"<span class='ranking-score'>{score_display}</span>"
                           f"</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("**BOTTOM 5**")
            for i in range(min(5, len(bottom_5))):
                state = bottom_5.iloc[i]
                score_display = f"{state['score']:.2f}" if score_type == 'review' else f"R$ {state['score']:,.0f}"
                st.markdown(f"<div class='ranking-item-bottom'>"
                           f"<span class='ranking-number'>#{len(state_scores)-4+i}</span>"
                           f"<span class='ranking-name'>{state['state']}</span>"
                           f"<span class='ranking-score-bad'>{score_display}</span>"
                           f"</div>", unsafe_allow_html=True)
    
    def display_product_rankings(self, data):
        """Menampilkan ranking produk berdasarkan review dan revenue"""
        if 'product_category_name_english' not in data.columns:
            st.warning("Data kategori produk tidak tersedia")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📦 TOP 5 KATEGORI - REVIEW**")
            # Review ranking
            category_review = data.groupby('product_category_name_english')['review_score'].mean().round(3).reset_index()
            category_review = category_review[category_review['review_score'].notna()]
            category_review = category_review[category_review['product_category_name_english'].notna()]
            
            # Filter hanya kategori dengan cukup data
            category_counts = data.groupby('product_category_name_english').size()
            valid_categories = category_counts[category_counts > 10].index
            category_review = category_review[category_review['product_category_name_english'].isin(valid_categories)]
            
            top_5_review = category_review.nlargest(5, 'review_score')
            bottom_5_review = category_review.nsmallest(5, 'review_score')
            
            for i, (idx, row) in enumerate(top_5_review.iterrows(), 1):
                st.markdown(f"<div class='ranking-item-top'>"
                           f"<span class='ranking-number'>#{i}</span>"
                           f"<span class='ranking-name'>{row['product_category_name_english']}</span>"
                           f"<span class='ranking-score'>{row['review_score']:.2f}</span>"
                           f"</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**📉 BOTTOM 5 KATEGORI - REVIEW**")
            for i, (idx, row) in enumerate(bottom_5_review.iterrows(), 1):
                st.markdown(f"<div class='ranking-item-bottom'>"
                           f"<span class='ranking-number'>#{i}</span>"
                           f"<span class='ranking-name'>{row['product_category_name_english']}</span>"
                           f"<span class='ranking-score-bad'>{row['review_score']:.2f}</span>"
                           f"</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("**💰 TOP 5 KATEGORI - REVENUE**")
            # Revenue ranking
            category_revenue = data.groupby('product_category_name_english')['price'].sum().round(0).reset_index()
            category_revenue = category_revenue[category_revenue['price'].notna()]
            category_revenue = category_revenue[category_revenue['product_category_name_english'].notna()]
            
            top_5_revenue = category_revenue.nlargest(5, 'price')
            bottom_5_revenue = category_revenue.nsmallest(5, 'price')
            
            for i, (idx, row) in enumerate(top_5_revenue.iterrows(), 1):
                st.markdown(f"<div class='ranking-item-top'>"
                           f"<span class='ranking-number'>#{i}</span>"
                           f"<span class='ranking-name'>{row['product_category_name_english']}</span>"
                           f"<span class='ranking-score'>R$ {row['price']:,.0f}</span>"
                           f"</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**📊 BOTTOM 5 KATEGORI - REVENUE**")
            for i, (idx, row) in enumerate(bottom_5_revenue.iterrows(), 1):
                st.markdown(f"<div class='ranking-item-bottom'>"
                           f"<span class='ranking-number'>#{i}</span>"
                           f"<span class='ranking-name'>{row['product_category_name_english']}</span>"
                           f"<span class='ranking-score-bad'>R$ {row['price']:,.0f}</span>"
                           f"</div>", unsafe_allow_html=True)
    
    def create_dashboard(self):
        """Membuat dashboard utama dengan tabs"""
        # Header
        st.markdown('<h1 class="main-header">📊 BRAZIL E-COMMERCE DASHBOARD</h1>', unsafe_allow_html=True)
        
        # Filter minimalis
        filtered_data, selected_period = self.create_minimal_filters()
        
        # Tabs utama
        tab1, tab2, tab3, tab4 = st.tabs(["⭐ REVIEW ANALYSIS", "💰 REVENUE ANALYSIS", "📦 PRODUCT ANALYSIS", "👥 CUSTOMER ANALYSIS"])
        
        with tab1:
            # Metrics expandable
            self.display_minimal_review_metrics(filtered_data)
            
            # Layout utama
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown("**🗺️ PETA REVIEW BRAZIL**")
                fig, state_data = self.create_simple_map(filtered_data, 'review')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**🏆 RANKING STATE**")
                self.display_state_ranking_vertical(filtered_data, 'review')
        
        with tab2:
            # Metrics expandable
            self.display_minimal_revenue_metrics(filtered_data)
            
            # Layout utama
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown("**🗺️ PETA REVENUE BRAZIL**")
                fig, state_data = self.create_simple_map(filtered_data, 'revenue')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**🏆 RANKING STATE**")
                self.display_state_ranking_vertical(filtered_data, 'revenue')
        
        with tab3:
            st.markdown("### 📦 PRODUCT PERFORMANCE ANALYSIS")
            self.display_product_rankings(filtered_data)
        
        with tab4:
            # Metrics untuk customer spending
            self.display_customer_spending_metrics(filtered_data)
            
            st.markdown("---")
            
            # Layout untuk customer analysis - FULL WIDTH untuk peta
            st.markdown("**🗺️ PETA SPENDING PER CUSTOMER - BRAZIL**")
            fig, state_data = self.create_customer_spending_map(filtered_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Spending segments dan repeat purchase analysis di bawah peta
            col1, col2 = st.columns(2)
            
            with col1:
                self.display_spending_segments(filtered_data)
            
            with col2:
                self.display_repeat_purchase_analysis(filtered_data)

def main():
    # Initialize dan jalankan dashboard
    dashboard = FinalCleanBrazilEcommerceDashboard("main_data.csv")
    dashboard.create_dashboard()

if __name__ == "__main__":
    main()

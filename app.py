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
    .correlation-high {
        color: #28a745;
        font-weight: bold;
    }
    .correlation-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .correlation-low {
        color: #dc3545;
        font-weight: bold;
    }
    .time-period-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid;
    }
    .period-dawn { border-left-color: #4e54c8; background: linear-gradient(90deg, #8f94fb, white); }
    .period-morning { border-left-color: #ff9a00; background: linear-gradient(90deg, #ffeca0, white); }
    .period-afternoon { border-left-color: #38ef7d; background: linear-gradient(90deg, #a8ff78, white); }
    .period-evening { border-left-color: #ff416c; background: linear-gradient(90deg, #ff9a9e, white); }
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
            self.df['jam'] = self.df['order_purchase_timestamp'].dt.hour
            
            # Kategorikan waktu berdasarkan jam
            def categorize_time_period(hour):
                if 0 <= hour < 6:
                    return 'Dini Hari (00:00-06:00)'
                elif 6 <= hour < 12:
                    return 'Pagi (06:00-12:00)'
                elif 12 <= hour < 18:
                    return 'Siang (12:00-18:00)'
                else:
                    return 'Malam (18:00-24:00)'
            
            self.df['time_period'] = self.df['jam'].apply(categorize_time_period)
            
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
                time_period_options = sorted(self.df['time_period'].dropna().unique())
                selected_time_period = st.multiselect(
                    "**Pilih Periode Hari:**",
                    options=time_period_options,
                    default=time_period_options
                )
            
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
                # PERBAIKAN: Filter out review_score = 0 sebelum menghitung rata-rata
                valid_reviews = data[data['review_score'] > 0]
                avg_review = valid_reviews['review_score'].mean()
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
                # PERBAIKAN: Hitung jumlah review dengan score 0
                count_zero_review = (data['review_score'] == 0).sum()
                total_reviews_count = total_reviews
                self.create_mini_metric(f"{total_reviews_count:,}", f"Total Review ({count_zero_review} score 0)", "📝")
    
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
            # Hitung spending per customer_unique_id per state
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
        
        if score_type == 'review':
            # PERBAIKAN: Filter out review_score = 0 sebelum menghitung rata-rata
            valid_reviews = data[data['review_score'] > 0]
            state_data = valid_reviews.groupby(state_col).agg({
                'review_score': 'mean',
                'price': 'sum'
            }).round(3)
        else:
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
        """Membuat peta spending per customer_unique_id dengan ukuran lebih kecil"""
        # Aggregate data per state - revenue dan unique customer_unique_ids
        if 'customer_state_full' in data.columns:
            state_col = 'customer_state_full'
        else:
            state_col = 'nama_state'
        
        state_data = data.groupby(state_col).agg({
            'price': 'sum',
            'customer_unique_id': 'nunique'
        }).round(2)
        
        state_data.columns = ['total_revenue', 'unique_customer_unique_ids']
        
        # Hitung spending per customer_unique_id
        state_data['spending_per_customer_unique_id'] = (state_data['total_revenue'] / state_data['unique_customer_unique_ids']).round(2)
        state_data = state_data.reset_index()
        
        # Tambahkan koordinat
        state_data['lat'] = state_data[state_col].map(lambda x: self.brazil_states_coords.get(x, {}).get('lat', 0))
        state_data['lon'] = state_data[state_col].map(lambda x: self.brazil_states_coords.get(x, {}).get('lon', 0))
        state_data = state_data[state_data['lat'] != 0]
        
        # Format hover text
        hover_texts = []
        for idx, row in state_data.iterrows():
            text = f"{row[state_col]}<br>Spending/Customer: R$ {row['spending_per_customer_unique_id']:.2f}<br>Total Customers: {row['unique_customer_unique_ids']:,}<br>Total Revenue: R$ {row['total_revenue']:,.0f}"
            hover_texts.append(text)
        
        # Buat peta dengan ukuran lebih kecil (10cm x 10cm)
        fig = go.Figure()
        
        fig.add_trace(go.Scattergeo(
            lon = state_data['lon'],
            lat = state_data['lat'],
            text = hover_texts,
            hoverinfo = 'text',
            marker = dict(
                size = 15,  # Ukuran marker lebih kecil
                color = state_data['spending_per_customer_unique_id'],
                colorscale = 'Viridis',
                cmin = state_data['spending_per_customer_unique_id'].min(),
                cmax = state_data['spending_per_customer_unique_id'].max(),
                colorbar = dict(
                    title = "Spending/Customer (R$)",
                    thickness = 15,
                    len = 0.6
                ),
                line = dict(width=1, color='white'),
            )
        ))
        
        fig.update_layout(
            title = dict(
                text = "<b>Average Spending per Customer by State</b>",
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
                showocean = True,
                oceancolor = 'rgb(204, 229, 255)',
                center=dict(lat=-14, lon=-55),
                projection_scale=2.5,  # Zoom level lebih kecil
                lonaxis_range=[-75, -30],  # Batas longitude
                lataxis_range=[-35, 5],    # Batas latitude
            ),
            height = 400,  # Tinggi peta lebih kecil
            margin = dict(l=0, r=0, t=40, b=0)
        )
        
        return fig, state_data
    
    def create_time_period_revenue_analysis(self, data):
        """Membuat analisis revenue berdasarkan periode waktu - SATU PIE CHART"""
        st.markdown("### 🕒 REVENUE BERDASARKAN PERIODE WAKTU")
        
        # Hitung revenue per periode waktu
        time_period_data = data.groupby('time_period').agg({
            'price': ['sum', 'count'],
            'order_id': 'nunique',
            'customer_unique_id': 'nunique'
        }).round(2)
        
        time_period_data.columns = ['total_revenue', 'transaction_count', 'unique_orders', 'unique_customer_unique_ids']
        time_period_data = time_period_data.reset_index()
        
        # Hitung rata-rata revenue per order
        time_period_data['avg_revenue_per_order'] = (time_period_data['total_revenue'] / time_period_data['unique_orders']).round(2)
        
        # Urutkan berdasarkan urutan waktu yang logis
        time_order = ['Dini Hari (00:00-06:00)', 'Pagi (06:00-12:00)', 'Siang (12:00-18:00)', 'Malam (18:00-24:00)']
        time_period_data['time_period'] = pd.Categorical(time_period_data['time_period'], categories=time_order, ordered=True)
        time_period_data = time_period_data.sort_values('time_period')
        
        # SATU PIE CHART untuk distribusi revenue
        fig_pie_revenue = px.pie(
            time_period_data,
            values='total_revenue',
            names='time_period',
            color='time_period',
            color_discrete_map={
                'Dini Hari (00:00-06:00)': '#4e54c8',
                'Pagi (06:00-12:00)': '#ff9a00',
                'Siang (12:00-18:00)': '#38ef7d',
                'Malam (18:00-24:00)': '#ff416c'
            }
        )
        
        fig_pie_revenue.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Revenue: R$ %{value:,.0f}<br>Persentase: %{percent}",
            textfont=dict(size=12)
        )
        
        fig_pie_revenue.update_layout(
            height=400,
            showlegend=False,  # Sembunyikan legend karena sudah ada di pie chart
            margin=dict(t=50, b=50, l=20, r=20)
        )
        
        st.plotly_chart(fig_pie_revenue, use_container_width=True)
    
    def display_spending_segments(self, data):
        """Menampilkan segmentasi spending customer_unique_id dengan % distribusi"""
        # Hitung spending per customer_unique_id
        customer_unique_id_spending = data.groupby('customer_unique_id').agg({
            'price': 'sum'
        }).reset_index()
        
        total_customer_unique_ids = len(customer_unique_id_spending)
        
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
        customer_unique_id_spending['segment'] = customer_unique_id_spending['price'].apply(get_spending_segment)
        
        # Hitung statistik per segment
        segment_stats = customer_unique_id_spending.groupby('segment').agg({
            'customer_unique_id': 'count',
            'price': ['sum', 'mean', 'median']
        }).round(2)
        
        segment_stats.columns = ['customer_unique_id_count', 'total_spending', 'avg_spending', 'median_spending']
        segment_stats = segment_stats.reset_index()
        
        # Hitung persentase
        segment_stats['percentage'] = (segment_stats['customer_unique_id_count'] / total_customer_unique_ids * 100).round(1)
        
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
                        <div style="font-weight: bold; font-size: 1.2rem;">{row['customer_unique_id_count']:,}</div>
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
        """Menampilkan analisis repeat purchase berdasarkan segment - DIPERBAIKI"""
        # Hitung jumlah order per customer_unique_id
        customer_unique_id_orders = data.groupby('customer_unique_id').agg({
            'order_id': 'nunique',
            'price': 'sum'
        }).reset_index()
        
        customer_unique_id_orders.columns = ['customer_unique_id', 'order_count', 'total_spending']
        
        total_customer_unique_ids = len(customer_unique_id_orders)
        
        # Definisikan segment repeat purchase - DIPERBAIKI dengan penjelasan
        def get_repeat_segment(order_count):
            if order_count == 1:
                return 'One-time Buyer'
            elif order_count <= 3:
                return 'Occasional Buyer (2-3 orders)'
            elif order_count <= 10:
                return 'Regular Buyer (4-10 orders)'
            else:
                return 'Frequent Buyer (>10 orders)'
        
        # Terapkan segmentasi repeat purchase
        customer_unique_id_orders['repeat_segment'] = customer_unique_id_orders['order_count'].apply(get_repeat_segment)
        
        # Hitung statistik per segment repeat
        repeat_stats = customer_unique_id_orders.groupby('repeat_segment').agg({
            'customer_unique_id': 'count',
            'order_count': ['mean', 'sum'],  # DITAMBAH: total semua orders
            'total_spending': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        repeat_stats.columns = [
            'customer_unique_id_count', 
            'avg_orders_per_customer_unique_id', 
            'total_orders',
            'total_spending', 
            'avg_spending_per_customer_unique_id'
        ]
        repeat_stats = repeat_stats.reset_index()
        
        # Hitung persentase customer_unique_id dan spending
        repeat_stats['customer_unique_id_percentage'] = (repeat_stats['customer_unique_id_count'] / total_customer_unique_ids * 100).round(1)
        repeat_stats['spending_percentage'] = (repeat_stats['total_spending'] / customer_unique_id_orders['total_spending'].sum() * 100).round(1)
        
        # Hitung nilai lifetime customer_unique_id
        repeat_stats['avg_lifetime_value'] = (repeat_stats['total_spending'] / repeat_stats['customer_unique_id_count']).round(2)
        
        # Urutkan berdasarkan order count (bukan alphabet)
        repeat_order = [
            'One-time Buyer', 
            'Occasional Buyer (2-3 orders)', 
            'Regular Buyer (4-10 orders)', 
            'Frequent Buyer (>10 orders)'
        ]
        repeat_stats['repeat_segment'] = pd.Categorical(
            repeat_stats['repeat_segment'], 
            categories=repeat_order, 
            ordered=True
        )
        repeat_stats = repeat_stats.sort_values('repeat_segment')
        
        # Tampilkan repeat purchase segments - DIPERBAIKI dengan metrik tambahan
        st.markdown("### 🔄 REPEAT PURCHASE SEGMENTS")
        
        # Tampilkan summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            repeat_rate = ((total_customer_unique_ids - repeat_stats.iloc[0]['customer_unique_id_count']) / total_customer_unique_ids * 100).round(1)
            self.create_mini_metric(f"{repeat_rate}%", "Customer Repeat Rate", "🔄")
        
        with col2:
            avg_orders = customer_unique_id_orders['order_count'].mean().round(2)
            self.create_mini_metric(f"{avg_orders}", "Rata-rata Orders/Customer", "📊")
        
        with col3:
            loyal_customer_unique_ids = repeat_stats[repeat_stats['repeat_segment'].isin(['Regular Buyer (4-10 orders)', 'Frequent Buyer (>10 orders)'])]['customer_unique_id_count'].sum()
            loyal_percentage = (loyal_customer_unique_ids / total_customer_unique_ids * 100).round(1)
            self.create_mini_metric(f"{loyal_percentage}%", "Loyal Customers", "⭐")
        
        with col4:
            total_repeat_orders = repeat_stats['total_orders'].sum() - repeat_stats.iloc[0]['total_orders']
            self.create_mini_metric(f"{total_repeat_orders:,}", "Total Repeat Orders", "📦")
        
        # Tampilkan segment cards dengan metrik yang lebih lengkap
        for idx, row in repeat_stats.iterrows():
            st.markdown(f"""
            <div class="repeat-card">
                <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">
                    {row['repeat_segment']} 
                    <span style="font-size: 0.9rem; color: #6c757d;">
                        ({row['customer_unique_id_percentage']}% customers, {row['spending_percentage']}% revenue)
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem;">
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Customers</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">{row['customer_unique_id_count']:,}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Total Orders</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">{row['total_orders']:,}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">Total Spending</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">R$ {row['total_spending']:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; color: #6c757d;">LTV/Customer</div>
                        <div style="font-weight: bold; font-size: 1.2rem;">R$ {row['avg_lifetime_value']:,.0f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tambahkan insights
        st.markdown("#### 💡 INSIGHTS REPEAT PURCHASE:")
        
        # Hitung beberapa metrics insight
        one_time_customer_unique_ids = repeat_stats.iloc[0]['customer_unique_id_count']
        repeat_customer_unique_ids = total_customer_unique_ids - one_time_customer_unique_ids
        revenue_from_repeaters = repeat_stats['total_spending'].sum() - repeat_stats.iloc[0]['total_spending']
        
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.info(f"**🔄 Customer Retention:** {repeat_customer_unique_ids:,} dari {total_customer_unique_ids:,} customers ({repeat_rate}%) melakukan repeat purchase")
            
        with col_insight2:
            st.info(f"**💰 Revenue Impact:** Repeat customers menyumbang R$ {revenue_from_repeaters:,.0f} ({repeat_stats['spending_percentage'].sum() - repeat_stats.iloc[0]['spending_percentage']:.1f}%) dari total revenue")
    
    def display_state_ranking_vertical(self, data, score_type='review'):
        """Menampilkan ranking state secara vertikal"""
        # Aggregate data per state
        if 'customer_state_full' in data.columns:
            state_col = 'customer_state_full'
        else:
            state_col = 'nama_state'
        
        if score_type == 'review':
            # PERBAIKAN: Filter out review_score = 0 sebelum menghitung rata-rata
            valid_reviews = data[data['review_score'] > 0]
            state_scores = valid_reviews.groupby(state_col)['review_score'].mean().round(3).reset_index()
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
            # PERBAIKAN: Filter out review_score = 0 sebelum menghitung rata-rata
            valid_reviews = data[data['review_score'] > 0]
            category_review = valid_reviews.groupby('product_category_name_english')['review_score'].mean().round(3).reset_index()
            category_review = category_review[category_review['review_score'].notna()]
            category_review = category_review[category_review['product_category_name_english'].notna()]
            
            # 🚨 FILTER MINIMUM ORDER DIHAPUS - semua kategori akan ditampilkan
            
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
            
            # 🚨 FILTER MINIMUM ORDER DIHAPUS - semua kategori akan ditampilkan
            
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
    
    def create_simple_trendline(self, x, y):
        """Membuat trendline sederhana menggunakan linear regression"""
        try:
            # Linear regression sederhana
            coeffs = np.polyfit(x, y, 1)
            trendline = np.poly1d(coeffs)
            return trendline(x)
        except:
            # Fallback jika error
            return y
    
    def create_review_revenue_correlation_analysis(self, data):
        """Membuat analisis korelasi antara review score dan revenue"""
        if 'product_category_name_english' not in data.columns:
            st.warning("Data kategori produk tidak tersedia untuk analisis korelasi")
            return
        
        st.markdown("### 📈 KORELASI REVIEW SCORE DAN REVENUE")
        
        # PERBAIKAN: Filter out review_score = 0 hanya untuk perhitungan review score, tapi revenue tetap semua data
        valid_reviews = data[data['review_score'] > 0]
        
        # PERBAIKAN: Filter kategori dengan minimal 10 order - gunakan data lengkap untuk revenue
        category_order_counts = data.groupby('product_category_name_english')['order_id'].nunique()  # Gunakan data lengkap
        categories_with_min_orders = category_order_counts[category_order_counts >= 10].index.tolist()
        
        # Filter data untuk review (hanya yang valid) dan revenue (semua data)
        # Untuk review: gunakan valid_reviews
        # Untuk revenue: gabungkan data review valid dengan data revenue lengkap
        review_data = valid_reviews[valid_reviews['product_category_name_english'].isin(categories_with_min_orders)]
        revenue_data = data[data['product_category_name_english'].isin(categories_with_min_orders)]
        
        # Aggregate data per kategori produk - review dari data valid, revenue dari semua data
        category_review = review_data.groupby('product_category_name_english')['review_score'].mean().round(3).reset_index()
        category_revenue = revenue_data.groupby('product_category_name_english')['price'].sum().round(0).reset_index()
        
        # Gabungkan data review dan revenue
        category_data = pd.merge(category_review, category_revenue, on='product_category_name_english', how='inner')
        category_data.columns = ['category', 'avg_review', 'total_revenue']
        
        # Tambahkan order count dari data lengkap
        order_counts = revenue_data.groupby('product_category_name_english')['order_id'].nunique().reset_index()
        order_counts.columns = ['category', 'order_count']
        category_data = pd.merge(category_data, order_counts, on='category', how='inner')
        
        if len(category_data) == 0:
            st.warning("Tidak ada kategori dengan minimal 10 order untuk analisis korelasi")
            return
        
        # Hitung korelasi
        correlation = category_data['avg_review'].corr(category_data['total_revenue'])
        
        # Tampilkan metrik korelasi
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if correlation > 0.7:
                correlation_class = "correlation-high"
                interpretation = "Korelasi Positif Kuat"
            elif correlation > 0.3:
                correlation_class = "correlation-medium" 
                interpretation = "Korelasi Positif Sedang"
            elif correlation > 0:
                correlation_class = "correlation-low"
                interpretation = "Korelasi Lemah"
            else:
                correlation_class = "correlation-low"
                interpretation = "Korelasi Negatif"
                
            st.markdown(f"""
            <div class="mini-metric">
                <div class="metric-value {correlation_class}">{correlation:.3f}</div>
                <div class="metric-label">{interpretation}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Jumlah Kategori Dianalisis", len(category_data))
        
        with col3:
            avg_review_all = category_data['avg_review'].mean()
            st.metric("Rata-rata Review Semua Kategori", f"{avg_review_all:.2f}")
            
        with col4:
            # Tampilkan informasi tentang filter minimal order
            total_categories = data['product_category_name_english'].nunique()  # Gunakan data lengkap
            excluded_categories = total_categories - len(category_data)
            st.metric(
                "Kategori Dikecualikan", 
                f"{excluded_categories}",
                help="Kategori dengan kurang dari 10 order dikecualikan dari analisis"
            )
        
        # Informasi tentang filter
        st.info(f"📊 **Analisis ini hanya mencakup kategori dengan minimal 10 order.** Dari {total_categories} kategori total, {len(category_data)} kategori memenuhi kriteria ini.")
        st.info("💰 **Revenue mencakup semua transaksi**, termasuk yang memiliki review score = 0.")
        
        # SCATTER PLOT 1: Semua Produk
        st.markdown("#### 🔍 SCATTER PLOT: SEMUA KATEGORI PRODUK (Min. 10 Order)")
        
        # Buat scatter plot tanpa trendline LOWESS
        fig_all = px.scatter(
            category_data, 
            x='avg_review', 
            y='total_revenue',
            size='order_count',
            hover_name='category',
            hover_data={
                'avg_review': ':.2f',
                'total_revenue': ':,.0f',
                'order_count': True
            },
            title='Korelasi Review Score vs Revenue - Semua Kategori (Min. 10 Order)',
            labels={
                'avg_review': 'Rata-rata Review Score',
                'total_revenue': 'Total Revenue (R$)',
                'order_count': 'Jumlah Order'
            }
        )
        
        # Tambahkan trendline sederhana menggunakan linear regression
        try:
            x_vals = category_data['avg_review'].values
            y_vals = category_data['total_revenue'].values
            
            # Urutkan berdasarkan x untuk trendline yang rapi
            sort_idx = np.argsort(x_vals)
            x_sorted = x_vals[sort_idx]
            y_sorted = y_vals[sort_idx]
            
            # Buat trendline
            trendline_vals = self.create_simple_trendline(x_sorted, y_sorted)
            
            fig_all.add_trace(
                go.Scatter(
                    x=x_sorted,
                    y=trendline_vals,
                    mode='lines',
                    name='Trendline',
                    line=dict(color='red', dash='dash'),
                    hoverinfo='skip'
                )
            )
        except Exception as e:
            st.warning(f"Tidak dapat menambahkan trendline: {str(e)}")
        
        fig_all.update_layout(
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig_all, use_container_width=True)
        
        # SCATTER PLOT 2: Top 5 Review dan Revenue
        st.markdown("#### 🏆 SCATTER PLOT: TOP 5 KATEGORI REVIEW & REVENUE (Min. 10 Order)")
        
        # Ambil top 5 dari masing-masing kategori
        top_5_review_cats = category_data.nlargest(5, 'avg_review')['category'].tolist()
        top_5_revenue_cats = category_data.nlargest(5, 'total_revenue')['category'].tolist()
        
        # Gabungkan dan hapus duplikat
        top_cats = list(set(top_5_review_cats + top_5_revenue_cats))
        top_categories_data = category_data[category_data['category'].isin(top_cats)]
        
        # Buat scatter plot untuk top categories
        fig_top = px.scatter(
            top_categories_data, 
            x='avg_review', 
            y='total_revenue',
            size='order_count',
            hover_name='category',
            hover_data={
                'avg_review': ':.2f',
                'total_revenue': ':,.0f',
                'order_count': True
            },
            title='Korelasi Review Score vs Revenue - Top Kategori (Min. 10 Order)',
            labels={
                'avg_review': 'Rata-rata Review Score',
                'total_revenue': 'Total Revenue (R$)',
                'order_count': 'Jumlah Order'
            },
            color='category'  # Warna berbeda untuk setiap kategori
        )
        
        fig_top.update_layout(
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig_top, use_container_width=True)
    
    def create_review_revenue_insights(self, data):
        """Membuat insights terpisah untuk PERFORMER TERBAIK dan PELUANG BISNIS"""
        if 'product_category_name_english' not in data.columns:
            st.warning("Data kategori produk tidak tersedia untuk analisis insights")
            return
        
        st.markdown("### 💡 INSIGHTS REVIEW DAN REVENUE")
        
        # PERBAIKAN: Filter out review_score = 0 hanya untuk perhitungan review score, tapi revenue tetap semua data
        valid_reviews = data[data['review_score'] > 0]
        
        # Filter kategori dengan minimal 10 order - gunakan data lengkap untuk revenue
        category_order_counts = data.groupby('product_category_name_english')['order_id'].nunique()  # Gunakan data lengkap
        categories_with_min_orders = category_order_counts[category_order_counts >= 10].index.tolist()
        
        # Filter data untuk review (hanya yang valid) dan revenue (semua data)
        review_data = valid_reviews[valid_reviews['product_category_name_english'].isin(categories_with_min_orders)]
        revenue_data = data[data['product_category_name_english'].isin(categories_with_min_orders)]
        
        # Aggregate data per kategori produk - review dari data valid, revenue dari semua data
        category_review = review_data.groupby('product_category_name_english')['review_score'].mean().round(3).reset_index()
        category_revenue = revenue_data.groupby('product_category_name_english')['price'].sum().round(0).reset_index()
        
        # Gabungkan data review dan revenue
        category_data = pd.merge(category_review, category_revenue, on='product_category_name_english', how='inner')
        category_data.columns = ['category', 'avg_review', 'total_revenue']
        
        # Tambahkan order count dari data lengkap
        order_counts = revenue_data.groupby('product_category_name_english')['order_id'].nunique().reset_index()
        order_counts.columns = ['category', 'order_count']
        category_data = pd.merge(category_data, order_counts, on='category', how='inner')
        
        if len(category_data) == 0:
            st.warning("Tidak ada kategori dengan minimal 10 order untuk analisis insights")
            return
        
        # Informasi tentang data yang digunakan
        st.info("📊 **Analisis ini hanya mencakup kategori dengan minimal 10 order.**")
        st.info("⭐ **Review Score**: Hanya menghitung review dengan score > 0")
        st.info("💰 **Revenue**: Mencakup semua transaksi, termasuk yang memiliki review score = 0")
        
        # Cari produk dengan performa terbaik (review tinggi & revenue tinggi)
        best_performers = category_data[
            (category_data['avg_review'] >= category_data['avg_review'].quantile(0.75)) &
            (category_data['total_revenue'] >= category_data['total_revenue'].quantile(0.75))
        ]
        
        # Cari produk dengan review tinggi tapi revenue rendah (opportunity)
        high_review_low_revenue = category_data[
            (category_data['avg_review'] >= category_data['avg_review'].quantile(0.75)) &
            (category_data['total_revenue'] <= category_data['total_revenue'].quantile(0.25))
        ]
        
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.markdown("#### ✅ PERFORMER TERBAIK")
            st.markdown("Kategori dengan **review tinggi** dan **revenue tinggi**:")
            if len(best_performers) > 0:
                for _, product in best_performers.head(5).iterrows():
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, #d4edda, white); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #28a745;">
                        <div style="font-weight: bold; font-size: 1.1rem; color: #155724;">{product['category']}</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem;">
                            <div>
                                <div style="font-size: 0.8rem; color: #6c757d;">Review Score</div>
                                <div style="font-weight: bold; color: #28a745;">⭐ {product['avg_review']:.2f}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.8rem; color: #6c757d;">Revenue</div>
                                <div style="font-weight: bold; color: #007bff;">💰 R$ {product['total_revenue']:,.0f}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.8rem; color: #6c757d;">Orders</div>
                                <div style="font-weight: bold; color: #6c757d;">📦 {product['order_count']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("*Tidak ada kategori yang masuk kriteria*")
        
        with col_insight2:
            st.markdown("#### 🎯 PELUANG BISNIS")
            st.markdown("Kategori dengan **review tinggi** tapi **revenue rendah**:")
            if len(high_review_low_revenue) > 0:
                for _, product in high_review_low_revenue.head(5).iterrows():
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, #fff3cd, white); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #ffc107;">
                        <div style="font-weight: bold; font-size: 1.1rem; color: #856404;">{product['category']}</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem;">
                            <div>
                                <div style="font-size: 0.8rem; color: #6c757d;">Review Score</div>
                                <div style="font-weight: bold; color: #28a745;">⭐ {product['avg_review']:.2f}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.8rem; color: #6c757d;">Revenue</div>
                                <div style="font-weight: bold; color: #dc3545;">💰 R$ {product['total_revenue']:,.0f}</div>
                            </div>
                            <div>
                                <div style="font-size: 0.8rem; color: #6c757d;">Orders</div>
                                <div style="font-weight: bold; color: #6c757d;">📦 {product['order_count']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("*Tidak ada kategori yang masuk kriteria*")
    
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
            
            # Tab untuk product analysis
            subtab1, subtab2, subtab3 = st.tabs(["🏆 PRODUCT RANKINGS", "📈 REVIEW-REVENUE CORRELATION", "💡 INSIGHTS REVIEW-REVENUE"])
            
            with subtab1:
                self.display_product_rankings(filtered_data)
            
            with subtab2:
                self.create_review_revenue_correlation_analysis(filtered_data)
            
            with subtab3:
                self.create_review_revenue_insights(filtered_data)
        
        with tab4:
            # Metrics untuk customer spending
            self.display_customer_spending_metrics(filtered_data)
            
            st.markdown("---")
            
            # Layout untuk customer analysis - BERDAMPINGAN
            col_map, col_time = st.columns([2, 1])
            
            with col_map:
                st.markdown("**🗺️ PETA SPENDING PER CUSTOMER - BRAZIL**")
                fig, state_data = self.create_customer_spending_map(filtered_data)
                st.plotly_chart(fig, use_container_width=True)
            
            with col_time:
                # Tambahkan analisis revenue berdasarkan waktu di sini
                self.create_time_period_revenue_analysis(filtered_data)
            
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

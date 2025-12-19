"""
=================================================================
PHASE 6: STREAMLIT DASHBOARD - E-COMMERCE ANALYTICS
=================================================================
Interactive dashboard with filters and comprehensive KPIs
=================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# Get the project root directory (parent of dashboard folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== TITLE & DESCRIPTION ========================
st.markdown("""
    <style>
    .main-title { font-size: 40px; font-weight: bold; color: #1f77b4; }
    .subtitle { font-size: 16px; color: #666; }
    </style>
    <div class='main-title'>📊 E-Commerce Sales & Customer Analytics Dashboard</div>
    <div class='subtitle'>Real-time insights on revenue, customers, and business performance</div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ======================== LOAD DATA ========================
@st.cache_data
def load_data():
    data_path = os.path.join(PROJECT_ROOT, "data", "processed", "superstore_cleaned.csv")
    df = pd.read_csv(data_path, encoding='latin-1')
    # Convert date columns
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col])
    return df

@st.cache_data
def load_kpis():
    kpi_path = os.path.join(PROJECT_ROOT, "data", "processed", "kpis.csv")
    kpis_df = pd.read_csv(kpi_path)
    # Convert to dictionary: {'KPI Name': 'Value'}
    return dict(zip(kpis_df['KPI'], kpis_df['Value']))

try:
    df = load_data()
    kpis = load_kpis()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# ======================== SIDEBAR FILTERS ========================
st.sidebar.markdown("### 🎯 FILTERS")
st.sidebar.markdown("---")

# Date range filter
date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    value=(df['Order Date'].min().date(), df['Order Date'].max().date()),
    min_value=df['Order Date'].min().date(),
    max_value=df['Order Date'].max().date()
)

if len(date_range) == 2:
    df_filtered = df[(df['Order Date'].dt.date >= date_range[0]) & 
                     (df['Order Date'].dt.date <= date_range[1])]
else:
    df_filtered = df.copy()

# Region filter
regions = df_filtered['Region'].unique() if 'Region' in df_filtered.columns else []
selected_regions = st.sidebar.multiselect(
    "🌍 Select Regions",
    options=sorted(regions),
    default=sorted(regions)
)
df_filtered = df_filtered[df_filtered['Region'].isin(selected_regions)]

# Category filter
categories = df_filtered['Category'].unique() if 'Category' in df_filtered.columns else []
selected_categories = st.sidebar.multiselect(
    "📦 Select Categories",
    options=sorted(categories),
    default=sorted(categories)
)
df_filtered = df_filtered[df_filtered['Category'].isin(selected_categories)]

# Customer type filter
if 'customer_type' in df_filtered.columns:
    customer_types = df_filtered['customer_type'].unique()
    selected_cust_types = st.sidebar.multiselect(
        "👥 Select Customer Types",
        options=sorted(customer_types),
        default=sorted(customer_types)
    )
    df_filtered = df_filtered[df_filtered['customer_type'].isin(selected_cust_types)]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 Filtered Data:** {len(df_filtered):,} orders")

# ======================== TAB LAYOUT ========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview KPIs",
    "💹 Sales Trends",
    "👥 Customer Insights",
    "🌍 Regional Analysis",
    "🏷️ Discount Impact"
])

# ======================== TAB 1: OVERVIEW KPIs ========================
with tab1:
    st.markdown("### 🎯 KEY PERFORMANCE INDICATORS")
    
    # Calculate KPIs for filtered data
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = df_filtered['Sales'].sum()
    total_profit = df_filtered['Profit'].sum()
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    aov = df_filtered['Sales'].mean()
    
    col1.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.0f}",
        delta="Current period"
    )
    col2.metric(
        "📊 Total Profit",
        f"${total_profit:,.0f}",
        delta=f"{profit_margin:.2f}% margin"
    )
    col3.metric(
        "💵 Average Order Value",
        f"${aov:.2f}",
        delta="Per transaction"
    )
    col4.metric(
        "📦 Total Orders",
        f"{df_filtered['Order ID'].nunique():,}",
        delta="Unique transactions"
    )
    
    col5, col6, col7, col8 = st.columns(4)
    
    unique_customers = df_filtered['Customer ID'].nunique()
    revenue_per_customer = total_revenue / unique_customers if unique_customers > 0 else 0
    repeat_rate = (df_filtered[df_filtered['customer_type'] == 'Returning']['Customer ID'].nunique() / unique_customers * 100) if 'customer_type' in df_filtered.columns and unique_customers > 0 else 0
    avg_profit_per_order = total_profit / df_filtered['Order ID'].nunique() if df_filtered['Order ID'].nunique() > 0 else 0
    
    col5.metric(
        "👥 Unique Customers",
        f"{unique_customers:,}",
        delta="Total customers"
    )
    col6.metric(
        "💎 Revenue Per Customer",
        f"${revenue_per_customer:.2f}",
        delta="Lifetime value"
    )
    col7.metric(
        "🔁 Repeat Customer Rate",
        f"{repeat_rate:.1f}%",
        delta="Retention indicator"
    )
    col8.metric(
        "💰 Profit Per Order",
        f"${avg_profit_per_order:.2f}",
        delta="Average profitability"
    )
    
    st.markdown("---")
    
    # Category & Region distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📦 Revenue by Category")
        if 'Category' in df_filtered.columns:
            category_data = df_filtered.groupby('Category')['Sales'].sum().sort_values(ascending=False)
            fig = px.pie(
                values=category_data.values,
                names=category_data.index,
                hole=0.3,
                title="Category Revenue Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🌍 Revenue by Region")
        if 'Region' in df_filtered.columns:
            region_data = df_filtered.groupby('Region')['Sales'].sum().sort_values(ascending=False)
            fig = px.pie(
                values=region_data.values,
                names=region_data.index,
                hole=0.3,
                title="Region Revenue Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

# ======================== TAB 2: SALES TRENDS ========================
with tab2:
    st.markdown("### 💹 SALES & REVENUE TRENDS")
    
    # Monthly trend
    monthly_data = df_filtered.groupby(df_filtered['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count'
    }).reset_index()
    monthly_data['Order Date'] = monthly_data['Order Date'].astype(str)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Monthly Revenue Trend")
        fig = px.line(
            monthly_data,
            x='Order Date',
            y='Sales',
            markers=True,
            title="Monthly Revenue",
            labels={'Sales': 'Revenue ($)', 'Order Date': 'Month'}
        )
        fig.add_trace(go.Scatter(
            x=monthly_data['Order Date'],
            y=monthly_data['Profit'],
            name='Profit',
            yaxis='y2',
            line=dict(color='red')
        ))
        fig.update_layout(
            yaxis2=dict(title='Profit ($)', overlaying='y', side='right'),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📦 Monthly Order Volume")
        fig = px.bar(
            monthly_data,
            x='Order Date',
            y='Order ID',
            title="Monthly Orders",
            labels={'Order ID': 'Number of Orders', 'Order Date': 'Month'},
            color='Order ID',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top products
    st.markdown("---")
    st.markdown("#### 🔥 TOP 10 PRODUCTS BY REVENUE")
    if 'Product Name' in df_filtered.columns:
        top_products = df_filtered.groupby('Product Name').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count'
        }).sort_values('Sales', ascending=False).head(10)
        top_products.columns = ['Revenue', 'Profit', 'Orders']
        top_products['Profit Margin %'] = (top_products['Profit'] / top_products['Revenue'] * 100).round(2)
        
        fig = px.bar(
            top_products.reset_index(),
            x='Revenue',
            y='Product Name',
            orientation='h',
            color='Profit',
            color_continuous_scale='RdYlGn',
            title="Top 10 Products",
            labels={'Revenue': 'Revenue ($)', 'Profit': 'Profit ($)'}
        )
        fig.update_yaxes(automargin=True)
        st.plotly_chart(fig, use_container_width=True)

# ======================== TAB 3: CUSTOMER INSIGHTS ========================
with tab3:
    st.markdown("### 👥 CUSTOMER INSIGHTS & SEGMENTATION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🆕 New vs Repeat Customers")
        if 'customer_type' in df_filtered.columns:
            cust_type_data = df_filtered.groupby('customer_type').agg({
                'Customer ID': 'nunique',
                'Sales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            cust_type_data.columns = ['Type', 'Customers', 'Revenue', 'Profit']
            
            fig = px.bar(
                cust_type_data,
                x='Type',
                y=['Revenue', 'Profit'],
                barmode='group',
                title="Revenue by Customer Type",
                labels={'value': 'Amount ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 💎 PARETO ANALYSIS")
        customer_value = df_filtered.groupby('Customer ID')['Sales'].sum().sort_values(ascending=False)
        total_revenue = customer_value.sum()
        cumsum_pct = (customer_value.cumsum() / total_revenue * 100).values[:100]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=cumsum_pct,
            mode='lines+markers',
            name='Cumulative Revenue %',
            fill='tozeroy'
        ))
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Rule")
        fig.update_layout(
            title="Pareto Curve: Customer Contribution",
            xaxis_title="Top N Customers",
            yaxis_title="Cumulative Revenue %",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer churn
    st.markdown("---")
    st.markdown("#### ⚠️ CHURN RISK ANALYSIS")
    if 'Order Date' in df_filtered.columns:
        today = df_filtered['Order Date'].max()
        customer_activity = df_filtered.groupby('Customer ID')['Order Date'].max().reset_index()
        customer_activity.columns = ['Customer_ID', 'Last_Order']
        customer_activity['Days_Since_Last_Order'] = (today - customer_activity['Last_Order']).dt.days
        
        median_days = customer_activity['Days_Since_Last_Order'].median()
        at_risk = (customer_activity['Days_Since_Last_Order'] > median_days).sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("⏱️ Median Days Since Order", f"{median_days:.0f} days")
        col2.metric("🔴 At-Risk Customers", f"{at_risk:,}")
        col3.metric("% At Risk", f"{(at_risk/len(customer_activity)*100):.1f}%")
        
        fig = px.histogram(
            customer_activity,
            x='Days_Since_Last_Order',
            nbins=30,
            title="Distribution: Days Since Last Order",
            labels={'Days_Since_Last_Order': 'Days'}
        )
        fig.add_vline(x=median_days, line_dash="dash", line_color="red", annotation_text=f"Median: {median_days:.0f}")
        st.plotly_chart(fig, use_container_width=True)

# ======================== TAB 4: REGIONAL ANALYSIS ========================
with tab4:
    st.markdown("### 🌍 REGIONAL PERFORMANCE ANALYSIS")
    
    if 'Region' in df_filtered.columns:
        region_data = df_filtered.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'count',
            'Customer ID': 'nunique'
        }).reset_index()
        region_data.columns = ['Region', 'Revenue', 'Profit', 'Orders', 'Customers']
        region_data['Profit_Margin_%'] = (region_data['Profit'] / region_data['Revenue'] * 100).round(2)
        region_data['Avg_Order_Value'] = (region_data['Revenue'] / region_data['Orders']).round(2)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📊 Revenue by Region")
            fig = px.bar(
                region_data.sort_values('Revenue', ascending=False),
                x='Region',
                y='Revenue',
                color='Revenue',
                color_continuous_scale='Blues',
                title="Regional Revenue"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 💰 Profit by Region")
            fig = px.bar(
                region_data.sort_values('Profit', ascending=False),
                x='Region',
                y='Profit',
                color='Profit',
                color_continuous_scale='RdYlGn',
                title="Regional Profit"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("#### 📈 Profit Margin by Region")
            fig = px.bar(
                region_data.sort_values('Profit_Margin_%', ascending=False),
                x='Region',
                y='Profit_Margin_%',
                color='Profit_Margin_%',
                color_continuous_scale='RdYlGn',
                title="Regional Profit Margin"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Regional comparison table
        st.markdown("---")
        st.markdown("#### 📋 REGIONAL METRICS TABLE")
        st.dataframe(
            region_data.sort_values('Revenue', ascending=False).style.format({
                'Revenue': '${:,.0f}',
                'Profit': '${:,.0f}',
                'Profit_Margin_%': '{:.2f}%',
                'Avg_Order_Value': '${:,.2f}'
            }),
            use_container_width=True
        )

# ======================== TAB 5: DISCOUNT IMPACT ========================
with tab5:
    st.markdown("### 🏷️ DISCOUNT IMPACT ANALYSIS")
    
    if 'Discount' in df_filtered.columns:
        # Discount segments
        discount_segments = []
        for bin_label, bin_range in [
            ('No Discount (0%)', (0, 0)),
            ('Low (1-10%)', (0.01, 0.10)),
            ('Medium (11-20%)', (0.11, 0.20)),
            ('High (20%+)', (0.20, 1.0))
        ]:
            seg_data = df_filtered[
                (df_filtered['Discount'] >= bin_range[0]) &
                (df_filtered['Discount'] <= bin_range[1])
            ]
            if len(seg_data) > 0:
                discount_segments.append({
                    'Discount Level': bin_label,
                    'Orders': len(seg_data),
                    'Revenue': seg_data['Sales'].sum(),
                    'Profit': seg_data['Profit'].sum(),
                    'Avg Order Value': seg_data['Sales'].mean(),
                    'Profit Margin %': (seg_data['Profit'].sum() / seg_data['Sales'].sum() * 100)
                })
        
        discount_df = pd.DataFrame(discount_segments)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Profit Margin by Discount Level")
            fig = px.bar(
                discount_df,
                x='Discount Level',
                y='Profit Margin %',
                color='Profit Margin %',
                color_continuous_scale='RdYlGn',
                title="Does Discount Hurt Profit?"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📦 Order Volume by Discount Level")
            fig = px.bar(
                discount_df,
                x='Discount Level',
                y='Orders',
                color='Orders',
                color_continuous_scale='Blues',
                title="Volume Impact of Discounts"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Revenue vs Profit
        st.markdown("---")
        st.markdown("#### 💰 REVENUE vs PROFIT by Discount Level")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=discount_df['Discount Level'],
            y=discount_df['Revenue'],
            name='Revenue',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            x=discount_df['Discount Level'],
            y=discount_df['Profit'],
            name='Profit',
            marker_color='lightgreen'
        ))
        fig.update_layout(barmode='group', title="Revenue vs Profit by Discount")
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.markdown("---")
        st.markdown("#### 📋 DETAILED DISCOUNT ANALYSIS")
        st.dataframe(
            discount_df.style.format({
                'Revenue': '${:,.0f}',
                'Profit': '${:,.0f}',
                'Avg Order Value': '${:,.2f}',
                'Profit Margin %': '{:.2f}%'
            }),
            use_container_width=True
        )

# ======================== FOOTER ========================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
    📊 E-Commerce Analytics Dashboard | Last Updated: {}
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

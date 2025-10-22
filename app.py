import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Configuration de la page
st.set_page_config(
    page_title="Optimisation+ | Plateforme BI Restaurant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Palette de couleurs Optimisation+ (basée sur la charte graphique)
COLORS = {
    'primary': '#DD6D6D',      # Rose coral (couleur principale)
    'secondary': '#3A1B50',    # Violet foncé (couleur secondaire)
    'accent': '#FF8A8A',       # Rose clair (accent)
    'success': '#10b981',      # Vert (succès)
    'warning': '#f59e0b',      # Orange (alerte)
    'danger': '#ef4444',       # Rouge (danger)
    'dark': '#1e293b',         # Gris foncé (texte)
    'light': '#f8fafc',        # Gris clair (fond)
    'text': '#334155'          # Texte principal
}

# CSS personnalisé professionnel
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .main-header {{
        font-size: 2.25rem;
        font-weight: 700;
        color: {COLORS['dark']};
        margin-bottom: 0.25rem;
        letter-spacing: -0.025em;
    }}
    
    .sub-header {{
        font-size: 1rem;
        color: {COLORS['text']};
        margin-bottom: 2rem;
        font-weight: 400;
    }}
    
    .insight-box {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
        margin: 1rem 0;
    }}
    
    .insight-box h4 {{
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }}
    
    .warning-box {{
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid {COLORS['warning']};
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    
    .success-box {{
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid {COLORS['success']};
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background-color: {COLORS['light']};
        padding: 0.5rem;
        border-radius: 12px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.75rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        border-radius: 8px;
        color: {COLORS['text']};
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: white;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        color: {COLORS['primary']} !important;
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['dark']};
    }}
    
    .alert-info {{
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid {COLORS['primary']};
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .alert-warning {{
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid {COLORS['warning']};
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .alert-success {{
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid {COLORS['success']};
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 1.75rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Génération de données fictives réalistes
@st.cache_data
def generate_data():
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    sales_data = []
    for date in dates:
        day_of_week = date.dayofweek
        is_weekend = day_of_week >= 5
        
        base_revenue = 2500 if is_weekend else 1800
        revenue = base_revenue + np.random.normal(0, 300)
        covers = int(revenue / 52 + np.random.normal(0, 5))
        
        sales_data.append({
            'date': date,
            'revenue': max(0, revenue),
            'covers': max(0, covers),
            'avg_ticket': revenue / covers if covers > 0 else 0,
            'day_of_week': date.strftime('%A')
        })
    
    df_sales = pd.DataFrame(sales_data)
    
    hours = list(range(11, 23))
    hourly_data = []
    for hour in hours:
        if 12 <= hour <= 14:
            covers = np.random.randint(35, 55)
        elif 18 <= hour <= 21:
            covers = np.random.randint(50, 75)
        else:
            covers = np.random.randint(10, 25)
        
        hourly_data.append({
            'hour': f"{hour}h-{hour+1}h",
            'covers': covers,
            'revenue': covers * (50 + np.random.randint(-10, 20))
        })
    
    df_hourly = pd.DataFrame(hourly_data)
    
    menu_items = [
        {'name': 'Pâtes Carbonara', 'qty': 890, 'revenue': 17800, 'cost': 28, 'margin': 72},
        {'name': 'Steak-Frites', 'qty': 760, 'revenue': 22800, 'cost': 45, 'margin': 55},
        {'name': 'Burger Signature', 'qty': 680, 'revenue': 13600, 'cost': 32, 'margin': 68},
        {'name': 'Saumon Atlantique', 'qty': 540, 'revenue': 18900, 'cost': 48, 'margin': 52},
        {'name': 'Pizza Margherita', 'qty': 470, 'revenue': 8460, 'cost': 25, 'margin': 75},
        {'name': 'Salade César', 'qty': 420, 'revenue': 7140, 'cost': 22, 'margin': 78},
        {'name': 'Risotto Champignons', 'qty': 380, 'revenue': 8360, 'cost': 30, 'margin': 70},
        {'name': 'Poulet Rôti', 'qty': 350, 'revenue': 7700, 'cost': 35, 'margin': 65}
    ]
    
    df_menu = pd.DataFrame(menu_items)
    
    future_dates = pd.date_range(start=datetime.now() + timedelta(days=1), periods=30, freq='D')
    forecast_data = []
    for date in future_dates:
        day_of_week = date.dayofweek
        is_weekend = day_of_week >= 5
        
        base_revenue = 2700 if is_weekend else 1950
        revenue = base_revenue + np.random.normal(0, 200)
        
        forecast_data.append({
            'date': date,
            'predicted_revenue': max(0, revenue),
            'confidence_lower': revenue * 0.9,
            'confidence_upper': revenue * 1.1
        })
    
    df_forecast = pd.DataFrame(forecast_data)
    
    # Nouvelles données de prévision
    # Prévision prochaine journée (en heures)
    next_day_hours = []
    for hour in range(11, 23):
        if 12 <= hour <= 14:
            base_covers = 42
        elif 18 <= hour <= 21:
            base_covers = 58
        else:
            base_covers = 18
        
        covers = base_covers + np.random.randint(-5, 5)
        next_day_hours.append({
            'hour': hour,
            'hour_label': f"{hour}h",
            'predicted_covers': max(0, covers)
        })
    
    df_next_day = pd.DataFrame(next_day_hours)
    
    # Prévision 7 prochains jours
    next_7_days = []
    for i in range(1, 8):
        date = datetime.now() + timedelta(days=i)
        day_of_week = date.weekday()
        is_weekend = day_of_week >= 5
        
        base_covers = 85 if is_weekend else 65
        covers = base_covers + np.random.randint(-8, 8)
        
        next_7_days.append({
            'date': date,
            'day_name': date.strftime('%A'),
            'day_short': date.strftime('%a %d'),
            'predicted_covers': max(0, covers)
        })
    
    df_next_7_days = pd.DataFrame(next_7_days)
    
    # Prévision 3 prochains mois (plateaux mensuels)
    next_3_months = []
    for i in range(1, 4):
        date = datetime.now() + timedelta(days=30*i)
        month_name = date.strftime('%B')
        
        # Calcul basé sur les tendances saisonnières
        base_covers_month = 2100 + (i * 120)  # Tendance croissante
        covers = base_covers_month + np.random.randint(-100, 100)
        
        next_3_months.append({
            'month': month_name,
            'month_short': date.strftime('%b'),
            'predicted_covers': max(0, covers)
        })
    
    df_next_3_months = pd.DataFrame(next_3_months)
    
    staff_data = {
        'position': ['Serveurs', 'Cuisiniers', 'Aide-cuisine', 'Bar', 'Management'],
        'headcount': [12, 8, 5, 3, 2],
        'avg_hourly_rate': [16, 22, 15, 18, 35],
        'monthly_hours': [1800, 1600, 1200, 900, 640]
    }
    df_staff = pd.DataFrame(staff_data)
    df_staff['monthly_cost'] = df_staff['avg_hourly_rate'] * df_staff['monthly_hours']
    
    return df_sales, df_hourly, df_menu, df_forecast, df_staff, df_next_day, df_next_7_days, df_next_3_months

df_sales, df_hourly, df_menu, df_forecast, df_staff, df_next_day, df_next_7_days, df_next_3_months = generate_data()

# Sidebar
with st.sidebar:
    # Logo Optimisation+
    try:
        st.image("Logo_Rose.png", use_container_width=True)
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    except:
        # Fallback si le logo n'est pas trouvé
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); border-radius: 12px; margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 700;'>Optimisation+</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.85rem;'>Plateforme BI Restaurant</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Tableau de bord")
    
    date_range = st.date_input(
        "Période d'analyse",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )
    
    st.markdown("---")
    
    st.markdown("### 🎯 Filtres rapides")
    
    selected_metric = st.selectbox(
        "Métrique principale",
        ["Revenus", "Couverts", "Ticket moyen", "Marge"]
    )
    
    comparison_period = st.selectbox(
        "Comparer avec",
        ["Semaine dernière", "Mois dernier", "Même période année dernière"]
    )
    
    st.markdown("---")
    
    st.markdown("### 📈 KPIs en temps réel")
    
    current_revenue = df_sales['revenue'].tail(7).sum()
    previous_revenue = df_sales['revenue'].tail(14).head(7).sum()
    revenue_change = ((current_revenue - previous_revenue) / previous_revenue) * 100
    
    st.metric(
        "Revenus (7 derniers jours)",
        f"{current_revenue:,.0f} $",
        f"{revenue_change:+.1f}%"
    )
    
    current_covers = df_sales['covers'].tail(7).sum()
    previous_covers = df_sales['covers'].tail(14).head(7).sum()
    covers_change = ((current_covers - previous_covers) / previous_covers) * 100
    
    st.metric(
        "Couverts (7 derniers jours)",
        f"{current_covers:,.0f}",
        f"{covers_change:+.1f}%"
    )
    
    avg_ticket = current_revenue / current_covers if current_covers > 0 else 0
    prev_avg_ticket = previous_revenue / previous_covers if previous_covers > 0 else 0
    ticket_change = ((avg_ticket - prev_avg_ticket) / prev_avg_ticket * 100) if prev_avg_ticket > 0 else 0
    
    st.metric(
        "Ticket moyen",
        f"{avg_ticket:.2f} $",
        f"{ticket_change:+.1f}%"
    )
    
    st.markdown("---")
    
    st.markdown("### ⚡ Actions rapides")
    
    if st.button("📊 Exporter rapport", use_container_width=True):
        st.success("Rapport exporté avec succès!")
    
    if st.button("🔔 Configurer alertes", use_container_width=True):
        st.info("Configuration des alertes disponible prochainement")
    
    if st.button("💡 Suggestions IA", use_container_width=True):
        st.info("Suggestions personnalisées disponibles prochainement")

# Header
st.markdown('<h1 class="main-header">Optimisation+ | Intelligence d\'Affaires</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Tableaux de bord en temps réel pour optimiser votre restaurant</p>', unsafe_allow_html=True)

# Navigation par onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble", 
    "💰 Analyse des ventes", 
    "🍽️ Performance menu",
    "🔮 Prévisions & IA",
    "👥 Gestion personnel"
])

# TAB 1: Vue d'ensemble
with tab1:
    st.markdown('<div class="insight-box"><h4>💡 Insight du jour</h4><p style="font-size: 1.1rem; margin: 0;">Vos revenus ont augmenté de 12,3% cette semaine. Le Steak-Frites performe exceptionnellement bien (+28% vs semaine dernière).</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df_sales['revenue'].sum()
        st.metric(
            "Revenus totaux",
            f"{total_revenue:,.0f} $",
            "+12.3%",
            help="Revenus des 90 derniers jours"
        )
    
    with col2:
        total_covers = df_sales['covers'].sum()
        st.metric(
            "Couverts servis",
            f"{total_covers:,.0f}",
            "+8.7%",
            help="Nombre total de clients servis"
        )
    
    with col3:
        avg_ticket_all = total_revenue / total_covers if total_covers > 0 else 0
        st.metric(
            "Ticket moyen",
            f"{avg_ticket_all:.2f} $",
            "+3.2%",
            help="Revenu moyen par client"
        )
    
    with col4:
        total_margin = df_menu['margin'].mean()
        st.metric(
            "Marge moyenne",
            f"{total_margin:.1f}%",
            "+1.8%",
            help="Marge bénéficiaire moyenne"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Évolution des revenus (90 derniers jours)")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sales['date'],
            y=df_sales['revenue'],
            mode='lines',
            name='Revenus quotidiens',
            line=dict(color=COLORS['primary'], width=3),
            fill='tozeroy',
            fillcolor=f"rgba(221, 109, 109, 0.1)"
        ))
        
        fig.add_trace(go.Scatter(
            x=df_sales['date'],
            y=df_sales['revenue'].rolling(window=7).mean(),
            mode='lines',
            name='Moyenne mobile (7j)',
            line=dict(color=COLORS['secondary'], width=2, dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            yaxis_title="Revenus ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Performance par jour")
        
        day_performance = df_sales.groupby('day_of_week').agg({
            'revenue': 'mean',
            'covers': 'mean'
        }).round(0)
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        
        day_performance = day_performance.reindex(days_order)
        day_performance.index = days_fr
        
        fig = go.Figure(data=[
            go.Bar(
                x=day_performance.index,
                y=day_performance['revenue'],
                marker_color=[COLORS['primary'] if i >= 5 else COLORS['secondary'] for i in range(7)],
                text=day_performance['revenue'].astype(int),
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            height=400,
            yaxis_title="Revenus moyens ($)",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=10)
        )
        
        fig.update_xaxes(showgrid=False, tickangle=-45)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ✅ **Points forts cette semaine**
        - Weekend exceptionnel: +28% vs moyenne
        - Ticket moyen en hausse constante
        - Taux de rotation optimal (1.8 couverts/table)
        - Marge brute à 68% (excellent)
        """)
    
    with col2:
        st.warning("""
        ⚠️ **Points d'attention**
        - Lundi-mardi sous-performent (-15%)
        - Coûts alimentaires en légère hausse (+3%)
        - Temps d'attente moyen augmenté (18 min)
        - 2 plats peu performants à revoir
        """)

# TAB 2: Analyse des ventes
with tab2:
    st.subheader("Analyse détaillée des ventes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribution des ventes par période")
        
        fig = go.Figure(data=[go.Bar(
            x=df_hourly['hour'],
            y=df_hourly['covers'],
            marker_color=[
                COLORS['success'] if 12 <= int(h.split('h')[0]) <= 14 or 18 <= int(h.split('h')[0]) <= 21 
                else COLORS['primary'] 
                for h in df_hourly['hour']
            ],
            text=df_hourly['covers'],
            textposition='outside'
        )])
        
        fig.update_layout(
            height=400,
            yaxis_title="Nombre de couverts",
            xaxis_title="Période",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        fig.update_xaxes(showgrid=False, tickangle=-45)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **💡 Insight horaire**
        - Pic du midi: 12h-14h (125 couverts/jour)
        - Pic du soir: 19h-20h (145 couverts/jour)
        - Recommandation: Renforcer staff 18h30-21h
        """)
    
    with col2:
        st.markdown("#### Répartition revenus vs coûts")
        
        total_revenue_pie = df_sales['revenue'].sum()
        estimated_costs = total_revenue_pie * 0.32
        estimated_margin = total_revenue_pie - estimated_costs
        
        fig = go.Figure(data=[go.Pie(
            labels=['Marge nette', 'Coûts opérationnels'],
            values=[estimated_margin, estimated_costs],
            hole=0.5,
            marker_colors=[COLORS['success'], COLORS['warning']],
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            height=400,
            annotations=[dict(text=f'{(estimated_margin/total_revenue_pie*100):.1f}%<br>Marge', 
                             x=0.5, y=0.5, font_size=20, showarrow=False)],
            font=dict(family='Inter', size=11)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("""
        **💰 Performance financière**
        - Marge brute: 68%
        - Coût nourriture: 28%
        - Coût personnel: 32%
        - Autres coûts: 12%
        """)
    
    st.markdown("---")
    
    st.markdown("#### Tendances hebdomadaires")
    
    df_sales['week'] = df_sales['date'].dt.isocalendar().week
    weekly_data = df_sales.groupby('week').agg({
        'revenue': 'sum',
        'covers': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weekly_data['week'],
        y=weekly_data['revenue'],
        name='Revenus hebdo',
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=weekly_data['week'],
        y=weekly_data['covers'] * 30,
        name='Couverts (x30)',
        mode='lines+markers',
        line=dict(color=COLORS['secondary'], width=2, dash='dash'),
        marker=dict(size=6),
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        yaxis=dict(title="Revenus ($)"),
        yaxis2=dict(title="Couverts (x30)", overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11)
    )
    
    fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="Semaine")
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: Performance menu
with tab3:
    st.subheader("Analyse de performance du menu")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Top performers du menu")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df_menu['name'],
            x=df_menu['revenue'],
            name='Revenus',
            orientation='h',
            marker=dict(
                color=df_menu['margin'],
                colorscale=[[0, COLORS['danger']], [0.5, COLORS['warning']], [1, COLORS['success']]],
                showscale=True,
                colorbar=dict(title="Marge %")
            ),
            text=df_menu['revenue'].apply(lambda x: f"{x:,.0f}$"),
            textposition='outside'
        ))
        
        fig.update_layout(
            height=450,
            xaxis_title="Revenus générés ($)",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Matrice BCG")
        
        df_menu['revenue_score'] = (df_menu['revenue'] - df_menu['revenue'].min()) / (df_menu['revenue'].max() - df_menu['revenue'].min())
        df_menu['qty_score'] = (df_menu['qty'] - df_menu['qty'].min()) / (df_menu['qty'].max() - df_menu['qty'].min())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_menu['qty_score'],
            y=df_menu['revenue_score'],
            mode='markers+text',
            marker=dict(
                size=df_menu['margin'],
                color=df_menu['margin'],
                colorscale=[[0, COLORS['danger']], [0.5, COLORS['warning']], [1, COLORS['success']]],
                showscale=False,
                line=dict(width=2, color='white')
            ),
            text=df_menu['name'].str.split().str[0],
            textposition='top center',
            textfont=dict(size=9)
        ))
        
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.add_annotation(x=0.25, y=0.75, text="⭐ Stars", showarrow=False, font=dict(size=12, color=COLORS['success']))
        fig.add_annotation(x=0.75, y=0.75, text="💰 Cash Cows", showarrow=False, font=dict(size=12, color=COLORS['primary']))
        fig.add_annotation(x=0.25, y=0.25, text="❓ Question Marks", showarrow=False, font=dict(size=12, color=COLORS['warning']))
        fig.add_annotation(x=0.75, y=0.25, text="🐕 Dogs", showarrow=False, font=dict(size=12, color=COLORS['danger']))
        
        fig.update_layout(
            height=450,
            xaxis_title="Popularité →",
            yaxis_title="Revenus →",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("#### Détails du menu")
    
    display_df = df_menu[['name', 'qty', 'revenue', 'margin']].copy()
    display_df.columns = ['Plat', 'Quantité vendue', 'Revenus', 'Marge (%)']
    display_df['Revenus'] = display_df['Revenus'].apply(lambda x: f"{x:,.0f}$")
    
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Marge (%)": st.column_config.ProgressColumn(
                "Marge (%)",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
        }
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        **🌟 Plats stars**
        1. Steak-Frites (22,800$)
        2. Saumon Atlantique (18,900$)
        3. Pâtes Carbonara (17,800$)
        
        → Maintenir qualité et disponibilité
        """)
    
    with col2:
        st.warning("""
        **⚠️ À optimiser**
        - Poulet Rôti: faible marge (35%)
        - Salade César: peu vendue
        
        → Revoir recette ou retirer
        """)
    
    with col3:
        st.info("""
        **💡 Opportunités**
        - Augmenter prix Steak +2$
        - Promouvoir Risotto (marge 70%)
        - Bundle Pizza + Salade
        
        → Impact: +3,200$/mois
        """)

# TAB 4: Prévisions & IA
with tab4:
    st.subheader("Prévisions intelligentes et analyses prédictives")
    
    # Section 1: Prévision prochaine journée (en heures)
    st.markdown("#### 📅 Prévision pour la prochaine journée (par heure)")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_next_day['hour_label'],
        y=df_next_day['predicted_covers'],
        marker_color=[
            COLORS['success'] if 12 <= h <= 14 or 18 <= h <= 21 
            else COLORS['primary'] 
            for h in df_next_day['hour']
        ],
        text=df_next_day['predicted_covers'],
        textposition='outside',
        name='Couverts prévus'
    ))
    
    fig.update_layout(
        height=350,
        yaxis_title="Nombre de couverts prévus",
        xaxis_title="Heure",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11)
    )
    
    fig.update_xaxes(showgrid=False, tickangle=-45)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    total_next_day = df_next_day['predicted_covers'].sum()
    peak_hour = df_next_day.loc[df_next_day['predicted_covers'].idxmax()]
    
    with col1:
        st.metric(
            "Total couverts prévus demain",
            f"{total_next_day:.0f}",
            "+8% vs moyenne"
        )
    
    with col2:
        st.metric(
            "Heure de pointe",
            f"{peak_hour['hour_label']}",
            f"{peak_hour['predicted_covers']:.0f} couverts"
        )
    
    with col3:
        estimated_revenue = total_next_day * 52
        st.metric(
            "Revenus estimés",
            f"{estimated_revenue:,.0f} $",
            "Ticket moyen: 52$"
        )
    
    st.markdown("---")
    
    # Section 2: Prévision 7 prochains jours
    st.markdown("#### 📆 Prévision pour les 7 prochains jours")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_next_7_days['day_short'],
        y=df_next_7_days['predicted_covers'],
        marker_color=[
            COLORS['accent'] if 'Sam' in day or 'Dim' in day 
            else COLORS['secondary'] 
            for day in df_next_7_days['day_short']
        ],
        text=df_next_7_days['predicted_covers'],
        textposition='outside',
        name='Couverts prévus'
    ))
    
    fig.update_layout(
        height=350,
        yaxis_title="Nombre de couverts prévus",
        xaxis_title="Jour",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11)
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    total_7_days = df_next_7_days['predicted_covers'].sum()
    best_day = df_next_7_days.loc[df_next_7_days['predicted_covers'].idxmax()]
    
    with col1:
        st.metric(
            "Total 7 jours",
            f"{total_7_days:.0f} couverts",
            "+12% vs semaine dernière"
        )
    
    with col2:
        st.metric(
            "Meilleur jour prévu",
            best_day['day_name'],
            f"{best_day['predicted_covers']:.0f} couverts"
        )
    
    with col3:
        avg_7_days = total_7_days / 7
        st.metric(
            "Moyenne quotidienne",
            f"{avg_7_days:.0f} couverts",
            "Stable"
        )
    
    st.markdown("---")
    
    # Section 3: Prévision 3 prochains mois (plateaux mensuels)
    st.markdown("#### 📊 Prévision des plateaux mensuels (3 prochains mois)")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_next_3_months['month'],
        y=df_next_3_months['predicted_covers'],
        marker=dict(
            color=df_next_3_months['predicted_covers'],
            colorscale=[[0, COLORS['secondary']], [1, COLORS['primary']]],
            showscale=False
        ),
        text=df_next_3_months['predicted_covers'].apply(lambda x: f"{x:.0f}"),
        textposition='outside',
        name='Couverts mensuels prévus'
    ))
    
    fig.update_layout(
        height=350,
        yaxis_title="Nombre de couverts mensuels",
        xaxis_title="Mois",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11)
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    total_3_months = df_next_3_months['predicted_covers'].sum()
    growth_rate = ((df_next_3_months.iloc[-1]['predicted_covers'] - df_next_3_months.iloc[0]['predicted_covers']) / df_next_3_months.iloc[0]['predicted_covers']) * 100
    
    with col1:
        st.metric(
            "Total 3 mois",
            f"{total_3_months:,.0f} couverts",
            f"+{growth_rate:.1f}% croissance"
        )
    
    with col2:
        avg_monthly = total_3_months / 3
        st.metric(
            "Moyenne mensuelle",
            f"{avg_monthly:,.0f} couverts",
            "Tendance haussière"
        )
    
    with col3:
        best_month = df_next_3_months.loc[df_next_3_months['predicted_covers'].idxmax()]
        st.metric(
            "Meilleur mois prévu",
            best_month['month'],
            f"{best_month['predicted_covers']:.0f} couverts"
        )
    
    st.markdown("---")
    
    # Prévisions revenus 30 jours (graphique existant)
    st.markdown("#### 💰 Prévisions de revenus (30 prochains jours)")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_forecast['date'],
        y=df_forecast['predicted_revenue'],
        mode='lines',
        name='Revenus prévus',
        line=dict(color=COLORS['success'], width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_forecast['date'],
        y=df_forecast['confidence_upper'],
        mode='lines',
        name='Intervalle confiance',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=df_forecast['date'],
        y=df_forecast['confidence_lower'],
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.1)',
        line=dict(width=0),
        name='Intervalle confiance',
        showlegend=True
    ))
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        yaxis_title="Revenus ($)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11)
    )
    
    fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    predicted_total = df_forecast['predicted_revenue'].sum()
    
    with col1:
        st.metric(
            "Revenus prévus (30j)",
            f"{predicted_total:,.0f} $",
            "+15.2% vs période équivalente"
        )
    
    with col2:
        st.metric(
            "Précision du modèle",
            "94.3%",
            "Basé sur 18 mois"
        )
    
    with col3:
        best_day_rev = df_forecast.loc[df_forecast['predicted_revenue'].idxmax()]
        st.metric(
            "Meilleur jour prévu",
            best_day_rev['date'].strftime('%d/%m'),
            f"{best_day_rev['predicted_revenue']:.0f} $"
        )
    
    with col4:
        st.metric(
            "Économies identifiées",
            "3,840$/mois",
            "Grâce aux prévisions"
        )
    
    st.markdown("---")
    
    st.markdown("#### Alertes et recommandations prédictives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        **Alerte: Forte affluence prévue**
        - Date: Vendredi 25 octobre
        - Couverts estimés: 420 (+45% vs moyenne)
        - Actions recommandées:
            - Ajouter 2 serveurs (18h-22h)
            - Commander +30% poulet et pâtes
            - Préparer sauces à l'avance
        """)
    
    with col2:
        st.warning("""
        **Impact météo détecté**
        - Prévision: Pluie mardi prochain
        - Impact attendu: -15% dine-in, +25% livraison
        - Actions recommandées:
            - Augmenter stock plats à emporter
            - Renforcer équipe livraison
            - Promotion "Comfort food" spéciale
        """)

# TAB 5: Gestion personnel
with tab5:
    st.subheader("Analyse et optimisation du personnel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Répartition des coûts de personnel")
        
        fig = go.Figure(data=[go.Pie(
            labels=df_staff['position'],
            values=df_staff['monthly_cost'],
            hole=0.4,
            marker_colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success'], COLORS['warning']]
        )])
        
        fig.update_layout(
            height=400,
            font=dict(family='Inter', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Détail par poste")
        
        display_df = df_staff[['position', 'headcount', 'avg_hourly_rate', 'monthly_cost']].copy()
        display_df.columns = ['Poste', 'Effectif', 'Taux horaire', 'Coût mensuel']
        display_df['Taux horaire'] = display_df['Taux horaire'].apply(lambda x: f"{x}$/h")
        display_df['Coût mensuel'] = display_df['Coût mensuel'].apply(lambda x: f"{x:,.0f}$")
        
        st.dataframe(display_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_staff_cost = df_staff['monthly_cost'].sum()
    
    with col1:
        st.metric(
            "Coût total personnel",
            f"{total_staff_cost:,.0f}$/mois",
            "-2.3% vs mois dernier"
        )
    
    with col2:
        labor_percentage = (total_staff_cost / (df_sales['revenue'].sum() / 3)) * 100
        st.metric(
            "% Coût du travail",
            f"{labor_percentage:.1f}%",
            "Cible: 30-35%"
        )
    
    with col3:
        st.metric(
            "Taux de rotation",
            "12%/an",
            "-3% vs année dernière"
        )
    
    with col4:
        st.metric(
            "Productivité",
            "1,847$/employé",
            "+5.2%"
        )
    
    st.markdown("---")
    
    st.markdown("#### Optimisation des horaires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **Périodes bien staffées**
        - Vendredi-Samedi soir (18h-21h)
        - Dimanche midi (11h-14h)
        - Mercredi midi (12h-13h30)
        
        Taux de couverture: 95%
        """)
        
        st.info("""
        **Recommandations d'économies**
        - Réduire 1 serveur lundi-mardi 14h-17h
        - Économie estimée: 1,920$/mois
        - Impact service: Minimal (affluence faible)
        """)
    
    with col2:
        st.warning("""
        **Périodes sous-staffées**
        - Jeudi soir (19h-21h)
        - Samedi midi (12h-14h)
        
        Impact: Temps d'attente +15 min
        Satisfaction: -0.3 points
        """)
        
        st.error("""
        **Action requise**
        - Ajouter 1 serveur jeudi 18h-22h
        - Ajouter 1 aide-cuisine samedi 11h-15h
        - Coût: 1,280$/mois
        - ROI: +2,400$/mois (meilleur service)
        """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {COLORS['text']}; padding: 2rem; font-size: 0.9rem;'>
    <p style='margin: 0; font-weight: 500;'>Optimisation+ | Plateforme BI Restaurant</p>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.7;'>Données mises à jour en temps réel © 2025</p>
</div>
""", unsafe_allow_html=True)
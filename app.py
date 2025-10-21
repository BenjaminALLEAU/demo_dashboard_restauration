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

# Palette de couleurs professionnelle
COLORS = {
    'primary': '#2563eb',      # Bleu professionnel
    'secondary': '#7c3aed',    # Violet tech
    'accent': '#06b6d4',       # Cyan moderne
    'success': '#10b981',      # Vert
    'warning': '#f59e0b',      # Orange
    'danger': '#ef4444',       # Rouge
    'dark': '#1e293b',         # Gris foncé
    'light': '#f8fafc',        # Gris clair
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
    
    staff_data = {
        'position': ['Serveurs', 'Cuisiniers', 'Aide-cuisine', 'Bar', 'Management'],
        'headcount': [12, 8, 5, 3, 2],
        'avg_hourly_rate': [16, 22, 15, 18, 35],
        'monthly_hours': [1800, 1600, 1200, 900, 640]
    }
    df_staff = pd.DataFrame(staff_data)
    df_staff['monthly_cost'] = df_staff['avg_hourly_rate'] * df_staff['monthly_hours']
    
    return df_sales, df_hourly, df_menu, df_forecast, df_staff

df_sales, df_hourly, df_menu, df_forecast, df_staff = generate_data()

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); border-radius: 12px; margin-bottom: 1.5rem;'>
        <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 700;'>Optimisation+</h2>
        <p style='color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.85rem;'>Plateforme BI Restaurant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Période d'analyse")
    period = st.selectbox(
        "Sélectionnez la période",
        ["7 derniers jours", "30 derniers jours", "90 derniers jours", "Année en cours"],
        label_visibility="collapsed"
    )
    
    period_map = {
        "7 derniers jours": 7,
        "30 derniers jours": 30,
        "90 derniers jours": 90,
        "Année en cours": 365
    }
    days = period_map[period]
    df_filtered = df_sales.tail(days)
    
    st.markdown("---")
    st.subheader("Filtres avancés")
    
    selected_days = st.multiselect(
        "Jours de la semaine",
        options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        default=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        label_visibility="collapsed"
    )
    
    if selected_days:
        df_filtered = df_filtered[df_filtered['day_of_week'].isin(selected_days)]
    
    st.markdown("---")
    st.info("Utilisez les filtres pour analyser des périodes spécifiques et identifier les tendances.")

# Header
st.markdown(f'<div class="main-header">Tableau de bord analytique</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Intelligence d\'affaires alimentée par l\'IA • Optimisation+</div>', unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Vue d'ensemble", 
    "Analyse des ventes", 
    "Performance menu",
    "Prévisions IA",
    "Gestion du personnel"
])

# TAB 1: Vue d'ensemble
with tab1:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_revenue = df_filtered['revenue'].sum()
    total_covers = df_filtered['covers'].sum()
    avg_ticket = df_filtered['avg_ticket'].mean()
    
    prev_period = df_sales.tail(days * 2).head(days)
    prev_revenue = prev_period['revenue'].sum()
    revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    with col1:
        st.metric(
            "Chiffre d'affaires",
            f"{total_revenue:,.0f} $",
            f"{revenue_change:+.1f}%"
        )
    
    with col2:
        covers_change = ((total_covers - prev_period['covers'].sum()) / prev_period['covers'].sum() * 100)
        st.metric(
            "Nombre de couverts",
            f"{total_covers:,.0f}",
            f"{covers_change:+.1f}%"
        )
    
    with col3:
        ticket_change = ((avg_ticket - prev_period['avg_ticket'].mean()) / prev_period['avg_ticket'].mean() * 100)
        st.metric(
            "Ticket moyen",
            f"{avg_ticket:.2f} $",
            f"{ticket_change:+.1f}%"
        )
    
    with col4:
        st.metric(
            "Taux d'occupation",
            "74%",
            "-1.2%"
        )
    
    with col5:
        st.metric(
            "Satisfaction client",
            "4.7/5",
            "+0.2"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Évolution du chiffre d'affaires")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['revenue'],
            mode='lines',
            name='Revenus',
            line=dict(color=COLORS['primary'], width=3),
            fill='tozeroy',
            fillcolor=f"rgba(37, 99, 235, 0.1)"
        ))
        
        df_filtered['ma7'] = df_filtered['revenue'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['ma7'],
            mode='lines',
            name='Moyenne mobile (7j)',
            line=dict(color=COLORS['warning'], width=2, dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Affluence par heure")
        
        fig = go.Figure()
        
        colors = [COLORS['success'] if x > 60 else COLORS['warning'] if x > 30 else COLORS['accent'] 
                  for x in df_hourly['covers']]
        
        fig.add_trace(go.Bar(
            x=df_hourly['hour'],
            y=df_hourly['covers'],
            marker_color=colors,
            text=df_hourly['covers'],
            textposition='outside'
        ))
        
        fig.update_layout(
            height=400,
            showlegend=False,
            yaxis_title="Nombre de couverts",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Insights IA - Recommandations prioritaires")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <h4>Opportunité détectée</h4>
            <p><strong>Jeudi soir sous-optimisé</strong></p>
            <p>Taux d'occupation: 48% vs 75% en moyenne</p>
            <p><strong>Potentiel: +2,400$/mois</strong></p>
            <p>Action: Promotion "Soirée duo" jeudi 18h-21h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4 style="font-weight: 600; margin-bottom: 0.5rem;">Alerte gaspillage</h4>
            <p style="margin: 0.25rem 0;"><strong>Saumon Atlantique</strong></p>
            <p style="margin: 0.25rem 0;">Taux de perte: 18% (cible: <10%)</p>
            <p style="margin: 0.25rem 0;"><strong>Économie: 780$/mois</strong></p>
            <p style="margin: 0.25rem 0;">Action: Réduire commandes de 25% lun-mar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="success-box">
            <h4 style="font-weight: 600; margin-bottom: 0.5rem;">Performance exceptionnelle</h4>
            <p style="margin: 0.25rem 0;"><strong>Pâtes Carbonara</strong></p>
            <p style="margin: 0.25rem 0;">Marge: 72% | Popularité: #1</p>
            <p style="margin: 0.25rem 0;"><strong>Impact: +3-5% marge globale</strong></p>
            <p style="margin: 0.25rem 0;">Action: Mise en vedette dans menu</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Analyse des ventes
with tab2:
    st.subheader("Analyse approfondie des ventes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Revenus par jour de la semaine")
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_names_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        
        weekly_data = df_sales.groupby('day_of_week').agg({
            'revenue': 'mean',
            'covers': 'mean'
        }).reindex(day_order)
        
        weekly_data['day_fr'] = day_names_fr
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weekly_data['day_fr'],
            y=weekly_data['revenue'],
            marker_color=COLORS['secondary'],
            text=[f"{x:.0f}$" for x in weekly_data['revenue']],
            textposition='outside'
        ))
        
        fig.update_layout(
            height=400, 
            showlegend=False, 
            yaxis_title="Revenus moyens",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Répartition des revenus")
        
        revenue_breakdown = {
            'Plats principaux': 45,
            'Entrées': 15,
            'Desserts': 12,
            'Boissons': 18,
            'Vins & alcools': 10
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(revenue_breakdown.keys()),
            values=list(revenue_breakdown.values()),
            hole=0.4,
            marker_colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success'], COLORS['warning']]
        )])
        
        fig.update_layout(
            height=400, 
            showlegend=True,
            font=dict(family='Inter', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 5 jours les plus rentables")
        top_days = df_sales.nlargest(5, 'revenue')[['date', 'revenue', 'covers']]
        top_days['date'] = top_days['date'].dt.strftime('%d/%m/%Y')
        top_days['revenue'] = top_days['revenue'].apply(lambda x: f"{x:,.0f}$")
        st.dataframe(top_days, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### Tendances mensuelles")
        monthly = df_sales.groupby(df_sales['date'].dt.to_period('M')).agg({
            'revenue': 'sum',
            'covers': 'sum'
        }).reset_index()
        monthly['date'] = monthly['date'].astype(str)
        monthly['avg_ticket'] = monthly['revenue'] / monthly['covers']
        
        st.dataframe(
            monthly.style.format({
                'revenue': '{:,.0f}$',
                'covers': '{:,.0f}',
                'avg_ticket': '{:.2f}$'
            }),
            hide_index=True,
            use_container_width=True
        )

# TAB 3: Performance menu
with tab3:
    st.subheader("Analyse de performance du menu")
    
    # Graphique principal - Barres horizontales
    st.markdown("#### Performance des plats - Marge & Volume")
    
    # Trier par score
    df_menu['score'] = (df_menu['qty'] / df_menu['qty'].max() * 50 + 
                       df_menu['margin'] / 100 * 50)
    df_menu_sorted = df_menu.sort_values('score', ascending=True)
    
    fig = go.Figure()
    
    # Barres de marge
    fig.add_trace(go.Bar(
        y=df_menu_sorted['name'],
        x=df_menu_sorted['margin'],
        name='Marge (%)',
        orientation='h',
        marker=dict(
            color=df_menu_sorted['margin'],
            colorscale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']],
            showscale=False
        ),
        text=df_menu_sorted['margin'].apply(lambda x: f"{x}%"),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Marge: %{x}%<extra></extra>'
    ))
    
    fig.update_layout(
        height=450,
        xaxis_title="Marge (%)",
        yaxis_title="",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=12, color='#333'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            range=[0, 100]
        ),
        yaxis=dict(
            showgrid=False
        ),
        margin=dict(t=20, b=40, l=20, r=80),
        showlegend=False
    )
    
    # Ligne de référence pour la marge cible
    fig.add_vline(
        x=65,
        line_dash="dash",
        line_color="gray",
        opacity=0.5,
        annotation_text="Marge cible: 65%",
        annotation_position="top right"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Tableau de données avec métriques
    st.markdown("#### Détails par plat")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Préparer le dataframe pour affichage
        display_menu = df_menu.sort_values('score', ascending=False)[['name', 'qty', 'margin', 'revenue']].copy()
        display_menu.columns = ['Plat', 'Quantité vendue', 'Marge (%)', 'Revenus ($)']
        display_menu['Revenus ($)'] = display_menu['Revenus ($)'].apply(lambda x: f"{x:,.0f} $")
        
        st.dataframe(
            display_menu,
            hide_index=True,
            use_container_width=True,
            height=350
        )
    
    with col2:
        st.markdown("##### Top 3 performers")
        
        top_3 = df_menu.nlargest(3, 'score')
        
        for idx, (i, row) in enumerate(top_3.iterrows(), 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                        padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem;
                        border-left: 4px solid {COLORS['primary']};'>
                <div style='font-weight: 600; font-size: 1rem; margin-bottom: 0.25rem;'>
                    {medal} {row['name']}
                </div>
                <div style='font-size: 0.85rem; color: #64748b;'>
                    Score: {row['score']:.0f}/100<br>
                    Marge: {row['margin']}% • Ventes: {row['qty']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("##### Alertes")
        
        bottom_2 = df_menu.nsmallest(2, 'score')
        
        for i, row in bottom_2.iterrows():
            st.markdown(f"""
            <div style='background: #fef3c7; padding: 0.75rem; border-radius: 8px; 
                        margin-bottom: 0.5rem; border-left: 4px solid {COLORS['warning']};'>
                <div style='font-weight: 600; font-size: 0.9rem;'>{row['name']}</div>
                <div style='font-size: 0.8rem; color: #64748b;'>
                    Marge faible: {row['margin']}%
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recommandations simplifiées
    st.markdown("#### Recommandations stratégiques")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="alert-success">
            <strong>Stars à promouvoir</strong><br><br>
            • Pâtes Carbonara (72% marge)<br>
            • Pizza Margherita (75% marge)<br>
            • Salade César (78% marge)<br><br>
            <strong>Action:</strong> Mise en avant visuelle
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="alert-warning">
            <strong>À optimiser</strong><br><br>
            • Saumon (52% marge, gaspillage)<br>
            • Steak-Frites (55% marge)<br><br>
            <strong>Action:</strong> Renégocier fournisseurs
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="alert-info">
            <strong>Opportunités</strong><br><br>
            • Plats végétariens (+25% demande)<br>
            • Menu saisonnier<br>
            • Formules midi<br><br>
            <strong>Action:</strong> Test A/B 2 semaines
        </div>
        """, unsafe_allow_html=True)

# TAB 4: Prévisions IA
with tab4:
    st.subheader("Prévisions intelligentes alimentées par l'IA")
    
    st.markdown("#### Prévision des revenus - 30 prochains jours")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_sales.tail(30)['date'],
        y=df_sales.tail(30)['revenue'],
        mode='lines',
        name='Historique',
        line=dict(color=COLORS['primary'], width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_forecast['date'],
        y=df_forecast['predicted_revenue'],
        mode='lines',
        name='Prévisions IA',
        line=dict(color=COLORS['success'], width=3, dash='dash')
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
        best_day = df_forecast.loc[df_forecast['predicted_revenue'].idxmax()]
        st.metric(
            "Meilleur jour prévu",
            best_day['date'].strftime('%d/%m'),
            f"{best_day['predicted_revenue']:.0f} $"
        )
    
    with col4:
        st.metric(
            "Économies identifiées",
            "3,840$/mois",
            "Grâce aux prévisions"
        )
    
    st.markdown("---")
    
    st.markdown("#### Facteurs d'influence détectés par l'IA")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        factors = {
            'Météo': 18,
            'Événements locaux': 25,
            'Jours fériés': 30,
            'Saison': 22,
            'Promotions': 35,
            'Réseaux sociaux': 15
        }
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=list(factors.values()),
            theta=list(factors.keys()),
            fill='toself',
            fillcolor=f"rgba(37, 99, 235, 0.2)",
            line=dict(color=COLORS['primary'], width=3)
        ))
        
        fig.update_layout(
            height=400,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 40])
            ),
            showlegend=False,
            font=dict(family='Inter', size=11)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Impact sur revenus")
        for factor, impact in sorted(factors.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"**{factor}**")
            st.progress(impact / 40)
            st.caption(f"±{impact}% d'impact")
    
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
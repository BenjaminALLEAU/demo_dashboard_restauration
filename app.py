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
    
    .status-card {{
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    
    .status-green {{
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid {COLORS['success']};
    }}
    
    .status-yellow {{
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid {COLORS['warning']};
    }}
    
    .status-red {{
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 4px solid {COLORS['danger']};
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
        
        # Patterns réalistes : vendredi > samedi > jeudi > dimanche > mercredi > mardi > lundi
        day_multipliers = {
            0: 0.75,  # Lundi (faible)
            1: 0.80,  # Mardi
            2: 0.90,  # Mercredi
            3: 1.05,  # Jeudi (pré-weekend)
            4: 1.30,  # Vendredi (fort)
            5: 1.25,  # Samedi (fort)
            6: 1.00   # Dimanche (moyen)
        }
        
        base_revenue = 2000 * day_multipliers[day_of_week]
        revenue = base_revenue + np.random.normal(0, 150)
        
        # Ticket moyen réaliste entre 45-65$
        avg_ticket = np.random.uniform(48, 58)
        covers = int(revenue / avg_ticket)
        
        # Calcul des coûts réalistes
        food_cost_pct = np.random.uniform(0.28, 0.32)  # 28-32% food cost
        labor_cost_pct = np.random.uniform(0.30, 0.35)  # 30-35% labor cost
        
        food_cost = revenue * food_cost_pct
        labor_cost = revenue * labor_cost_pct
        other_costs = revenue * 0.15  # Autres coûts fixes
        
        sales_data.append({
            'date': date,
            'revenue': max(0, revenue),
            'covers': max(0, covers),
            'avg_ticket': avg_ticket,
            'day_of_week': date.strftime('%A'),
            'food_cost': food_cost,
            'labor_cost': labor_cost,
            'other_costs': other_costs,
            'total_costs': food_cost + labor_cost + other_costs,
            'gross_profit': revenue - (food_cost + labor_cost + other_costs)
        })
    
    df_sales = pd.DataFrame(sales_data)
    
    # Données horaires réalistes avec rush du midi et du soir
    hours = list(range(11, 23))
    hourly_data = []
    for hour in hours:
        # Lunch rush: 11h30-13h30 avec pic à 12h30
        if hour == 11:
            covers = np.random.randint(15, 25)
        elif hour == 12:
            covers = np.random.randint(45, 60)  # Peak lunch
        elif hour == 13:
            covers = np.random.randint(35, 50)
        elif hour == 14:
            covers = np.random.randint(10, 20)
        # Creux de l'après-midi
        elif 15 <= hour <= 17:
            covers = np.random.randint(5, 15)
        # Dinner rush: 18h-21h avec pic à 19h-20h
        elif hour == 18:
            covers = np.random.randint(35, 50)
        elif hour == 19:
            covers = np.random.randint(65, 85)  # Peak dinner
        elif hour == 20:
            covers = np.random.randint(55, 75)
        elif hour == 21:
            covers = np.random.randint(30, 45)
        else:
            covers = np.random.randint(10, 20)
        
        # Ticket moyen légèrement plus élevé le soir
        ticket_multiplier = 1.15 if hour >= 18 else 1.0
        avg_ticket = np.random.uniform(48, 58) * ticket_multiplier
        
        hourly_data.append({
            'hour': f"{hour}h-{hour+1}h",
            'hour_num': hour,
            'covers': covers,
            'revenue': covers * avg_ticket,
            'avg_ticket': avg_ticket
        })
    
    df_hourly = pd.DataFrame(hourly_data)
    
    # Menu items avec catégories et marges réalistes
    menu_items = [
        # Entrées (marge élevée)
        {'name': 'Salade César', 'category': 'Entrées', 'qty': 420, 'price': 17, 'cost': 3.80, 'revenue': 7140, 'margin': 78},
        {'name': 'Soupe du jour', 'category': 'Entrées', 'qty': 280, 'price': 9, 'cost': 1.80, 'revenue': 2520, 'margin': 80},
        
        # Plats principaux (marge moyenne)
        {'name': 'Steak-Frites', 'category': 'Viandes', 'qty': 760, 'price': 30, 'cost': 13.50, 'revenue': 22800, 'margin': 55},
        {'name': 'Saumon Atlantique', 'category': 'Poissons', 'qty': 540, 'price': 35, 'cost': 16.80, 'revenue': 18900, 'margin': 52},
        {'name': 'Poulet Rôti', 'category': 'Viandes', 'qty': 350, 'price': 22, 'cost': 7.70, 'revenue': 7700, 'margin': 65},
        
        # Pâtes et pizzas (marge très élevée)
        {'name': 'Pâtes Carbonara', 'category': 'Pâtes', 'qty': 890, 'price': 20, 'cost': 5.60, 'revenue': 17800, 'margin': 72},
        {'name': 'Pizza Margherita', 'category': 'Pizzas', 'qty': 470, 'price': 18, 'cost': 4.50, 'revenue': 8460, 'margin': 75},
        {'name': 'Risotto Champignons', 'category': 'Pâtes', 'qty': 380, 'price': 22, 'cost': 6.60, 'revenue': 8360, 'margin': 70},
        
        # Burgers (marge bonne)
        {'name': 'Burger Signature', 'category': 'Burgers', 'qty': 680, 'price': 20, 'cost': 6.40, 'revenue': 13600, 'margin': 68},
    ]
    
    df_menu = pd.DataFrame(menu_items)
    df_menu['food_cost_pct'] = (df_menu['cost'] / df_menu['price'] * 100).round(1)
    
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
    
    # Prévision 3 prochains mois
    next_3_months = []
    for i in range(1, 4):
        date = datetime.now() + timedelta(days=30*i)
        month_name = date.strftime('%B')
        
        base_covers_month = 2100 + (i * 120)
        covers = base_covers_month + np.random.randint(-100, 100)
        
        next_3_months.append({
            'month': month_name,
            'month_short': date.strftime('%b'),
            'predicted_covers': max(0, covers)
        })
    
    df_next_3_months = pd.DataFrame(next_3_months)
    
    staff_data = {
        'position': ['Serveurs', 'Cuisiniers', 'Aide-cuisine', 'Plongeurs', 'Bar', 'Gérance'],
        'headcount': [8, 6, 4, 2, 2, 2],
        'avg_hourly_rate': [15, 24, 16, 15, 18, 40],
        'weekly_hours': [320, 240, 180, 80, 90, 80],  # Heures par semaine
        'productive_pct': [85, 90, 85, 80, 85, 70]  # % temps productif
    }
    df_staff = pd.DataFrame(staff_data)
    df_staff['monthly_hours'] = df_staff['weekly_hours'] * 4.33  # Moyenne mois
    df_staff['monthly_cost'] = (df_staff['avg_hourly_rate'] * df_staff['monthly_hours']).round(0)
    df_staff['productive_hours'] = (df_staff['monthly_hours'] * df_staff['productive_pct'] / 100).round(0)
    
    # Calcul du RevPASH (Revenue Per Available Seat Hour) - métrique clé en restauration
    total_seats = 80
    hours_open_per_day = 12
    days_per_month = 30
    available_seat_hours = total_seats * hours_open_per_day * days_per_month
    monthly_revenue = df_sales['revenue'].tail(30).sum()
    revpash = monthly_revenue / available_seat_hours
    
    return df_sales, df_hourly, df_menu, df_forecast, df_staff, df_next_day, df_next_7_days, df_next_3_months, revpash

df_sales, df_hourly, df_menu, df_forecast, df_staff, df_next_day, df_next_7_days, df_next_3_months, revpash = generate_data()

# Calcul des KPIs essentiels de restaurant
def calculate_restaurant_kpis(df_sales, df_staff):
    # Prime Cost (Food + Labor) - doit être < 60% idéalement
    recent_revenue = df_sales['revenue'].tail(30).sum()
    recent_food_cost = df_sales['food_cost'].tail(30).sum()
    recent_labor_cost = df_staff['monthly_cost'].sum()
    prime_cost = recent_food_cost + recent_labor_cost
    prime_cost_pct = (prime_cost / recent_revenue * 100) if recent_revenue > 0 else 0
    
    # Table Turn Rate (rotation des tables) - cible 1.5-2.5 par service
    avg_daily_covers = df_sales['covers'].tail(30).mean()
    total_seats = 80
    lunch_turns = (df_hourly[df_hourly['hour_num'].between(11, 15)]['covers'].sum() / total_seats)
    dinner_turns = (df_hourly[df_hourly['hour_num'].between(18, 22)]['covers'].sum() / total_seats)
    
    # Seat Occupancy (taux d'occupation) - cible 65-75%
    hours_open_per_day = 12
    max_possible_covers = total_seats * hours_open_per_day
    seat_occupancy = (avg_daily_covers / max_possible_covers * 100) if max_possible_covers > 0 else 0
    
    # Break-even covers
    total_monthly_costs = df_sales['total_costs'].tail(30).sum()
    avg_contribution_margin = df_sales['avg_ticket'].mean() * 0.60  # 60% contribution
    break_even_covers_daily = (total_monthly_costs / 30) / avg_contribution_margin if avg_contribution_margin > 0 else 0
    
    return {
        'prime_cost_pct': prime_cost_pct,
        'lunch_turns': lunch_turns,
        'dinner_turns': dinner_turns,
        'seat_occupancy': seat_occupancy,
        'break_even_covers': break_even_covers_daily,
        'recent_revenue': recent_revenue,
        'recent_profit': df_sales['gross_profit'].tail(30).sum()
    }

kpis = calculate_restaurant_kpis(df_sales, df_staff)

# Sidebar
with st.sidebar:
    try:
        st.image("Logo_Rose.png", use_container_width=True)
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    except:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%); border-radius: 12px; margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 700;'>Optimisation+</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.85rem;'>Plateforme BI Restaurant</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Période d'analyse")
    
    period_choice = st.radio(
        "Choisir une période",
        ["Aujourd'hui", "Cette semaine", "4 semaines roulantes"],
        index=1
    )
    
    st.markdown("---")
    
    st.markdown("### 🎯 Filtres rapides")
    
    selected_metric = st.selectbox(
        "Métrique principale",
        ["Revenus", "Couverts", "Ticket moyen", "Marge"]
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

# Header
st.markdown('<h1 class="main-header">Optimisation+ | Intelligence d\'Affaires</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Tableaux de bord en temps réel pour optimiser votre restaurant</p>', unsafe_allow_html=True)

# Navigation par onglets selon la nouvelle structure
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Mon Tableau de bord", 
    "⚙️ Suivi des opérations",
    "📈 Analyses",
    "💰 Suivi des coûts et revenus"
])

# TAB 1: Mon Tableau de bord
with tab1:
    st.markdown("### 📊 Vue d'ensemble des performances")
    
    # KPIs critiques essentiels seulement
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Coût Principal",
            f"{kpis['prime_cost_pct']:.1f}%",
            "Cible: < 60%",
            delta_color="inverse",
            help="Coût nourriture + main d'œuvre combinés"
        )
    
    with col2:
        avg_ticket = df_sales['avg_ticket'].tail(30).mean()
        st.metric(
            "Ticket moyen",
            f"{avg_ticket:.2f}$",
            "+2.1%",
            help="Montant moyen dépensé par client"
        )
    
    with col3:
        profit_margin = (kpis['recent_profit'] / kpis['recent_revenue'] * 100) if kpis['recent_revenue'] > 0 else 0
        st.metric(
            "Marge nette",
            f"{profit_margin:.1f}%",
            "Cible: 15-20%",
            help="Profit après tous les coûts"
        )
    
    with col4:
        daily_covers = df_sales['covers'].tail(7).mean()
        st.metric(
            "Couverts/jour",
            f"{daily_covers:.0f}",
            "+5.2%",
            help="Nombre moyen de clients par jour"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏢 Mes opérations")
        
        # Détermination des statuts basés sur les KPIs réels
        lunch_status = 'VERT' if kpis['lunch_turns'] >= 1.5 else 'JAUNE'
        dinner_status = 'VERT' if kpis['dinner_turns'] >= 1.8 else 'JAUNE'
        menu_status = 'VERT' if df_menu['margin'].mean() >= 65 else 'JAUNE'
        occupancy_status = 'VERT' if 65 <= kpis['seat_occupancy'] <= 75 else 'JAUNE'
        
        operations_status = {
            f'Rotation midi ({kpis["lunch_turns"]:.1f}x)': lunch_status,
            f'Rotation soir ({kpis["dinner_turns"]:.1f}x)': dinner_status,
            f'Performance menu': menu_status,
            f'Taux d\'occupation ({kpis["seat_occupancy"]:.0f}%)': occupancy_status
        }
        
        for item, status in operations_status.items():
            if status == 'VERT':
                st.markdown(f'<div class="status-card status-green">✅ <strong>{item}</strong></div>', unsafe_allow_html=True)
            elif status == 'JAUNE':
                st.markdown(f'<div class="status-card status-yellow">⚠️ <strong>{item}</strong></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-card status-red">🚨 <strong>{item}</strong></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 💰 Mes finances")
        
        # Détermination des statuts financiers
        prime_status = 'VERT' if kpis['prime_cost_pct'] < 60 else 'JAUNE' if kpis['prime_cost_pct'] < 65 else 'ROUGE'
        profit_status = 'VERT' if profit_margin >= 15 else 'JAUNE' if profit_margin >= 10 else 'ROUGE'
        
        food_cost_pct = (df_sales['food_cost'].tail(30).sum() / df_sales['revenue'].tail(30).sum() * 100)
        food_cost_status = 'VERT' if food_cost_pct < 32 else 'JAUNE'
        
        labor_cost_pct = (df_staff['monthly_cost'].sum() / df_sales['revenue'].tail(30).sum() * 100)
        labor_cost_status = 'VERT' if labor_cost_pct < 35 else 'JAUNE'
        
        finances_status = {
            f'Coût principal ({kpis["prime_cost_pct"]:.1f}%)': prime_status,
            f'Marge nette ({profit_margin:.1f}%)': profit_status,
            f'Coût nourriture ({food_cost_pct:.1f}%)': food_cost_status,
            f'Coût main d\'œuvre ({labor_cost_pct:.1f}%)': labor_cost_status
        }
        
        for item, status in finances_status.items():
            if status == 'VERT':
                st.markdown(f'<div class="status-card status-green">✅ <strong>{item}</strong></div>', unsafe_allow_html=True)
            elif status == 'JAUNE':
                st.markdown(f'<div class="status-card status-yellow">⚠️ <strong>{item}</strong></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-card status-red">🚨 <strong>{item}</strong></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Métriques simplifiées
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔄 Rotation des tables")
        st.metric("Service midi", f"{kpis['lunch_turns']:.1f}x", "Cible: 1.5-2x")
        st.metric("Service soir", f"{kpis['dinner_turns']:.1f}x", "Cible: 1.8-2.5x")
    
    with col2:
        st.markdown("#### 💺 Seuil de rentabilité")
        st.metric("Couverts nécessaires/jour", f"{kpis['break_even_covers']:.0f}")
        st.caption("Nombre de clients minimum pour couvrir les coûts")
    
    with col3:
        st.markdown("#### 📊 Cette semaine")
        week_revenue = df_sales['revenue'].tail(7).sum()
        prev_week = df_sales['revenue'].tail(14).head(7).sum()
        change = ((week_revenue - prev_week) / prev_week * 100) if prev_week > 0 else 0
        st.metric("Revenus (7j)", f"{week_revenue:,.0f}$", f"{change:+.1f}%")
        
        week_profit = df_sales['gross_profit'].tail(7).sum()
        st.metric("Profit (7j)", f"{week_profit:,.0f}$", f"{change:+.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Actions prioritaires cette semaine")
        
        actions = []
        
        # Actions basées sur les KPIs
        if kpis['prime_cost_pct'] > 60:
            actions.append("🔴 **URGENT**: Prime Cost à {:.1f}% - Réduire coûts nourriture ou main d'œuvre".format(kpis['prime_cost_pct']))
        
        if kpis['lunch_turns'] < 1.5:
            actions.append("🟡 Rotation midi faible ({:.1f}x) - Accélérer le service ou promotions lunch".format(kpis['lunch_turns']))
        
        if kpis['seat_occupancy'] < 65:
            actions.append("🟡 Taux occupation bas ({:.1f}%) - Renforcer marketing et réservations".format(kpis['seat_occupancy']))
        
        # Identifier les plats peu performants
        low_performers = df_menu[df_menu['qty'] < df_menu['qty'].quantile(0.3)]
        if len(low_performers) > 0:
            actions.append(f"📋 Revoir {len(low_performers)} plats peu vendus: {', '.join(low_performers['name'].head(2).tolist())}")
        
        # Identifier les plats à faible marge
        low_margin = df_menu[df_menu['margin'] < 60]
        if len(low_margin) > 0:
            actions.append(f"💰 Améliorer marge de: {', '.join(low_margin['name'].head(2).tolist())}")
        
        actions.append("✅ Réviser planning personnel semaine prochaine")
        actions.append("✅ Vérifier inventaire produits frais")
        
        for action in actions:
            st.markdown(f"- {action}")
    
    with col2:
        st.markdown("### 💡 Opportunités identifiées")
        
        opportunities = []
        
        # Opportunités basées sur les données
        best_dish = df_menu.loc[df_menu['revenue'].idxmax()]
        opportunities.append(f"⭐ **{best_dish['name']}** cartonne! Considérer une variation ou augmenter le prix de 1-2$")
        
        high_margin_dishes = df_menu[df_menu['margin'] > 70].sort_values('qty', ascending=False)
        if len(high_margin_dishes) > 0:
            top_margin = high_margin_dishes.iloc[0]
            opportunities.append(f"💎 Promouvoir **{top_margin['name']}** (marge {top_margin['margin']:.0f}%) - potentiel +{top_margin['revenue']*0.2:.0f}$/mois")
        
        # Heures creuses
        slow_hours = df_hourly[df_hourly['covers'] < 20]
        if len(slow_hours) > 0:
            opportunities.append(f"⏰ {len(slow_hours)} périodes creuses - Lancer happy hour ou promotions")
        
        if kpis['dinner_turns'] > 2.0:
            opportunities.append("🎉 Excellente rotation soir! Possibilité d'augmenter capacité ou prix")
        
        opportunities.append("📱 Lancer campagne réseaux sociaux pour lundi-mardi")
        opportunities.append("🎁 Programme fidélité pourrait augmenter revenus de 8-12%")
        
        for opp in opportunities:
            st.markdown(f"- {opp}")

# TAB 2: Suivi des opérations
with tab2:
    st.markdown(f"### Suivi des opérations - **{period_choice}**")
    
    st.markdown("""
    <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0;'>
        <strong>Légende:</strong> 
        <span style='color: #10b981;'>🟢 VERT</span> – Tout va bien / 
        <span style='color: #f59e0b;'>🟡 JAUNE</span> – Opportunité d'optimisation / 
        <span style='color: #ef4444;'>🔴 ROUGE</span> – Attention requise
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total couverts prévus demain",
            "440",
            "+38% vs moyenne"
        )
    
    with col2:
        st.metric(
            "Heure de pointe",
            "21h",
            "96 couverts"
        )
    
    with col3:
        st.metric(
            "Revenus estimés",
            "22,880 $",
            "Ticket moyen: 52$"
        )
    
    st.markdown("---")
    
    # Statut
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Points forts cette semaine**
        - Weekend exceptionnel: +38% vs moyenne
        - Ticket moyen en hausse constante
        - Taux de rotation optimal (1.8 couverts/table)
        - Marge brute à 68% (excellent)
        """)
    
    with col2:
        st.warning("""
        **⚠️ Points d'attention**
        - Lundi-mardi sous-performent (+15%)
        - Coûts alimentaires en légère hausse (+3%)
        - Temps d'attente moyen augmenté (18 min)
        - 2 plats peu performants à revoir
        """)
    
    st.markdown("---")
    
    # Prévision prochaine journée
    st.markdown("#### 📊 Prévision pour la prochaine journée (par heure)")
    
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
    
    st.markdown("---")
    
    # Alertes et recommandations prédictives
    st.markdown("#### 🔔 Alertes et recommandations prédictives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        **🚨 Alerte: Forte affluence prévue**
        - Date: Vendredi 25 octobre
        - Couverts estimés: 420 (+45% vs moyenne)
        - **Actions recommandées:**
            - Ajouter 2 serveurs (18h-22h)
            - Commander +30% poulet et pâtes
            - Préparer sauces à l'avance
        """)
    
    with col2:
        st.warning("""
        **☁️ Impact météo détecté**
        - Prévision: Pluie mardi prochain
        - Impact attendu: -15% dine-in, +25% livraison
        - **Actions recommandées:**
            - Augmenter stock plats à emporter
            - Renforcer équipe livraison
            - Promotion "Comfort food" spéciale
        """)
    
    st.markdown("---")
    
    # Sections supplémentaires
    st.markdown("#### 📦 Inventaire")
    st.info("Voir la section **Analyses > Inventaires** pour plus de détails")
    
    st.markdown("#### 🍽️ Performance du menu")
    st.info("Voir la section **Analyses > Performance du menu** pour plus de détails")
    
    st.markdown("#### 👥 Effectifs")
    st.info("Voir la section **Suivi des coûts et revenus > Coûts de main d'œuvre** pour plus de détails")

# TAB 3: Analyses
with tab3:
    st.subheader("Analyses détaillées")
    
    analysis_tabs = st.tabs([
        "🍕 Performance du menu",
        "👥 Effectifs",
        "📦 Inventaires",
        "👤 Clients"
    ])
    
    # SOUS-TAB 1: Performance du menu
    with analysis_tabs[0]:
        st.markdown("#### 📊 Analyse de la performance du menu")
        
        # Calcul des seuils pour la classification
        avg_qty = df_menu['qty'].mean()
        avg_margin_pct = df_menu['margin'].mean()
        
        # Classification des plats en français
        df_menu['classification'] = df_menu.apply(
            lambda row: 'Vedette' if row['qty'] >= avg_qty and row['margin'] >= avg_margin_pct
            else 'Populaire' if row['qty'] >= avg_qty and row['margin'] < avg_margin_pct
            else 'Potentiel' if row['qty'] < avg_qty and row['margin'] >= avg_margin_pct
            else 'À revoir',
            axis=1
        )
        
        # Classification des plats
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📋 Tous les plats")
            
            # Calcul de métriques supplémentaires
            df_menu_display = df_menu.copy()
            df_menu_display['contribution_margin'] = df_menu_display['revenue'] * (df_menu_display['margin'] / 100)
            df_menu_display['revenue_per_unit'] = df_menu_display['revenue'] / df_menu_display['qty']
            
            # Préparer le tableau simplifié
            display_df = df_menu_display[['name', 'category', 'qty', 'price', 'margin', 'revenue', 'classification']].copy()
            display_df.columns = ['Plat', 'Catégorie', 'Vendus', 'Prix', 'Marge %', 'Revenus', 'Classe']
            display_df['Prix'] = display_df['Prix'].apply(lambda x: f"{x:.2f}$")
            display_df['Revenus'] = display_df['Revenus'].apply(lambda x: f"{x:,.0f}$")
            
            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Marge %": st.column_config.ProgressColumn(
                        "Marge %",
                        format="%.0f%%",
                        min_value=0,
                        max_value=100,
                    )
                }
            )
        
        with col2:
            st.markdown("#### 📊 Classification")
            
            for classification in ['Vedette', 'Populaire', 'Potentiel', 'À revoir']:
                df_class = df_menu[df_menu['classification'] == classification]
                
                if classification == 'Vedette':
                    icon = "⭐"
                    desc = "Haute popularité + Haute marge"
                    action = "✅ Maintenir qualité"
                    color = "success"
                elif classification == 'Populaire':
                    icon = "👥"
                    desc = "Haute popularité + Faible marge"
                    action = "💰 Augmenter prix légèrement"
                    color = "info"
                elif classification == 'Potentiel':
                    icon = "💎"
                    desc = "Faible popularité + Haute marge"
                    action = "📣 Promouvoir activement"
                    color = "warning"
                else:
                    icon = "⚠️"
                    desc = "Faible popularité + Faible marge"
                    action = "🗑️ Retirer ou reformuler"
                    color = "danger"
                
                if len(df_class) > 0:
                    if color == "success":
                        st.success(f"**{icon} {classification}** ({len(df_class)})")
                    elif color == "warning":
                        st.warning(f"**{icon} {classification}** ({len(df_class)})")
                    elif color == "danger":
                        st.error(f"**{icon} {classification}** ({len(df_class)})")
                    else:
                        st.info(f"**{icon} {classification}** ({len(df_class)})")
                    
                    st.caption(desc)
                    st.caption(f"➡️ {action}")
                    
                    for _, item in df_class.iterrows():
                        st.caption(f"• {item['name']}")
                    
                    st.markdown("---")
        
        st.markdown("---")
        
        # Analyse par catégorie
        st.markdown("#### 📂 Performance par catégorie")
        
        category_stats = df_menu.groupby('category').agg({
            'qty': 'sum',
            'revenue': 'sum',
            'margin': 'mean'
        }).round(1)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=category_stats.index,
            y=category_stats['revenue'],
            name='Revenus',
            marker_color=COLORS['primary'],
            text=category_stats['revenue'].apply(lambda x: f"{x:,.0f}$"),
            textposition='outside'
        ))
        
        fig.update_layout(
            height=300,
            yaxis_title="Revenus ($)",
            xaxis_title="Catégorie",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            vedettes = df_menu[df_menu['classification'] == 'Vedette']
            st.success(f"""
            **⭐ Vedettes ({len(vedettes)} plats)**
            
            Vos champions à conserver!
            """)
            for _, item in vedettes.iterrows():
                st.caption(f"✅ {item['name']} - {item['qty']} vendus")
        
        with col2:
            potentiels = df_menu[df_menu['classification'] == 'Potentiel']
            a_revoir = df_menu[df_menu['classification'] == 'À revoir']
            
            st.warning(f"""
            **⚠️ À optimiser ({len(potentiels) + len(a_revoir)} plats)**
            """)
            
            if len(potentiels) > 0:
                st.caption("**Potentiels (haute marge):**")
                for _, item in potentiels.iterrows():
                    st.caption(f"📣 {item['name']} - À promouvoir!")
            
            if len(a_revoir) > 0:
                st.caption("**À revoir (faible performance):**")
                for _, item in a_revoir.iterrows():
                    st.caption(f"🗑️ {item['name']} - Retirer/revoir")
        
        with col3:
            populaires = df_menu[df_menu['classification'] == 'Populaire']
            
            st.info(f"""
            **💡 Opportunités ({len(populaires)} plats)**
            """)
            
            if len(populaires) > 0:
                st.caption("**Populaires (augmenter prix):**")
                for _, item in populaires.iterrows():
                    potential_increase = item['price'] * 0.10  # Augmentation 10%
                    monthly_potential = item['qty'] * potential_increase
                    st.caption(f"💰 {item['name']}")
                    st.caption(f"   → +{potential_increase:.2f}$ = +{monthly_potential:,.0f}$/mois")
            
            # Potentiel total
            total_potential = 0
            for _, item in populaires.iterrows():
                total_potential += item['qty'] * item['price'] * 0.10
            
            if total_potential > 0:
                st.metric("Potentiel total", f"+{total_potential:,.0f}$/mois")
    
    # SOUS-TAB 2: Effectifs
    with analysis_tabs[1]:
        st.markdown("#### Planification des effectifs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Répartition des coûts de personnel")
            
            fig = go.Figure(data=[go.Pie(
                labels=df_staff['position'],
                values=df_staff['monthly_cost'],
                hole=0.4,
                marker_colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success'], COLORS['warning'], COLORS['text']]
            )])
            
            fig.update_layout(
                height=400,
                font=dict(family='Inter', size=11)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Détail par poste")
            
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
            **✅ Périodes bien staffées**
            - Vendredi-Samedi soir (18h-21h)
            - Dimanche midi (11h-14h)
            - Mercredi midi (12h-13h30)
            
            **Taux de couverture: 95%**
            """)
            
            st.info("""
            **💡 Recommandations d'économies**
            - Réduire 1 serveur lundi-mardi 14h-17h
            - **Économie estimée: 1,920$/mois**
            - Impact service: Minimal (affluence faible)
            """)
        
        with col2:
            st.warning("""
            **⚠️ Périodes sous-staffées**
            - Jeudi soir (19h-21h)
            - Samedi midi (12h-14h)
            
            **Impact:** Temps d'attente +15 min
            **Satisfaction:** -0.3 points
            """)
            
            st.error("""
            **🚨 Action requise**
            - Ajouter 1 serveur jeudi 18h-22h
            - Ajouter 1 aide-cuisine samedi 11h-15h
            - **Coût: 1,280$/mois**
            - **ROI: +2,400$/mois** (meilleur service)
            """)
    
    # SOUS-TAB 3: Inventaires
    with analysis_tabs[2]:
        st.markdown("#### Gestion des stocks")
        
        st.info("""
        **📦 Gestion des inventaires**
        
        Cette section permet de suivre:
        - Niveaux de stock en temps réel
        - Alertes de réapprovisionnement
        - Analyse du gaspillage
        - Optimisation des commandes
        
        *Fonctionnalité en développement*
        """)
    
    # SOUS-TAB 4: Clients
    with analysis_tabs[3]:
        st.markdown("#### Comportement des clients")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Livraison", "35%", "+5%")
        
        with col2:
            st.metric("Bar", "15%", "-2%")
        
        with col3:
            st.metric("Salle", "50%", "-3%")
        
        st.markdown("---")
        
        st.markdown("##### Temps de service moyen")
        
        st.metric("Temps moyen", "18 minutes", "+3 min vs mois dernier")
        
        st.warning("""
        **⚠️ Attention:** Le temps de service a augmenté. 
        Considérer l'ajout de personnel aux heures de pointe.
        """)
        
        st.markdown("---")
        
        st.markdown("##### Efficacité du Marketing")
        
        st.info("""
        **📱 Efficacité du Marketing**
        
        Analyse des campagnes:
        - Réseaux sociaux: ROI de 3.2x
        - Email marketing: Taux d'ouverture 28%
        - Promotions: Impact moyen +15% revenus
        
        *Données synchronisées avec vos outils marketing*
        """)

# TAB 4: Suivi des coûts et revenus
with tab4:
    st.subheader("Suivi des coûts et revenus")
    
    finance_tabs = st.tabs([
        "💰 Profitabilité",
        "📈 Revenus",
        "💸 Coûts"
    ])
    
    # SOUS-TAB 1: Profitabilité
    with finance_tabs[0]:
        st.markdown("#### Vue d'ensemble de la profitabilité")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Répartition revenus vs coûts")
            
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
        
        with col2:
            st.markdown("##### Performance financière")
            
            st.success("""
            **💰 Indicateurs clés**
            - Marge brute: **68%** ✅
            - Coût nourriture: **28%** ✅
            - Coût personnel: **32%** ✅
            - Autres coûts: **12%** ✅
            """)
            
            st.markdown("---")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("Marge brute", "68%", "+2%")
            
            with col_b:
                st.metric("Coût total", "32%", "-1%")
    
    # SOUS-TAB 2: Revenus
    with finance_tabs[1]:
        st.markdown("#### 📊 Prévisions de revenus (30 prochains jours)")
        
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
        
        col1, col2, col3 = st.columns(3)
        
        predicted_total = df_forecast['predicted_revenue'].sum()
        
        with col1:
            st.metric(
                "Revenus prévus (30j)",
                f"{predicted_total:,.0f} $",
                "+15.2%"
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
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            yaxis=dict(title="Revenus ($)"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=11)
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title="Semaine")
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # SOUS-TAB 3: Coûts
    with finance_tabs[2]:
        st.markdown("#### Coûts de main d'œuvre")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("##### Répartition des coûts")
            
            fig = go.Figure(data=[go.Pie(
                labels=df_staff['position'],
                values=df_staff['monthly_cost'],
                hole=0.4,
                marker_colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success'], COLORS['warning'], COLORS['text']]
            )])
            
            fig.update_layout(
                height=350,
                font=dict(family='Inter', size=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Analyse des coûts")
            
            st.info("""
            **📊 Ratio coûts vs revenus**
            
            - Heures de pointe (18h-21h): Ratio optimal 1:3.2
            - Heures creuses (14h-17h): Ratio élevé 1:1.8
            
            **Efficacité de la planification: 85%**
            """)
            
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns(4)
            
            total_staff_cost = df_staff['monthly_cost'].sum()
            
            with col1:
                st.metric("Coût total", f"{total_staff_cost:,.0f}$/mois", "-2.3%")
            
            with col2:
                labor_pct = (total_staff_cost / df_sales['revenue'].tail(30).sum() * 100)
                st.metric("% Coût travail", f"{labor_pct:.1f}%", "Cible: 30-35%")
            
            with col3:
                st.metric("Taux rotation", "12%/an", "-3%")
            
            with col4:
                st.metric("Productivité", "1,847$/employé", "+5.2%")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: {COLORS['text']}; padding: 2rem; font-size: 0.9rem;'>
    <p style='margin: 0; font-weight: 500;'>Optimisation+ | Plateforme BI Restaurant</p>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.7;'>Données mises à jour en temps réel © 2025</p>
</div>
""", unsafe_allow_html=True)
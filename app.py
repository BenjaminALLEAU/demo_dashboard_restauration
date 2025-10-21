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
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .insight-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Génération de données fictives réalistes
@st.cache_data
def generate_data():
    # Dates
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    
    # Données de ventes
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
    
    # Données par heure
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
    
    # Menu items
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
    
    # Données de prévisions
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
    
    # Données de staff
    staff_data = {
        'position': ['Serveurs', 'Cuisiniers', 'Aide-cuisine', 'Bar', 'Management'],
        'headcount': [12, 8, 5, 3, 2],
        'avg_hourly_rate': [16, 22, 15, 18, 35],
        'monthly_hours': [1800, 1600, 1200, 900, 640]
    }
    df_staff = pd.DataFrame(staff_data)
    df_staff['monthly_cost'] = df_staff['avg_hourly_rate'] * df_staff['monthly_hours']
    
    return df_sales, df_hourly, df_menu, df_forecast, df_staff

# Chargement des données
df_sales, df_hourly, df_menu, df_forecast, df_staff = generate_data()

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=Optimisation%2B", use_container_width=True)
    st.markdown("---")
    
    st.subheader("📅 Période d'analyse")
    period = st.selectbox(
        "Sélectionnez la période",
        ["7 derniers jours", "30 derniers jours", "90 derniers jours", "Année en cours"]
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
    st.subheader("🎯 Filtres avancés")
    
    selected_days = st.multiselect(
        "Jours de la semaine",
        options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        default=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    
    if selected_days:
        df_filtered = df_filtered[df_filtered['day_of_week'].isin(selected_days)]
    
    st.markdown("---")
    st.info("💡 **Astuce**: Utilisez les filtres pour analyser des périodes spécifiques et identifier les tendances.")

# Header
st.markdown('<div class="main-header">🍽️ Optimisation+ | Business Intelligence Restaurant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Tableau de bord analytique alimenté par l\'IA pour maximiser la rentabilité</div>', unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble", 
    "💰 Analyse des ventes", 
    "🍕 Performance menu",
    "🔮 Prévisions IA",
    "👥 Gestion du personnel"
])

# TAB 1: Vue d'ensemble
with tab1:
    # KPIs principaux
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_revenue = df_filtered['revenue'].sum()
    total_covers = df_filtered['covers'].sum()
    avg_ticket = df_filtered['avg_ticket'].mean()
    
    # Comparaison période précédente
    prev_period = df_sales.tail(days * 2).head(days)
    prev_revenue = prev_period['revenue'].sum()
    revenue_change = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    with col1:
        st.metric(
            "Chiffre d'affaires",
            f"{total_revenue:,.0f}$",
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
            f"{avg_ticket:.2f}$",
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
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution du chiffre d'affaires")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['revenue'],
            mode='lines',
            name='Revenus',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        # Moyenne mobile
        df_filtered['ma7'] = df_filtered['revenue'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['ma7'],
            mode='lines',
            name='Moyenne mobile (7j)',
            line=dict(color='#f59e0b', width=2, dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⏰ Affluence par heure")
        
        fig = go.Figure()
        
        colors = ['#10b981' if x > 60 else '#f59e0b' if x > 30 else '#3b82f6' 
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
            yaxis_title="Nombre de couverts"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Insights IA
    st.subheader("🤖 Insights IA - Recommandations prioritaires")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
            <h4>💡 Opportunité détectée</h4>
            <p><strong>Jeudi soir sous-optimisé</strong></p>
            <p>Taux d'occupation: 48% vs 75% en moyenne</p>
            <p>💰 Potentiel: <strong>+2,400$/mois</strong></p>
            <p>✅ Action: Promotion "Soirée duo" jeudi 18h-21h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Alerte gaspillage</h4>
            <p><strong>Saumon Atlantique</strong></p>
            <p>Taux de perte: 18% (cible: <10%)</p>
            <p>💰 Économie: <strong>780$/mois</strong></p>
            <p>✅ Action: Réduire commandes de 25% lun-mar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="success-box">
            <h4>🎯 Performance exceptionnelle</h4>
            <p><strong>Pâtes Carbonara</strong></p>
            <p>Marge: 72% | Popularité: #1</p>
            <p>💰 Impact: <strong>+3-5% marge globale</strong></p>
            <p>✅ Action: Mise en vedette dans menu</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Analyse des ventes
with tab2:
    st.subheader("💰 Analyse approfondie des ventes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📊 Revenus par jour de la semaine")
        
        # Agrégation par jour de semaine
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
            marker_color='#667eea',
            text=[f"{x:.0f}$" for x in weekly_data['revenue']],
            textposition='outside'
        ))
        
        fig.update_layout(height=400, showlegend=False, yaxis_title="Revenus moyens")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Répartition des revenus")
        
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
            marker_colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
        )])
        
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Analyse comparative
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📉 Top 5 jours les plus rentables")
        top_days = df_sales.nlargest(5, 'revenue')[['date', 'revenue', 'covers']]
        top_days['date'] = top_days['date'].dt.strftime('%d/%m/%Y')
        top_days['revenue'] = top_days['revenue'].apply(lambda x: f"{x:,.0f}$")
        st.dataframe(top_days, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Tendances mensuelles")
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
    st.subheader("🍕 Analyse de performance du menu")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 📊 Top plats - Volume & Rentabilité")
        
        # Matrice BCG simplifiée
        fig = go.Figure()
        
        for idx, row in df_menu.iterrows():
            size = row['revenue'] / 100
            color = '#10b981' if row['margin'] > 70 else '#f59e0b' if row['margin'] > 60 else '#ef4444'
            
            fig.add_trace(go.Scatter(
                x=[row['qty']],
                y=[row['margin']],
                mode='markers+text',
                marker=dict(size=size, color=color, opacity=0.6),
                text=row['name'],
                textposition='top center',
                name=row['name'],
                hovertemplate=f"<b>{row['name']}</b><br>" +
                             f"Quantité: {row['qty']}<br>" +
                             f"Revenus: {row['revenue']}$<br>" +
                             f"Marge: {row['margin']}%<extra></extra>"
            ))
        
        fig.update_layout(
            height=500,
            xaxis_title="Volume de ventes",
            yaxis_title="Marge (%)",
            showlegend=False,
            hovermode='closest'
        )
        
        # Lignes de référence
        fig.add_hline(y=65, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=df_menu['qty'].median(), line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏆 Classement des plats")
        
        # Calcul du score performance
        df_menu['score'] = (df_menu['qty'] / df_menu['qty'].max() * 50 + 
                           df_menu['margin'] / 100 * 50)
        df_menu_sorted = df_menu.sort_values('score', ascending=False)
        
        for idx, row in df_menu_sorted.iterrows():
            color = "green" if row['score'] > 75 else "orange" if row['score'] > 60 else "red"
            st.markdown(f"""
            **{row['name']}**  
            Score: {row['score']:.0f}/100 | Marge: {row['margin']}% | Ventes: {row['qty']}  
            :{color}[{'█' * int(row['score']/10)}]
            """)
            st.markdown("---")
    
    st.markdown("---")
    
    # Recommandations menu
    st.markdown("#### 💡 Recommandations d'optimisation du menu")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        **⭐ Stars (à promouvoir)**
        - Pâtes Carbonara (72% marge)
        - Pizza Margherita (75% marge)
        - Salade César (78% marge)
        
        Action: Mise en avant visuelle dans le menu
        """)
    
    with col2:
        st.warning("""
        **🔧 À optimiser**
        - Saumon Atlantique (52% marge, gaspillage élevé)
        - Steak-Frites (55% marge)
        
        Action: Renégocier fournisseurs ou ajuster prix
        """)
    
    with col3:
        st.info("""
        **🆕 Opportunités**
        - Ajouter plats végétariens (+25% demande)
        - Menu saisonnier (automne)
        - Formules midi attractives
        
        Action: Test A/B sur 2 semaines
        """)

# TAB 4: Prévisions IA
with tab4:
    st.subheader("🔮 Prévisions intelligentes alimentées par l'IA")
    
    # Graphique de prévisions
    st.markdown("#### 📈 Prévision des revenus - 30 prochains jours")
    
    fig = go.Figure()
    
    # Données historiques
    fig.add_trace(go.Scatter(
        x=df_sales.tail(30)['date'],
        y=df_sales.tail(30)['revenue'],
        mode='lines',
        name='Historique',
        line=dict(color='#667eea', width=3)
    ))
    
    # Prévisions
    fig.add_trace(go.Scatter(
        x=df_forecast['date'],
        y=df_forecast['predicted_revenue'],
        mode='lines',
        name='Prévisions IA',
        line=dict(color='#10b981', width=3, dash='dash')
    ))
    
    # Intervalle de confiance
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
        yaxis_title="Revenus ($)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métriques de prévision
    col1, col2, col3, col4 = st.columns(4)
    
    predicted_total = df_forecast['predicted_revenue'].sum()
    
    with col1:
        st.metric(
            "Revenus prévus (30j)",
            f"{predicted_total:,.0f}$",
            f"+15.2% vs période équivalente"
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
            f"{best_day['predicted_revenue']:.0f}$"
        )
    
    with col4:
        st.metric(
            "Économies identifiées",
            "3,840$/mois",
            "Grâce aux prévisions"
        )
    
    st.markdown("---")
    
    # Facteurs d'influence
    st.markdown("#### 🌡️ Facteurs d'influence détectés par l'IA")
    
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
            fillcolor='rgba(102, 126, 234, 0.2)',
            line=dict(color='#667eea', width=3)
        ))
        
        fig.update_layout(
            height=400,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 40])
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### 📊 Impact sur revenus")
        for factor, impact in sorted(factors.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"**{factor}**")
            st.progress(impact / 40)
            st.caption(f"±{impact}% d'impact")
    
    st.markdown("---")
    
    # Alertes prédictives
    st.markdown("#### ⚠️ Alertes et recommandations prédictives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        **🚨 Alerte: Forte affluence prévue**
        - **Date**: Vendredi 25 octobre
        - **Couverts estimés**: 420 (+45% vs moyenne)
        - **Actions recommandées**:
            - Ajouter 2 serveurs (18h-22h)
            - Commander +30% poulet et pâtes
            - Préparer sauces à l'avance
        """)
    
    with col2:
        st.warning("""
        **☔ Impact météo détecté**
        - **Prévision**: Pluie mardi prochain
        - **Impact attendu**: -15% dine-in, +25% livraison
        - **Actions recommandées**:
            - Augmenter stock plats à emporter
            - Renforcer équipe livraison
            - Promotion "Comfort food" spéciale
        """)

# TAB 5: Gestion personnel
with tab5:
    st.subheader("👥 Analyse et optimisation du personnel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💼 Répartition des coûts de personnel")
        
        fig = go.Figure(data=[go.Pie(
            labels=df_staff['position'],
            values=df_staff['monthly_cost'],
            hole=0.4,
            marker_colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
        )])
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Détail par poste")
        
        display_df = df_staff[['position', 'headcount', 'avg_hourly_rate', 'monthly_cost']].copy()
        display_df.columns = ['Poste', 'Effectif', 'Taux horaire', 'Coût mensuel']
        display_df['Taux horaire'] = display_df['Taux horaire'].apply(lambda x: f"{x}$/h")
        display_df['Coût mensuel'] = display_df['Coût mensuel'].apply(lambda x: f"{x:,.0f}$")
        
        st.dataframe(display_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Métriques RH
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
    
    # Optimisation horaires
    st.markdown("#### ⏰ Optimisation des horaires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Périodes bien staffées**
        - Vendredi-Samedi soir (18h-21h)
        - Dimanche midi (11h-14h)
        - Mercredi midi (12h-13h30)
        
        Taux de couverture: 95%
        """)
        
        st.info("""
        **💡 Recommandations d'économies**
        - Réduire 1 serveur lundi-mardi 14h-17h
        - Économie estimée: **1,920$/mois**
        - Impact service: Minimal (affluence faible)
        """)
    
    with col2:
        st.warning("""
        **⚠️ Périodes sous-staffées**
        - Jeudi soir (19h-21h)
        - Samedi midi (12h-14h)
        
        Impact: Temps d'attente +15 min
        Satisfaction: -0.3 points
        """)
        
        st.error("""
        **🚨 Action requise**
        - Ajouter 1 serveur jeudi 18h-22h
        - Ajouter 1 aide-cuisine samedi 11h-15h
        - Coût: **1,280$/mois**
        - ROI: +2,400$/mois (meilleur service)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem;'>
    <p><strong>Optimisation+</strong> | Plateforme BI alimentée par l'IA</p>
    <p>© 2025 - Tous droits réservés | Données mises à jour en temps réel</p>
    <p style='font-size: 0.9rem;'>💡 Pour une démo personnalisée, contactez notre équipe</p>
</div>
""", unsafe_allow_html=True)

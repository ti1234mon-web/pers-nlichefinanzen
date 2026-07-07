# ============================================================
# PERSÖNLICHER JAHRESABSCHLUSS – CFO DASHBOARD
# 3 TABS: GUV (Eingabe), BILANZ (Eingabe), DASHBOARD (Übersicht + Handlungsempfehlung)
# STREAMLIT, SQLITE, DARK LUXURY
# ============================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta

# ============================================================
# 1. SEITENKONFIGURATION
# ============================================================

st.set_page_config(page_title="Persönlicher Jahresabschluss", layout="wide")

# ============================================================
# 2. CSS – DARK LUXURY
# ============================================================

def render_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        .stApp { background: linear-gradient(160deg, #0A0A0A 0%, #1A1A1A 35%, #222222 65%, #0A0A0A 100%); min-height: 100vh; }
        .stApp::before { content: ''; position: fixed; top: -20%; left: -20%; width: 140%; height: 140%; background: radial-gradient(ellipse at 40% 30%, rgba(212, 168, 83, 0.03) 0%, transparent 60%); pointer-events: none; z-index: 0; }
        .main > div { background: transparent; max-width: 1200px; margin: 0 auto; padding: 1rem 2rem 4rem 2rem; position: relative; z-index: 1; }
        .block-container { padding-top: 0.5rem; padding-bottom: 4rem; max-width: 1200px; margin: 0 auto; }
        .title-wrapper { display: flex; justify-content: center; width: 100%; margin: 1.5rem auto 2rem auto; }
        .main-title { font-size: 2.2rem; font-weight: 800; letter-spacing: 0.04em; text-align: center; margin: 0; color: #FFFFFF; line-height: 1.2; text-shadow: 0 2px 40px rgba(212, 168, 83, 0.05); }
        .main-title span { background: linear-gradient(135deg, #D4A853 0%, #F5D98E 50%, #D4A853 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .section-label { color: rgba(255, 255, 255, 0.35); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.8rem; }
        .metric-container { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 16px; padding: 1rem 1.2rem; text-align: center; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }
        .metric-label { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255, 255, 255, 0.3); margin-bottom: 0.2rem; }
        .metric-value { font-size: 1.4rem; font-weight: 700; color: #FFFFFF; }
        .metric-value.green { color: #4CAF50; }
        .metric-value.yellow { color: #FFC107; }
        .metric-value.red { color: #F44336; }
        .metric-value.gold { color: #D4A853; }
        .input-area { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; }
        .input-area .stTextInput input, .input-area .stNumberInput input, .input-area .stSelectbox div { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; border-radius: 8px !important; color: white !important; }
        .input-area .stButton button { background: linear-gradient(135deg, #D4A853 0%, #F5D98E 100%) !important; color: #0A0A0A !important; font-weight: 600 !important; border: none !important; border-radius: 8px !important; padding: 0.4rem 1.5rem !important; transition: all 0.3s ease !important; width: 100% !important; }
        .input-area .stButton button:hover { transform: scale(1.02); box-shadow: 0 4px 20px rgba(212, 168, 83, 0.3); }
        .input-label { color: rgba(255, 255, 255, 0.3); font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.2rem; }
        .kpi-bar { background: rgba(255, 255, 255, 0.03); border-radius: 8px; height: 8px; overflow: hidden; margin-top: 0.3rem; }
        .kpi-bar .fill { height: 100%; border-radius: 8px; transition: width 0.5s ease; }
        .kpi-row { display: flex; justify-content: space-between; align-items: center; padding: 0.3rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.02); }
        .kpi-label { color: rgba(255, 255, 255, 0.5); font-size: 0.8rem; }
        .kpi-value { font-weight: 600; font-size: 0.85rem; }
        .kpi-value.green { color: #4CAF50; }
        .kpi-value.yellow { color: #FFC107; }
        .kpi-value.red { color: #F44336; }
        .action-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; }
        .action-title { font-weight: 600; color: #D4A853; font-size: 0.9rem; }
        .action-detail { color: rgba(255, 255, 255, 0.6); font-size: 0.85rem; margin-top: 0.2rem; }
        .action-result { color: #4CAF50; font-size: 0.8rem; margin-top: 0.3rem; }
        .kpi-explanation { background: rgba(255, 255, 255, 0.02); border-left: 2px solid #D4A853; border-radius: 0 8px 8px 0; padding: 0.5rem 0.8rem; margin: 0.3rem 0; }
        .kpi-explanation .kpi-name { color: #D4A853; font-weight: 500; font-size: 0.8rem; }
        .kpi-explanation .kpi-desc { color: rgba(255, 255, 255, 0.4); font-size: 0.75rem; }
        .delete-btn { color: #F44336 !important; background: rgba(244, 67, 54, 0.1) !important; border: 1px solid rgba(244, 67, 54, 0.2) !important; border-radius: 6px !important; padding: 0.1rem 0.6rem !important; font-size: 0.6rem !important; cursor: pointer !important; transition: all 0.2s ease !important; }
        .delete-btn:hover { background: rgba(244, 67, 54, 0.2) !important; border-color: #F44336 !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: rgba(255, 255, 255, 0.02); border-radius: 12px; padding: 0.3rem; }
        .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; padding: 0.5rem 1.2rem; color: rgba(255, 255, 255, 0.3); font-weight: 500; font-size: 0.8rem; transition: all 0.3s ease; }
        .stTabs [data-baseweb="tab"][aria-selected="true"] { background: rgba(212, 168, 83, 0.1); color: #D4A853; border: 1px solid rgba(212, 168, 83, 0.2); }
        .stTabs [data-baseweb="tab"]:hover { color: rgba(255, 255, 255, 0.6); }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 3. DATENBANK-FUNKTIONEN
# ============================================================

DB_PATH = "finance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Transaktionen (GuV)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            type TEXT,
            amount REAL,
            description TEXT
        )
    ''')
    # Aktiva (Bilanz)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value REAL,
            asset_type TEXT
        )
    ''')
    # Passiva (Bilanz)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value REAL,
            liability_type TEXT
        )
    ''')
    # Einnahmen (monatlich – für GuV)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            amount REAL,
            income_type TEXT
        )
    ''')
    conn.commit()
    conn.close()
    add_defaults()

def add_defaults():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Einnahmen
    cursor.execute("SELECT COUNT(*) FROM income")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO income (name, amount, income_type) VALUES ('Gehalt', 3200, 'Angestellt')")
    # Aktiva
    cursor.execute("SELECT COUNT(*) FROM assets")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO assets (name, value, asset_type) VALUES ('Tagesgeld', 15000, 'Umlaufvermögen')")
        cursor.execute("INSERT INTO assets (name, value, asset_type) VALUES ('ETFs', 25000, 'Anlagevermögen')")
    # Passiva
    cursor.execute("SELECT COUNT(*) FROM liabilities")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO liabilities (name, value, liability_type) VALUES ('Kreditkarte', 1000, 'Kurzfristig')")
        cursor.execute("INSERT INTO liabilities (name, value, liability_type) VALUES ('Immobilienkredit', 250000, 'Langfristig')")
    conn.commit()
    conn.close()

# --- TRANSACTIONS (GuV) ---
def get_transactions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC", conn)
    conn.close()
    return df

def add_transaction(date, category, type, amount, description=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, category, type, amount, description) VALUES (?, ?, ?, ?, ?)",
                   (date, category, type, amount, description))
    conn.commit()
    conn.close()

def delete_transaction(tx_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    conn.close()

# --- INCOME ---
def get_income():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM income", conn)
    conn.close()
    return df

def add_income(name, amount, income_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO income (name, amount, income_type) VALUES (?, ?, ?)", (name, amount, income_type))
    conn.commit()
    conn.close()

def update_income(name, amount):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE income SET amount = ? WHERE name = ?", (amount, name))
    conn.commit()
    conn.close()

def delete_income(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM income WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# --- ASSETS ---
def get_assets():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM assets", conn)
    conn.close()
    return df

def add_asset(name, value, asset_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO assets (name, value, asset_type) VALUES (?, ?, ?)", (name, value, asset_type))
    conn.commit()
    conn.close()

def update_asset(name, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE assets SET value = ? WHERE name = ?", (value, name))
    conn.commit()
    conn.close()

def delete_asset(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assets WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# --- LIABILITIES ---
def get_liabilities():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM liabilities", conn)
    conn.close()
    return df

def add_liability(name, value, liability_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO liabilities (name, value, liability_type) VALUES (?, ?, ?)", (name, value, liability_type))
    conn.commit()
    conn.close()

def update_liability(name, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE liabilities SET value = ? WHERE name = ?", (value, name))
    conn.commit()
    conn.close()

def delete_liability(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM liabilities WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# ============================================================
# 4. BERECHNUNGEN (KPIs + Handlungsempfehlungen)
# ============================================================

def calculate_kpis():
    """Berechnet alle 7 KPIs."""
    df_income = get_income()
    total_income = df_income['amount'].sum() if not df_income.empty else 0
    
    df_tx = get_transactions()
    if not df_tx.empty:
        # Ausgaben nach Fix/Variabel kategorisieren
        fixed_categories = ['Miete', 'Versicherungen', 'Abos', 'Kredite']
        variable_categories = ['Lebensmittel', 'Transport', 'Freizeit', 'Sonstiges']
        
        df_expenses = df_tx[df_tx['type'] == 'Ausgabe']
        fixed_expenses = df_expenses[df_expenses['category'].isin(fixed_categories)]['amount'].sum()
        variable_expenses = df_expenses[~df_expenses['category'].isin(fixed_categories)]['amount'].sum()
        total_expenses = fixed_expenses + variable_expenses
    else:
        fixed_expenses = 0
        variable_expenses = 0
        total_expenses = 0
    
    df_assets = get_assets()
    current_assets = df_assets[df_assets['asset_type'] == 'Umlaufvermögen']['value'].sum()
    non_current_assets = df_assets[df_assets['asset_type'] == 'Anlagevermögen']['value'].sum()
    total_assets = current_assets + non_current_assets
    
    df_liabilities = get_liabilities()
    current_liabilities = df_liabilities[df_liabilities['liability_type'] == 'Kurzfristig']['value'].sum()
    non_current_liabilities = df_liabilities[df_liabilities['liability_type'] == 'Langfristig']['value'].sum()
    total_liabilities = current_liabilities + non_current_liabilities
    
    equity = total_assets - total_liabilities
    
    # Zinsen (Annahme: 5% von kurzfristigen Verbindlichkeiten + 2% von langfristigen)
    interest = (current_liabilities * 0.05) / 12 + (non_current_liabilities * 0.02) / 12
    
    # Cash Runway (nur Tagesgeld als Cash)
    cash = df_assets[df_assets['name'] == 'Tagesgeld']['value'].sum() if not df_assets.empty else 0
    cash_runway = cash / total_expenses if total_expenses > 0 else 0
    
    # Current Ratio
    current_ratio = current_assets / current_liabilities if current_liabilities > 0 else float('inf')
    
    # Profit Marge
    profit_marge = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
    
    # Zinsdeckungsgrad
    income_after_variable = total_income - variable_expenses
    interest_coverage = income_after_variable / interest if interest > 0 else float('inf')
    
    # Eigenkapitalquote
    equity_ratio = (equity / total_assets * 100) if total_assets > 0 else 0
    
    # Umlaufintensität
    current_assets_ratio = (current_assets / total_assets * 100) if total_assets > 0 else 0
    
    # Anlageintensität
    non_current_assets_ratio = (non_current_assets / total_assets * 100) if total_assets > 0 else 0
    
    # Zeit bis Ziel (vereinfacht)
    monthly_surplus = total_income - total_expenses
    # Monate bis 12 Monate Cash Runway
    if monthly_surplus > 0:
        months_to_12_cash = (12 * total_expenses - cash) / monthly_surplus if (12 * total_expenses - cash) > 0 else 0
    else:
        months_to_12_cash = float('inf')
    
    # Alle 7 KPIs
    kpis = {
        'cash_runway': cash_runway,
        'current_ratio': current_ratio,
        'profit_marge': profit_marge,
        'interest_coverage': interest_coverage,
        'equity_ratio': equity_ratio,
        'current_assets_ratio': current_assets_ratio,
        'non_current_assets_ratio': non_current_assets_ratio,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'fixed_expenses': fixed_expenses,
        'variable_expenses': variable_expenses,
        'monthly_surplus': monthly_surplus,
        'cash': cash,
        'current_assets': current_assets,
        'non_current_assets': non_current_assets,
        'current_liabilities': current_liabilities,
        'non_current_liabilities': non_current_liabilities,
        'equity': equity,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'months_to_12_cash': months_to_12_cash,
        'interest': interest,
        'income_after_variable': income_after_variable,
    }
    return kpis

def get_optimal_action(kpis):
    """Berechnet NUR die optimale Handlungsempfehlung."""
    actions = []
    
    # 1. Cash Runway
    if kpis['cash_runway'] < 12:
        needed_cash = (12 - kpis['cash_runway']) * kpis['total_expenses']
        if kpis['monthly_surplus'] > 0:
            months = needed_cash / kpis['monthly_surplus']
            action = {
                'priority': 1,
                'kpi': 'Cash Runway',
                'problem': f'{kpis["cash_runway"]:.1f} Monate (Ziel: 12)',
                'action': f'{needed_cash:.0f} € auf Tagesgeld sparen',
                'detail': f'Monate bis Ziel: {months:.0f} Monate bei {kpis["monthly_surplus"]:.0f} €/Monat',
                'result': f'Neuer Cash Runway: 12 Monate (optimal) ✅',
                'status': 'red'
            }
            actions.append(action)
    elif kpis['cash_runway'] > 12:
        excess_cash = (kpis['cash_runway'] - 12) * kpis['total_expenses']
        action = {
            'priority': 2,
            'kpi': 'Cash Runway',
            'problem': f'{kpis["cash_runway"]:.1f} Monate (Ziel: 12)',
            'action': f'{excess_cash:.0f} € in langfristige Anlagen investieren',
            'detail': 'Du hast mehr Cash als nötig – investiere den Überschuss',
            'result': f'Neuer Cash Runway: 12 Monate (optimal) ✅',
            'status': 'yellow'
        }
        actions.append(action)
    
    # 2. Current Ratio
    if kpis['current_ratio'] < 1.5:
        needed = (1.5 * kpis['current_liabilities']) - kpis['current_assets']
        if needed > 0:
            action = {
                'priority': 3,
                'kpi': 'Current Ratio',
                'problem': f'{kpis["current_ratio"]:.2f} (Ziel: 1,5-2,0)',
                'action': f'{needed:.0f} € Schulden tilgen oder Cash erhöhen',
                'detail': f'Current Ratio auf 1,5 bringen',
                'result': f'Neues Current Ratio: 1,5 (optimal) ✅',
                'status': 'red'
            }
            actions.append(action)
    elif kpis['current_ratio'] > 2.0:
        excess = kpis['current_assets'] - (2.0 * kpis['current_liabilities'])
        if excess > 0:
            action = {
                'priority': 4,
                'kpi': 'Current Ratio',
                'problem': f'{kpis["current_ratio"]:.2f} (Ziel: 1,5-2,0)',
                'action': f'{excess:.0f} € in langfristige Anlagen umschichten',
                'detail': 'Zu viel Cash im Verhältnis zu Schulden',
                'result': f'Neues Current Ratio: 2,0 (optimal) ✅',
                'status': 'yellow'
            }
            actions.append(action)
    
    # 3. Profit Marge
    if kpis['profit_marge'] < 20:
        needed = (0.20 * kpis['total_income']) - (kpis['total_income'] - kpis['total_expenses'])
        action = {
            'priority': 5,
            'kpi': 'Profit Marge',
            'problem': f'{kpis["profit_marge"]:.1f}% (Ziel: >20%)',
            'action': f'{needed:.0f} € variable Kosten senken',
            'detail': 'Fokus auf variable Kosten (Lebensmittel, Transport, Freizeit)',
            'result': f'Neue Profit Marge: 20% (optimal) ✅',
            'status': 'red'
        }
        actions.append(action)
    
    # 4. Zinsdeckungsgrad
    if kpis['interest_coverage'] < 1.5 and kpis['interest'] > 0:
        needed = (kpis['income_after_variable'] / 1.5) - kpis['interest']
        if needed > 0:
            action = {
                'priority': 6,
                'kpi': 'Zinsdeckungsgrad',
                'problem': f'{kpis["interest_coverage"]:.2f} (Ziel: >1,5)',
                'action': f'{needed:.0f} € Schulden tilgen oder umschulden',
                'detail': 'Zinslast senken oder Einkommen erhöhen',
                'result': f'Neuer Zinsdeckungsgrad: 1,5 (optimal) ✅',
                'status': 'red'
            }
            actions.append(action)
    
    # 5. Eigenkapitalquote
    if kpis['equity_ratio'] < 30:
        target_equity = 0.30 * kpis['total_assets']
        needed_equity = target_equity - kpis['equity']
        if needed_equity > 0 and kpis['monthly_surplus'] > 0:
            months = needed_equity / kpis['monthly_surplus']
            action = {
                'priority': 7,
                'kpi': 'Eigenkapitalquote',
                'problem': f'{kpis["equity_ratio"]:.1f}% (Ziel: >30%)',
                'action': f'{needed_equity:.0f} € in ETFs investieren',
                'detail': f'Monate bis Ziel: {months:.0f} Monate bei {kpis["monthly_surplus"]:.0f} €/Monat',
                'result': f'Neue Eigenkapitalquote: 30% (optimal) ✅',
                'status': 'yellow'
            }
            actions.append(action)
    
    # 6. Umlaufintensität
    if kpis['current_assets_ratio'] < 20:
        target = 0.25 * kpis['total_assets']  # Ziel Mitte
        needed = target - kpis['current_assets']
        if needed > 0:
            action = {
                'priority': 8,
                'kpi': 'Umlaufintensität',
                'problem': f'{kpis["current_assets_ratio"]:.1f}% (Ziel: 20-40%)',
                'action': f'{needed:.0f} € in Umlaufvermögen umschichten',
                'detail': 'ETFs/Aktien in Tagesgeld umschichten',
                'result': f'Neue Umlaufintensität: 25% (optimal) ✅',
                'status': 'yellow'
            }
            actions.append(action)
    elif kpis['current_assets_ratio'] > 40:
        excess = kpis['current_assets'] - (0.40 * kpis['total_assets'])
        if excess > 0:
            action = {
                'priority': 9,
                'kpi': 'Umlaufintensität',
                'problem': f'{kpis["current_assets_ratio"]:.1f}% (Ziel: 20-40%)',
                'action': f'{excess:.0f} € in langfristige Anlagen umschichten',
                'detail': 'Zu viel im Umlaufvermögen – langfristig anlegen',
                'result': f'Neue Umlaufintensität: 35% (optimal) ✅',
                'status': 'yellow'
            }
            actions.append(action)
    
    # Nach Priorität sortieren
    actions.sort(key=lambda x: x['priority'])
    return actions

# ============================================================
# 5. DASHBOARD UI
# ============================================================

def main():
    render_css()
    init_db()
    
    # Titel
    st.markdown("""
        <div class="title-wrapper">
            <h1 class="main-title">📊 PERSÖNLICHER <span>JAHRESABSCHLUSS</span></h1>
        </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # 5.1 TABS
    # ============================================================
    
    tab1, tab2, tab3 = st.tabs(["📊 GuV (Eingabe)", "📊 Bilanz (Eingabe)", "🏆 Dashboard (Übersicht)"])
    
    # ============================================================
    # TAB 1: GUV (Eingabe)
    # ============================================================
    
    with tab1:
        st.markdown('<p class="section-label">📝 Einnahmen & Ausgaben erfassen</p>', unsafe_allow_html=True)
        
        # Neue Transaktion
        with st.container():
            st.markdown('<div class="input-area">', unsafe_allow_html=True)
            st.markdown('<p style="color: rgba(255,255,255,0.3); font-size: 0.7rem; margin-bottom: 0.8rem;">➕ Neue Transaktion</p>', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns([1.2, 1.5, 1, 1.5, 0.8])
            with col1:
                date = st.date_input("Datum", value=datetime.today(), label_visibility="collapsed")
            with col2:
                category = st.selectbox("Kategorie", ["Miete", "Lebensmittel", "Transport", "Freizeit", "Versicherungen", "Abos", "Kredite", "Sonstiges", "Gehalt", "Nebeneinkünfte"], label_visibility="collapsed")
            with col3:
                tx_type = st.selectbox("Typ", ["Einnahme", "Ausgabe"], label_visibility="collapsed")
            with col4:
                amount = st.number_input("Betrag (€)", min_value=0.01, value=100.0, step=5.0, format="%.2f", label_visibility="collapsed")
            with col5:
                if st.button("💾 Speichern"):
                    add_transaction(str(date), category, tx_type, amount)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Alle Transaktionen
        df_tx = get_transactions()
        if not df_tx.empty:
            st.markdown('<p class="section-label">📋 Alle Transaktionen</p>', unsafe_allow_html=True)
            
            # Tabelle mit Lösch-Buttons
            for idx, row in df_tx.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([0.5, 1.2, 1.5, 1.2, 1.5, 0.5])
                with col1:
                    st.write(f"{idx + 1}")
                with col2:
                    st.write(row['date'])
                with col3:
                    st.write(row['category'])
                with col4:
                    color = "green" if row['type'] == "Einnahme" else "red"
                    st.markdown(f"<span style='color: {color};'>{row['type']}</span>", unsafe_allow_html=True)
                with col5:
                    color = "green" if row['type'] == "Einnahme" else "red"
                    st.markdown(f"<span style='color: {color}; font-weight: 600;'>{row['amount']:.2f} €</span>", unsafe_allow_html=True)
                with col6:
                    if st.button("🗑️", key=f"del_tx_{row['id']}"):
                        delete_transaction(row['id'])
                        st.rerun()
        else:
            st.info("📭 Noch keine Transaktionen erfasst.")
    
    # ============================================================
    # TAB 2: BILANZ (Eingabe)
    # ============================================================
    
    with tab2:
        st.markdown('<p class="section-label">📝 Aktiva & Passiva verwalten</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # AKTIVA
        with col1:
            st.markdown('<p style="color: #D4A853; font-size: 0.8rem; font-weight: 500; margin-bottom: 0.5rem;">🟢 Aktiva (Was du hast)</p>', unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="input-area" style="padding: 0.8rem 1rem;">', unsafe_allow_html=True)
                col_a, col_b, col_c, col_d = st.columns([1.5, 1.5, 1.2, 0.6])
                with col_a:
                    asset_name = st.text_input("Name", placeholder="z.B. Tagesgeld", label_visibility="collapsed", key="asset_name")
                with col_b:
                    asset_value = st.number_input("Wert (€)", min_value=0.0, value=1000.0, step=100.0, format="%.0f", label_visibility="collapsed", key="asset_value")
                with col_c:
                    asset_type = st.selectbox("Typ", ["Umlaufvermögen", "Anlagevermögen"], label_visibility="collapsed", key="asset_type")
                with col_d:
                    if st.button("➕", key="add_asset"):
                        if asset_name.strip():
                            add_asset(asset_name.strip(), asset_value, asset_type)
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            df_assets = get_assets()
            if not df_assets.empty:
                for idx, row in df_assets.iterrows():
                    col_a, col_b, col_c, col_d = st.columns([2, 1.5, 1.5, 0.5])
                    with col_a:
                        st.write(row['name'])
                    with col_b:
                        st.write(row['asset_type'])
                    with col_c:
                        st.write(f"{row['value']:.0f} €")
                    with col_d:
                        if st.button("🗑️", key=f"del_asset_{row['id']}"):
                            delete_asset(row['name'])
                            st.rerun()
            else:
                st.caption("Keine Aktiva erfasst.")
        
        # PASIVA
        with col2:
            st.markdown('<p style="color: #F44336; font-size: 0.8rem; font-weight: 500; margin-bottom: 0.5rem;">🔴 Passiva (Was du schuldest)</p>', unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="input-area" style="padding: 0.8rem 1rem;">', unsafe_allow_html=True)
                col_a, col_b, col_c, col_d = st.columns([1.5, 1.5, 1.2, 0.6])
                with col_a:
                    liability_name = st.text_input("Name", placeholder="z.B. Kreditkarte", label_visibility="collapsed", key="liability_name")
                with col_b:
                    liability_value = st.number_input("Wert (€)", min_value=0.0, value=1000.0, step=100.0, format="%.0f", label_visibility="collapsed", key="liability_value")
                with col_c:
                    liability_type = st.selectbox("Typ", ["Kurzfristig", "Langfristig"], label_visibility="collapsed", key="liability_type")
                with col_d:
                    if st.button("➕", key="add_liability"):
                        if liability_name.strip():
                            add_liability(liability_name.strip(), liability_value, liability_type)
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            df_liabilities = get_liabilities()
            if not df_liabilities.empty:
                for idx, row in df_liabilities.iterrows():
                    col_a, col_b, col_c, col_d = st.columns([2, 1.5, 1.5, 0.5])
                    with col_a:
                        st.write(row['name'])
                    with col_b:
                        st.write(row['liability_type'])
                    with col_c:
                        st.write(f"{row['value']:.0f} €")
                    with col_d:
                        if st.button("🗑️", key=f"del_liability_{row['id']}"):
                            delete_liability(row['name'])
                            st.rerun()
            else:
                st.caption("Keine Passiva erfasst.")
    
    # ============================================================
    # TAB 3: DASHBOARD (Übersicht)
    # ============================================================
    
    with tab3:
        # KPIs berechnen
        kpis = calculate_kpis()
        actions = get_optimal_action(kpis)
        
        # ============================================================
        # KPI-ÜBERSICHT
        # ============================================================
        
        st.markdown('<p class="section-label">📈 KPI-Übersicht</p>', unsafe_allow_html=True)
        
        kpi_list = [
            {"name": "Cash Runway", "value": kpis['cash_runway'], "target": "12 Monate", "unit": "Monate", "max": 20},
            {"name": "Current Ratio", "value": kpis['current_ratio'], "target": "1,5 – 2,0", "unit": "", "max": 4},
            {"name": "Profit Marge", "value": kpis['profit_marge'], "target": "> 20 %", "unit": "%", "max": 50},
            {"name": "Zinsdeckungsgrad", "value": kpis['interest_coverage'], "target": "> 1,5", "unit": "", "max": 10},
            {"name": "Eigenkapitalquote", "value": kpis['equity_ratio'], "target": "> 30 %", "unit": "%", "max": 100},
            {"name": "Umlaufintensität", "value": kpis['current_assets_ratio'], "target": "20 – 40 %", "unit": "%", "max": 100},
            {"name": "Anlageintensität", "value": kpis['non_current_assets_ratio'], "target": "60 – 80 %", "unit": "%", "max": 100},
        ]
        
        for kpi in kpi_list:
            # Status bestimmen
            if kpi['name'] == 'Cash Runway':
                if kpi['value'] < 12:
                    status = 'red'
                elif kpi['value'] <= 14:
                    status = 'green'
                else:
                    status = 'yellow'
                pct = min((kpi['value'] / 12) * 100, 100) if kpi['value'] > 0 else 0
            elif kpi['name'] == 'Current Ratio':
                if kpi['value'] < 1.5:
                    status = 'red'
                elif kpi['value'] <= 2.0:
                    status = 'green'
                else:
                    status = 'yellow'
                pct = min((kpi['value'] / 2.0) * 100, 100) if kpi['value'] > 0 else 0
            elif kpi['name'] == 'Profit Marge':
                if kpi['value'] < 15:
                    status = 'red'
                elif kpi['value'] >= 20:
                    status = 'green'
                else:
                    status = 'yellow'
                pct = min((kpi['value'] / 20) * 100, 100) if kpi['value'] > 0 else 0
            elif kpi['name'] == 'Zinsdeckungsgrad':
                if kpi['value'] < 1.5:
                    status = 'red'
                else:
                    status = 'green'
                pct = min((kpi['value'] / 1.5) * 100, 100) if kpi['value'] > 0 else 0
            elif kpi['name'] == 'Eigenkapitalquote':
                if kpi['value'] < 25:
                    status = 'red'
                elif kpi['value'] >= 30:
                    status = 'green'
                else:
                    status = 'yellow'
                pct = kpi['value']
            elif kpi['name'] == 'Umlaufintensität':
                if kpi['value'] < 20 or kpi['value'] > 40:
                    status = 'red'
                else:
                    status = 'green'
                pct = kpi['value']
            else:  # Anlageintensität
                if kpi['value'] < 60 or kpi['value'] > 80:
                    status = 'red'
                else:
                    status = 'green'
                pct = kpi['value']
            
            # Anzeige
            color_class = "green" if status == "green" else "yellow" if status == "yellow" else "red"
            display_value = f"{kpi['value']:.1f} {kpi['unit']}" if kpi['unit'] else f"{kpi['value']:.2f}"
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                    <div class="kpi-row">
                        <span class="kpi-label">{kpi['name']}</span>
                        <span class="kpi-value {color_class}">{display_value}</span>
                    </div>
                    <div class="kpi-bar">
                        <div class="fill" style="width: {min(pct, 100)}%; background: {'#4CAF50' if status == 'green' else '#FFC107' if status == 'yellow' else '#F44336'};"></div>
                    </div>
                    <div style="color: rgba(255,255,255,0.15); font-size: 0.55rem; text-align: right; margin-top: 0.1rem;">Ziel: {kpi['target']}</div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================================
        # GRAPHEN
        # ============================================================
        
        st.markdown('<p class="section-label">📊 Visualisierungen</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart: Ausgaben nach Kategorie
            df_tx = get_transactions()
            df_expenses = df_tx[df_tx['type'] == 'Ausgabe']
            if not df_expenses.empty:
                expenses_by_category = df_expenses.groupby('category')['amount'].sum().reset_index()
                fig = px.pie(expenses_by_category, values='amount', names='category', title='Ausgaben nach Kategorie',
                             color_discrete_sequence=px.colors.sequential.Purples_r, hole=0.4)
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Keine Ausgaben erfasst.")
        
        with col2:
            # Balkendiagramm: KPIs
            kpi_names = ['Cash Runway', 'Current Ratio', 'Profit Marge', 'Zinsdeckungsgrad', 'Eigenkapitalquote', 'Umlaufintensität', 'Anlageintensität']
            kpi_values = [
                kpis['cash_runway'],
                kpis['current_ratio'],
                kpis['profit_marge'],
                kpis['interest_coverage'],
                kpis['equity_ratio'],
                kpis['current_assets_ratio'],
                kpis['non_current_assets_ratio']
            ]
            # Normalisieren für bessere Darstellung
            kpi_values_norm = [
                min(kpis['cash_runway'] / 12 * 100, 100),
                min(kpis['current_ratio'] / 2.0 * 100, 100),
                min(kpis['profit_marge'] / 20 * 100, 100),
                min(kpis['interest_coverage'] / 1.5 * 100, 100),
                kpis['equity_ratio'],
                kpis['current_assets_ratio'],
                kpis['non_current_assets_ratio']
            ]
            df_kpis = pd.DataFrame({'KPI': kpi_names, 'Wert (%)': kpi_values_norm})
            fig = px.bar(df_kpis, x='KPI', y='Wert (%)', title='KPI-Erfüllungsgrad (%)',
                         color='KPI', color_discrete_sequence=px.colors.sequential.Greens_r)
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================================
        # OPTIMALE HANDLUNGSEMPFEHLUNG
        # ============================================================
        
        st.markdown('<p class="section-label">🎯 Optimale Handlungsempfehlung</p>', unsafe_allow_html=True)
        
        if actions:
            # Kritische Handlungen (sofort)
            critical_actions = [a for a in actions if a['status'] == 'red']
            if critical_actions:
                st.markdown('<p style="color: #F44336; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;">🔴 KRITISCHE HANDLUNGEN (Sofort)</p>', unsafe_allow_html=True)
                for a in critical_actions:
                    st.markdown(f"""
                        <div class="action-card" style="border-left: 3px solid #F44336;">
                            <div class="action-title">{a['kpi']}</div>
                            <div class="action-detail">⚠️ Problem: {a['problem']}</div>
                            <div class="action-detail">✅ Handlung: {a['action']}</div>
                            <div class="action-detail">📝 {a['detail']}</div>
                            <div class="action-result">➡️ {a['result']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Wichtige Handlungen (innerhalb 6 Monaten)
            important_actions = [a for a in actions if a['status'] == 'yellow']
            if important_actions:
                st.markdown('<p style="color: #FFC107; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;">⚠️ WICHTIGE HANDLUNGEN (Innerhalb 6 Monaten)</p>', unsafe_allow_html=True)
                for a in important_actions:
                    st.markdown(f"""
                        <div class="action-card" style="border-left: 3px solid #FFC107;">
                            <div class="action-title">{a['kpi']}</div>
                            <div class="action-detail">⚠️ Problem: {a['problem']}</div>
                            <div class="action-detail">✅ Handlung: {a['action']}</div>
                            <div class="action-detail">📝 {a['detail']}</div>
                            <div class="action-result">➡️ {a['result']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("🎉 Alle KPIs sind im optimalen Bereich! Keine Handlungsempfehlungen notwendig.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================================
        # ZEIT BIS ZUM ZIEL
        # ============================================================
        
        st.markdown('<p class="section-label">📅 Zeit bis zum Ziel</p>', unsafe_allow_html=True)
        
        months_to_target = kpis['months_to_12_cash']
        
        col1, col2 = st.columns(2)
        with col1:
            if months_to_target < float('inf'):
                st.metric("⏳ Bei Weiterführung", f"{months_to_target:.0f} Monate")
            else:
                st.metric("⏳ Bei Weiterführung", "∞ (kein Überschuss)")
        
        # Optimierte Zeit (wenn Handlungen umgesetzt werden)
        if actions and kpis['monthly_surplus'] > 0:
            # Vereinfachte Annahme: Optimierung halbiert die Zeit
            optimized_months = months_to_target / 2 if months_to_target < float('inf') else 0
            st.metric("🚀 Mit Handlungen", f"{optimized_months:.0f} Monate")
        else:
            st.metric("🚀 Mit Handlungen", "Keine Handlungen nötig")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ============================================================
        # ERKLÄRUNG DER KPIs
        # ============================================================
        
        with st.expander("💡 Erklärung der KPIs", expanded=False):
            explanations = [
                {"name": "Cash Runway", "desc": "Wie viele Monate du ohne Einkommen überlebst – basierend auf deinem Tagesgeld."},
                {"name": "Current Ratio", "desc": "Ob du deine kurzfristigen Rechnungen (Kreditkarte, Dispo) aus deinem kurzfristigen Vermögen bezahlen kannst."},
                {"name": "Profit Marge", "desc": "Wie viel Prozent deines Einkommens nach allen Ausgaben übrig bleibt."},
                {"name": "Zinsdeckungsgrad", "desc": "Ob du deine Zinszahlungen aus deinem laufenden Einkommen bedienen kannst."},
                {"name": "Eigenkapitalquote", "desc": "Wie viel Prozent deines Gesamtvermögens dir wirklich gehört (ohne Schulden)."},
                {"name": "Umlaufintensität", "desc": "Wie viel Prozent deines Vermögens kurzfristig verfügbar ist (Tagesgeld)."},
                {"name": "Anlageintensität", "desc": "Wie viel Prozent deines Vermögens langfristig gebunden ist (ETFs, Immobilien)."},
            ]
            for exp in explanations:
                st.markdown(f"""
                    <div class="kpi-explanation">
                        <div class="kpi-name">{exp['name']}</div>
                        <div class="kpi-desc">{exp['desc']}</div>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
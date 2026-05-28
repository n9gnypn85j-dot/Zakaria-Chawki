"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NEXUS TRADING TERMINAL  —  Complete Single-File app.py                    ║
║  Copy this file to GitHub as app.py.  That's the only file you need.       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ALSO CREATE  requirements.txt  in the same repo with these lines:         ║
║    streamlit                                                                ║
║    ccxt                                                                     ║
║    pandas                                                                   ║
║    numpy                                                                    ║
║    plotly                                                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  DEPLOY (free):                                                             ║
║  1. Push app.py + requirements.txt to a public GitHub repo                 ║
║  2. Go to share.streamlit.io → New app → select repo → Deploy              ║
║  3. Your live URL appears in ~2 minutes                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time

# ═════════════════════════════════════════════════════════════════════════════
# §1  PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NEXUS Trading Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════════════════════════
# §2  GLOBAL CSS  — Bloomberg Terminal × Obsidian Glass
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Design Tokens ───────────────────────────────────────────────────────── */
:root {
  --void:      #030407;
  --bg:        #060910;
  --surface:   #090d16;
  --card:      #0d1120;
  --raised:    #111726;
  --rim:       #161d2e;
  --border:    #1c2438;
  --border-hi: #263045;
  --muted:     #324058;
  --ghost:     #47587a;
  --sub:       #5e719a;
  --text:      #b4c4e8;
  --bright:    #dce8ff;
  --white:     #eef4ff;

  --cyan:      #00ccf5;
  --cyan-glow: rgba(0,204,245,0.18);
  --green:     #00df99;
  --green-dim: rgba(0,223,153,0.10);
  --red:       #ff3255;
  --red-dim:   rgba(255,50,85,0.10);
  --amber:     #ffbc28;
  --indigo:    #7b8fff;
  --indigo-dim:rgba(123,143,255,0.08);
  --purple:    #b06aff;

  --r-xs: 6px;  --r-sm: 9px;
  --r-md: 13px; --r-lg: 17px; --r-xl: 21px;

  --mono:    'IBM Plex Mono', monospace;
  --display: 'Bebas Neue', sans-serif;
  --body:    'DM Sans', sans-serif;

  --shadow-card: 0 4px 24px rgba(0,0,0,0.5), 0 1px 0 rgba(255,255,255,0.03);
  --shadow-glow: 0 0 32px rgba(0,204,245,0.10);
}

/* ── Global Reset ────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

/* ── App Background ──────────────────────────────────────────────────────── */
.stApp {
  background: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 70% 50% at 88% 0%,  rgba(0,204,245,0.055) 0%, transparent 55%),
    radial-gradient(ellipse 50% 40% at 6%  94%,  rgba(0,223,153,0.040) 0%, transparent 50%),
    radial-gradient(ellipse 40% 30% at 50% 50%, rgba(123,143,255,0.025) 0%, transparent 65%),
    repeating-linear-gradient(
      0deg, transparent, transparent 2px,
      rgba(160,190,255,0.0065) 2px, rgba(160,190,255,0.0065) 4px
    ) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
}

/* ── Scrollbar ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-hi); }

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * {
  color: var(--text) !important;
  font-family: var(--body) !important;
}
section[data-testid="stSidebar"] ::-webkit-scrollbar { width: 3px; }

/* ── Metric Cards ────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-lg) !important;
  padding: 18px 20px !important;
  box-shadow: var(--shadow-card) !important;
  transition: border-color .25s, box-shadow .25s !important;
  position: relative; overflow: hidden;
}
[data-testid="stMetric"]::after {
  content: '';
  position: absolute; inset: 0 0 auto 0; height: 1px;
  background: linear-gradient(90deg, transparent 10%, var(--cyan) 50%, transparent 90%);
  opacity: 0; transition: opacity .3s;
}
[data-testid="stMetric"]:hover {
  border-color: var(--border-hi) !important;
  box-shadow: var(--shadow-card), var(--shadow-glow) !important;
}
[data-testid="stMetric"]:hover::after { opacity: .45; }
[data-testid="stMetricLabel"] {
  color: var(--ghost) !important;
  font-family: var(--mono) !important;
  font-size: 9.5px !important;
  letter-spacing: .13em !important;
  text-transform: uppercase !important;
  margin-bottom: 5px !important;
}
[data-testid="stMetricValue"] {
  color: var(--bright) !important;
  font-family: var(--mono) !important;
  font-size: 23px !important;
  font-weight: 600 !important;
  letter-spacing: -.5px !important;
}
[data-testid="stMetricDelta"] {
  font-family: var(--mono) !important;
  font-size: 11.5px !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg,rgba(0,204,245,.10),rgba(0,204,245,.03)) !important;
  border: 1px solid rgba(0,204,245,.28) !important;
  border-radius: var(--r-md) !important;
  color: var(--cyan) !important;
  font-family: var(--mono) !important; font-size: 11px !important;
  font-weight: 600 !important; letter-spacing: .11em !important;
  text-transform: uppercase !important;
  padding: 10px 24px !important;
  transition: all .2s ease !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg,rgba(0,204,245,.19),rgba(0,204,245,.08)) !important;
  border-color: var(--cyan) !important;
  box-shadow: 0 0 24px rgba(0,204,245,.20), inset 0 1px 0 rgba(0,204,245,.14) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Select Boxes ────────────────────────────────────────────────────────── */
[data-baseweb="select"] > div {
  background: var(--card) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important; color: var(--text) !important;
  font-family: var(--mono) !important; font-size: 12px !important;
  transition: border-color .2s !important;
}
[data-baseweb="select"] > div:hover { border-color: var(--border-hi) !important; }
[data-baseweb="popover"] {
  background: var(--raised) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important;
}
[role="option"] { color: var(--text) !important; font-family: var(--mono) !important; font-size: 12px !important; }
[role="option"]:hover { background: var(--border) !important; }

/* ── Sliders ─────────────────────────────────────────────────────────────── */
[data-testid="stSlider"] > div > div > div > div { background: var(--cyan) !important; }
[data-testid="stSlider"] label {
  color: var(--ghost) !important; font-size: 10.5px !important;
  letter-spacing: .08em !important; font-family: var(--mono) !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important; padding: 4px !important; gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: var(--ghost) !important;
  font-family: var(--mono) !important; font-size: 10px !important;
  letter-spacing: .09em !important; text-transform: uppercase !important;
  border-radius: var(--r-sm) !important; padding: 8px 18px !important;
  transition: all .2s !important; border: none !important;
}
.stTabs [aria-selected="true"] {
  background: var(--card) !important; color: var(--cyan) !important;
  box-shadow: 0 0 14px rgba(0,204,245,.12) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 18px !important; }

/* ── Misc Overrides ──────────────────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 16px 0 !important; }
[data-testid="stExpander"] {
  background: var(--card) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important;
}
.stAlert {
  background: var(--card) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important; font-family: var(--body) !important;
}
[data-testid="stCheckbox"] label span { color: var(--text) !important; font-size: 13px !important; }

/* ═══════════════════════════════════════════════════════════════════════════
   COMPONENT CLASSES
═══════════════════════════════════════════════════════════════════════════ */

/* ── Page Header ── */
.nx-header {
  display: flex; align-items: flex-end; justify-content: space-between;
  padding: 28px 0 20px; border-bottom: 1px solid var(--border); margin-bottom: 24px;
}
.nx-logo { display: flex; align-items: center; gap: 14px; }
.nx-logo-icon {
  width: 44px; height: 44px; border-radius: 12px;
  background: linear-gradient(135deg, rgba(0,204,245,.15), rgba(0,204,245,.04));
  border: 1px solid rgba(0,204,245,.34);
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  box-shadow: 0 0 20px rgba(0,204,245,.12), inset 0 1px 0 rgba(0,204,245,.1);
}
.nx-title  { font-family: var(--display); font-size: 30px; letter-spacing: .06em; color: var(--bright); line-height: 1; margin: 0; }
.nx-sub    { font-family: var(--mono); font-size: 9px; letter-spacing: .15em; color: var(--ghost); text-transform: uppercase; margin-top: 4px; }
.nx-header-right { display: flex; align-items: center; gap: 14px; }
.nx-clock  { font-family: var(--mono); font-size: 11px; color: var(--muted); letter-spacing: .05em; }
.nx-live-badge {
  display: flex; align-items: center; gap: 7px;
  background: rgba(0,223,153,.09); border: 1px solid rgba(0,223,153,.24);
  border-radius: 20px; padding: 5px 13px;
}
.nx-live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green); box-shadow: 0 0 7px var(--green);
  animation: pulse-dot 2s ease infinite;
}
@keyframes pulse-dot {
  0%,100% { opacity:1;transform:scale(1);box-shadow:0 0 7px var(--green); }
  50%     { opacity:.6;transform:scale(1.12);box-shadow:0 0 14px var(--green); }
}
.nx-live-text { font-family: var(--mono); font-size: 10px; font-weight: 700; letter-spacing: .1em; color: var(--green); }

/* ── Ticker Bar ── */
.nx-ticker {
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-md);
  padding: 11px 22px; display: flex; gap: 28px; align-items: center;
  margin-bottom: 22px; overflow-x: auto; scrollbar-width: none;
}
.nx-ticker::-webkit-scrollbar { display: none; }
.nx-ticker-item { display: flex; align-items: center; gap: 9px; flex-shrink: 0; }
.nx-ticker-sym   { font-family: var(--mono); font-size: 9.5px; font-weight: 700; letter-spacing: .1em; color: var(--ghost); }
.nx-ticker-price { font-family: var(--mono); font-size: 13px; font-weight: 600; color: var(--bright); letter-spacing: -.3px; }
.nx-ticker-up    { font-family: var(--mono); font-size: 11px; font-weight: 600; color: var(--green); }
.nx-ticker-dn    { font-family: var(--mono); font-size: 11px; font-weight: 600; color: var(--red); }
.nx-ticker-sep   { width: 1px; height: 22px; background: var(--border); flex-shrink: 0; }

/* ── Section Heading ── */
.nx-section {
  font-family: var(--mono); font-size: 9px; font-weight: 700;
  letter-spacing: .15em; text-transform: uppercase;
  color: var(--muted); margin: 24px 0 14px;
  padding-bottom: 8px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 8px;
}
.nx-section-line { flex: 1; height: 1px; background: linear-gradient(90deg, var(--border), transparent); }

/* ── Asset Card ── */
.nx-asset {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: 17px 19px;
  box-shadow: var(--shadow-card);
  transition: border-color .25s, box-shadow .25s, transform .2s;
  cursor: default; position: relative; overflow: hidden;
}
.nx-asset::after {
  content:''; position:absolute; inset:0; border-radius:inherit;
  background: linear-gradient(135deg, rgba(255,255,255,.025) 0%, transparent 60%);
  pointer-events: none;
}
.nx-asset:hover {
  border-color: var(--border-hi);
  box-shadow: var(--shadow-card), 0 0 22px rgba(0,204,245,.07);
  transform: translateY(-2px);
}
.nx-asset-icon {
  width: 40px; height: 40px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; font-weight: 800; font-family: var(--mono);
}
.nx-asset-name  { font-size: 14px; font-weight: 600; color: var(--bright); font-family: var(--body); }
.nx-asset-pair  { font-size: 10.5px; color: var(--muted); font-family: var(--mono); margin-top: 2px; letter-spacing: .04em; }
.nx-asset-price { font-size: 18px; font-weight: 600; font-family: var(--mono); color: var(--bright); letter-spacing: -.5px; }
.nx-chg-up { font-family: var(--mono); font-size: 12px; font-weight: 600; color: var(--green); }
.nx-chg-dn { font-family: var(--mono); font-size: 12px; font-weight: 600; color: var(--red);   }
.nx-stat-lbl { font-family: var(--mono); font-size: 9.5px; color: var(--ghost); letter-spacing: .06em; margin-bottom: 2px; }
.nx-stat-val { font-family: var(--mono); font-size: 11.5px; font-weight: 600; color: var(--text); }

/* ── Signal Card ── */
.nx-signal {
  padding: 22px 24px; border-radius: var(--r-xl);
  position: relative; overflow: hidden; animation: fadeUp .4s ease;
  box-shadow: var(--shadow-card);
}
@keyframes fadeUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
.nx-signal-lbl  { font-family: var(--mono); font-size: 9px; letter-spacing: .15em; text-transform: uppercase; color: var(--ghost); margin-bottom: 8px; }
.nx-signal-val  { font-family: var(--display); font-size: 36px; letter-spacing: .07em; line-height: 1; margin-bottom: 3px; }
.nx-signal-zone { font-family: var(--mono); font-size: 9.5px; letter-spacing: .1em; opacity: .65; margin-bottom: 14px; }
.nx-signal-bar-bg   { height: 4px; background: rgba(0,0,0,.35); border-radius: 2px; overflow: hidden; margin-bottom: 7px; }
.nx-signal-bar-fill { height: 100%; border-radius: 2px; transition: width .7s ease; }
.nx-signal-conf { font-family: var(--mono); font-size: 9.5px; letter-spacing: .08em; opacity: .6; }

/* ── Indicator Panel ── */
.nx-panel {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: 16px 18px;
  box-shadow: var(--shadow-card); margin-bottom: 10px;
}
.nx-panel-title {
  font-family: var(--mono); font-size: 9px; font-weight: 700;
  letter-spacing: .14em; text-transform: uppercase; color: var(--ghost);
  margin-bottom: 13px; padding-bottom: 9px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 7px;
}
.nx-panel-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--cyan); box-shadow: 0 0 6px var(--cyan); }
.nx-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(28,36,56,.5); font-size: 12px; }
.nx-row:last-child { border-bottom: none; }
.nx-key   { color: var(--ghost); font-family: var(--mono); font-size: 10.5px; letter-spacing: .04em; }
.nx-val   { color: var(--bright); font-family: var(--mono); font-size: 11.5px; font-weight: 600; }
.nx-green { color: var(--green);  font-family: var(--mono); font-size: 11.5px; font-weight: 600; }
.nx-red   { color: var(--red);    font-family: var(--mono); font-size: 11.5px; font-weight: 600; }
.nx-amber { color: var(--amber);  font-family: var(--mono); font-size: 11.5px; font-weight: 600; }
.nx-cyan  { color: var(--cyan);   font-family: var(--mono); font-size: 11.5px; font-weight: 600; }

/* ── RSI Big Display ── */
.nx-rsi-big { font-family: var(--mono); font-size: 52px; font-weight: 700; letter-spacing: -3px; line-height: 1; transition: color .5s, text-shadow .5s; }
.nx-rsi-zone-bar { display: flex; height: 5px; border-radius: 3px; overflow: hidden; gap: 2px; margin: 9px 0 5px; }
.nx-rsi-seg { border-radius: 2px; transition: opacity .4s; }
.nx-rsi-axis { display: flex; justify-content: space-between; font-family: var(--mono); font-size: 9px; color: var(--muted); margin-bottom: 10px; }

/* ── Strength Bars ── */
.nx-strength { display: flex; gap: 3px; align-items: flex-end; }
.nx-sbar { width: 4px; border-radius: 2px; transition: background .4s; }

/* ── Bot Bubble ── */
.nx-bubble {
  border-radius: 0 var(--r-lg) var(--r-lg) var(--r-lg);
  padding: 13px 17px; margin-bottom: 10px;
  font-family: var(--body); font-size: 14px; line-height: 1.65;
  color: var(--text); animation: fadeUp .3s ease;
  box-shadow: var(--shadow-card);
}
.nx-bubble-time { font-family: var(--mono); font-size: 9px; color: var(--muted); margin-top: 6px; letter-spacing: .06em; }

/* ── Log Entry ── */
.nx-log {
  display: flex; align-items: center; gap: 12px;
  padding: 8px 13px; background: var(--surface);
  border: 1px solid var(--border); border-radius: 9px;
  margin-bottom: 6px; font-family: var(--mono); font-size: 11px; color: var(--text);
}

/* ── Sidebar ── */
.nx-sb-head { padding: 22px 18px 18px; border-bottom: 1px solid var(--border); text-align: center; margin-bottom: 18px; }
.nx-sb-title { font-family: var(--display); font-size: 22px; letter-spacing: .1em; color: var(--bright); margin-bottom: 2px; }
.nx-sb-sub   { font-family: var(--mono); font-size: 8px; color: var(--ghost); letter-spacing: .14em; text-transform: uppercase; }
.nx-sb-sec   { font-family: var(--mono); font-size: 8.5px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); margin: 16px 0 9px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
.nx-conn {
  display: flex; align-items: center; justify-content: center; gap: 7px;
  padding: 9px; background: rgba(0,223,153,.07); border: 1px solid rgba(0,223,153,.2);
  border-radius: 9px; margin-top: 14px;
  font-family: var(--mono); font-size: 10.5px; font-weight: 700;
  color: var(--green); letter-spacing: .06em;
}
.nx-conn-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--green); animation: pulse-dot 2s ease infinite; }

/* ── Footer ── */
.nx-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding: 13px 0; border-top: 1px solid var(--border); margin-top: 30px;
  font-family: var(--mono); font-size: 9px; color: var(--muted); letter-spacing: .07em;
}
@keyframes ripple-out { 0%{transform:scale(.9);opacity:1} 100%{transform:scale(2.0);opacity:0} }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# §3  CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════
ASSETS = {
    "BTC/USDT": {"name": "Bitcoin",  "icon": "₿",  "color": "#f7931a", "bg": "rgba(247,147,26,0.13)"},
    "ETH/USDT": {"name": "Ethereum", "icon": "Ξ",  "color": "#818cf8", "bg": "rgba(129,140,248,0.13)"},
    "XAU/USDT": {"name": "Gold",     "icon": "Au", "color": "#ffbc28", "bg": "rgba(255,188,40,0.13)"},
}

TIMEFRAMES = {
    "1m":  "1 Min",  "5m":  "5 Min",  "15m": "15 Min",
    "1h":  "1 Hour", "4h":  "4 Hours","1d":  "Daily",
}

SIGNALS = {
    "STRONG BUY":  {"color": "#00df99", "bg": "rgba(0,223,153,0.11)", "border": "rgba(0,223,153,0.30)", "icon": "▲▲", "zone": "DEEP OVERSOLD"},
    "BUY":         {"color": "#00c87a", "bg": "rgba(0,200,122,0.08)", "border": "rgba(0,200,122,0.22)", "icon": "▲",  "zone": "OVERSOLD"},
    "HOLD":        {"color": "#7b8fff", "bg": "rgba(123,143,255,0.08)","border":"rgba(123,143,255,0.25)","icon": "■",  "zone": "NEUTRAL"},
    "SELL":        {"color": "#ff7040", "bg": "rgba(255,112,64,0.08)", "border": "rgba(255,112,64,0.22)", "icon": "▼",  "zone": "OVERBOUGHT"},
    "STRONG SELL": {"color": "#ff3255", "bg": "rgba(255,50,85,0.11)",  "border": "rgba(255,50,85,0.30)",  "icon": "▼▼", "zone": "DEEP OVERBOUGHT"},
}

# ═════════════════════════════════════════════════════════════════════════════
# §4  DATA LAYER
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def _exchange():
    """Shared Binance client — created once per session."""
    return ccxt.binance({"enableRateLimit": True})


@st.cache_data(ttl=60)
def get_price(symbol: str) -> float:
    """
    Your original function — preserved 100%.
    Used internally and available if you import this module.
    """
    exchange = _exchange()
    ticker   = exchange.fetch_ticker(symbol)
    return ticker["last"]


@st.cache_data(ttl=60)
def _ticker_full(symbol: str) -> dict:
    """Extended ticker with 24-h stats."""
    t = _exchange().fetch_ticker(symbol)
    return {
        "price":  t["last"]           or 0.0,
        "change": t.get("percentage") or 0.0,
        "high":   t.get("high")       or 0.0,
        "low":    t.get("low")        or 0.0,
        "volume": t.get("baseVolume") or 0.0,
    }


@st.cache_data(ttl=60)
def _ohlcv(symbol: str, timeframe: str, limit: int = 220) -> pd.DataFrame:
    """Fetch OHLCV candles and return a clean DataFrame."""
    raw = _exchange().fetch_ohlcv(symbol, timeframe, limit=limit)
    df  = pd.DataFrame(raw, columns=["ts", "open", "high", "low", "close", "volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    return df.set_index("ts").astype(float)


# ── Technical Indicators ──────────────────────────────────────────────────────

def _rsi(s: pd.Series, p: int = 14) -> pd.Series:
    d  = s.diff()
    ag = d.clip(lower=0).ewm(alpha=1/p, min_periods=p, adjust=False).mean()
    al = (-d.clip(upper=0)).ewm(alpha=1/p, min_periods=p, adjust=False).mean()
    return 100 - 100 / (1 + ag / al.replace(0, np.nan))


def _macd(s: pd.Series, f=12, sl=26, sg=9):
    ml = s.ewm(span=f,  adjust=False).mean() - s.ewm(span=sl, adjust=False).mean()
    si = ml.ewm(span=sg, adjust=False).mean()
    return ml, si, ml - si


def _bb(s: pd.Series, p=20, d=2):
    m = s.rolling(p).mean()
    v = s.rolling(p).std()
    return m + d*v, m, m - d*v


def _analyze(symbol: str, timeframe: str,
             rsi_period: int, rsi_low: int, rsi_high: int) -> dict:
    """
    Full technical analysis.
    Signal scoring extends your original price < 60 000 logic
    with RSI + MACD + Bollinger + EMA cross.
    """
    df              = _ohlcv(symbol, timeframe)
    c               = df["close"]
    df["rsi"]       = _rsi(c, rsi_period)
    df["ema20"]     = c.ewm(span=20, adjust=False).mean()
    df["ema50"]     = c.ewm(span=50, adjust=False).mean()
    df["macd"], df["macd_sig"], df["macd_hist"] = _macd(c)
    df["bb_up"], df["bb_mid"], df["bb_lo"]      = _bb(c)

    L, P = df.iloc[-1], df.iloc[-2]

    # ── Score (your original price < 60 000 threshold maps to score +3) ──────
    score = 0
    if   L.rsi < rsi_low:       score += 3      # oversold  → buy
    elif L.rsi < rsi_low  + 5:  score += 1
    elif L.rsi > rsi_high:      score -= 3      # overbought→ sell
    elif L.rsi > rsi_high - 5:  score -= 1
    if L.macd_hist > 0:         score += 1      # bullish momentum
    if L.macd_hist < 0:         score -= 1
    if L.close < L.bb_lo:       score += 1      # near lower band → cheap
    if L.close > L.bb_up:       score -= 1      # near upper band → expensive
    if L.ema20 > L.ema50:       score += 1      # golden cross region
    if L.ema20 < L.ema50:       score -= 1      # death  cross region

    signal = (
        "STRONG BUY"  if score >= 4  else
        "BUY"         if score >= 2  else
        "STRONG SELL" if score <= -4 else
        "SELL"        if score <= -2 else "HOLD"
    )
    confidence = min(100, abs(score) * 17 + 18)

    return {
        "df":          df,
        "price":       L.close,
        "pct_change":  (L.close - P.close) / P.close * 100,
        "rsi":         L.rsi,    "rsi_prev": P.rsi,
        "macd":        L.macd,   "macd_hist": L.macd_hist,
        "bb_up":       L.bb_up,  "bb_lo":  L.bb_lo,
        "ema20":       L.ema20,  "ema50":  L.ema50,
        "volume":      L.volume,
        "signal":      signal,   "confidence": confidence,
        "score":       score,
        "ts":          datetime.now().strftime("%H:%M:%S"),
    }

# ═════════════════════════════════════════════════════════════════════════════
# §5  PLOTLY CHART  (dark theme, 3 panes: Candles+BB+EMA / RSI / MACD)
# ═════════════════════════════════════════════════════════════════════════════

def _chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.58, 0.22, 0.20],
    )

    # Candles
    fig.add_trace(go.Candlestick(
        x=df.index, open=df.open, high=df.high, low=df.low, close=df.close,
        name=symbol,
        increasing_fillcolor="#00df99", increasing_line_color="#00c87a",
        decreasing_fillcolor="#ff3255", decreasing_line_color="#cc2244",
        increasing_line_width=1, decreasing_line_width=1,
    ), row=1, col=1)
    # EMAs
    fig.add_trace(go.Scatter(x=df.index, y=df.ema20, name="EMA 20",
        line=dict(color="#00ccf5", width=1.3, dash="dot"), opacity=.85), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df.ema50, name="EMA 50",
        line=dict(color="#ffbc28", width=1.3, dash="dash"), opacity=.85), row=1, col=1)
    # Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=df.bb_up, name="BB Upper",
        line=dict(color="rgba(123,143,255,.55)", width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df.bb_lo, name="BB Lower",
        line=dict(color="rgba(123,143,255,.55)", width=1),
        fill="tonexty", fillcolor="rgba(123,143,255,.04)"), row=1, col=1)
    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df.rsi, name="RSI",
        line=dict(color="#7b8fff", width=2),
        fill="tozeroy", fillcolor="rgba(123,143,255,.055)"), row=2, col=1)
    for lvl, col in [(30, "#00df99"), (70, "#ff3255")]:
        fig.add_hline(y=lvl, line_color=col, line_width=1,
                      line_dash="dot", row=2, col=1, opacity=.4)
    fig.add_hrect(y0=0,  y1=30,  fillcolor="rgba(0,223,153,.04)",  row=2, col=1, line_width=0)
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(255,50,85,.04)",   row=2, col=1, line_width=0)
    # MACD
    hist_colors = ["#00df99" if v >= 0 else "#ff3255" for v in df.macd_hist]
    fig.add_trace(go.Bar(x=df.index, y=df.macd_hist, name="Hist",
        marker_color=hist_colors, opacity=.75), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df.macd, name="MACD",
        line=dict(color="#00ccf5", width=1.6)), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df.macd_sig, name="Signal",
        line=dict(color="#ffbc28", width=1.6)), row=3, col=1)

    ax_style = dict(
        gridcolor="#141c2a", gridwidth=1, zerolinecolor="#1c2438",
        linecolor="#1c2438",
        tickfont=dict(color="#324058", size=9, family="IBM Plex Mono"),
    )
    fig.update_layout(
        height=590,
        paper_bgcolor="#060910", plot_bgcolor="#090d16",
        font=dict(family="IBM Plex Mono", color="#324058", size=10),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#090d16", bordercolor="#1c2438", font_color="#b4c4e8"),
        legend=dict(
            bgcolor="rgba(9,13,22,.92)", bordercolor="#1c2438", borderwidth=1,
            font=dict(size=9, color="#47587a"),
        ),
        margin=dict(l=0, r=0, t=8, b=0),
    )
    fig.update_xaxes(**ax_style)
    fig.update_yaxes(**ax_style)
    return fig

# ═════════════════════════════════════════════════════════════════════════════
# §6  HTML COMPONENT BUILDERS
# ═════════════════════════════════════════════════════════════════════════════

def _h_signal(data: dict) -> str:
    s   = data["signal"]
    cfg = SIGNALS[s]
    w   = data["confidence"]
    return f"""
    <div class="nx-signal"
         style="background:{cfg['bg']};border:1px solid {cfg['border']};">
      <div class="nx-signal-lbl">AI Signal Engine</div>
      <div class="nx-signal-val"
           style="color:{cfg['color']};text-shadow:0 0 20px {cfg['color']}45;">
        {cfg['icon']}&nbsp;{s}
      </div>
      <div class="nx-signal-zone" style="color:{cfg['color']};">{cfg['zone']}</div>
      <div class="nx-signal-bar-bg">
        <div class="nx-signal-bar-fill"
             style="width:{w}%;background:{cfg['color']};
                    box-shadow:0 0 8px {cfg['color']}65;"></div>
      </div>
      <div class="nx-signal-conf" style="color:{cfg['color']};">
        Confidence: {w}%
      </div>
    </div>"""


def _h_asset(sym: str, t: dict) -> str:
    a  = ASSETS[sym]
    up = t["change"] >= 0
    c  = "#00df99" if up else "#ff3255"
    ch = f"+{t['change']:.2f}%" if up else f"{t['change']:.2f}%"
    return f"""
    <div class="nx-asset">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div class="nx-asset-icon"
             style="background:{a['bg']};border:1px solid {a['color']}44;color:{a['color']};">
          {a['icon']}
        </div>
        <div>
          <div class="nx-asset-name">{a['name']}</div>
          <div class="nx-asset-pair">{sym}</div>
        </div>
        <div style="margin-left:auto;text-align:right;">
          <div class="nx-asset-price">${t['price']:,.2f}</div>
          <div class="{'nx-chg-up' if up else 'nx-chg-dn'}">{ch}</div>
        </div>
      </div>
      <div style="height:1px;background:var(--border);margin-bottom:10px;"></div>
      <div style="display:flex;justify-content:space-between;">
        <div>
          <div class="nx-stat-lbl">24h High</div>
          <div class="nx-stat-val">${t['high']:,.2f}</div>
        </div>
        <div style="text-align:center;">
          <div class="nx-stat-lbl">Volume</div>
          <div class="nx-stat-val">{t['volume']:,.0f}</div>
        </div>
        <div style="text-align:right;">
          <div class="nx-stat-lbl">24h Low</div>
          <div class="nx-stat-val">${t['low']:,.2f}</div>
        </div>
      </div>
    </div>"""


def _h_indicators(data: dict, rsi_low: int, rsi_high: int) -> str:
    r   = data["rsi"]
    rc  = "#00df99" if r < rsi_low else "#ff3255" if r > rsi_high else "#7b8fff"
    rz  = "OVERSOLD" if r < rsi_low else "OVERBOUGHT" if r > rsi_high else "NEUTRAL"
    o   = lambda cond: "1" if cond else ".15"
    mc  = "nx-green" if data["macd_hist"] > 0 else "nx-red"
    md  = "▲ Bullish" if data["macd_hist"] > 0 else "▼ Bearish"
    ec  = "nx-green"  if data["ema20"] > data["ema50"] else "nx-red"
    et  = "▲ Uptrend" if data["ema20"] > data["ema50"] else "▼ Downtrend"
    bp  = ("Near Lower 🟢" if data["price"] < data["bb_lo"] * 1.01
           else "Near Upper 🔴" if data["price"] > data["bb_up"] * 0.99
           else "Mid Band  ●")
    return f"""
    <div class="nx-panel">
      <div class="nx-panel-title">
        <div class="nx-panel-dot"></div>RSI Indicator
      </div>
      <div style="text-align:center;padding:6px 0 2px;">
        <div class="nx-rsi-big"
             style="color:{rc};text-shadow:0 0 24px {rc}45;">{r:.1f}</div>
        <div style="font-family:var(--mono);font-size:9.5px;
                    color:{rc};opacity:.7;letter-spacing:.1em;">{rz}</div>
      </div>
      <div class="nx-rsi-zone-bar">
        <div class="nx-rsi-seg" style="flex:30;background:#00df99;opacity:{o(r < rsi_low)};"></div>
        <div class="nx-rsi-seg" style="flex:40;background:#7b8fff;opacity:{o(rsi_low<=r<=rsi_high)};"></div>
        <div class="nx-rsi-seg" style="flex:30;background:#ff3255;opacity:{o(r > rsi_high)};"></div>
      </div>
      <div class="nx-rsi-axis">
        <span>0</span><span>{rsi_low}</span><span>{rsi_high}</span><span>100</span>
      </div>
      <div class="nx-row">
        <span class="nx-key">MACD</span>
        <span class="{mc}">{md}</span>
      </div>
      <div class="nx-row">
        <span class="nx-key">EMA Trend</span>
        <span class="{ec}">{et}</span>
      </div>
      <div class="nx-row">
        <span class="nx-key">Bollinger</span>
        <span class="nx-val" style="font-size:10.5px;">{bp}</span>
      </div>
      <div class="nx-row">
        <span class="nx-key">EMA 20</span>
        <span class="nx-cyan">${data['ema20']:,.2f}</span>
      </div>
      <div class="nx-row">
        <span class="nx-key">EMA 50</span>
        <span class="nx-amber">${data['ema50']:,.2f}</span>
      </div>
    </div>"""


def _h_strength(signal: str, confidence: int) -> str:
    cfg    = SIGNALS[signal]
    filled = max(1, round(confidence / 20))
    bars   = "".join(
        f'<div class="nx-sbar" style="height:{5+i*4}px;'
        f'background:{"" + cfg["color"] if i <= filled else "var(--rim)"};'
        f'{"box-shadow:0 0 5px "+cfg["color"]+";" if i<=filled else ""}"></div>'
        for i in range(1, 6)
    )
    return f'<div class="nx-strength" title="Signal strength">{bars}</div>'


def _h_log(entry: dict) -> str:
    cfg = SIGNALS[entry["signal"]]
    return f"""
    <div class="nx-log">
      <span style="color:var(--muted);min-width:58px;">{entry['time']}</span>
      <span style="color:var(--ghost);min-width:78px;font-weight:700;">{entry['symbol']}</span>
      <span style="color:var(--bright);min-width:110px;">${entry['price']:,.2f}</span>
      <span style="color:var(--ghost);min-width:70px;">RSI {entry['rsi']:.1f}</span>
      <span style="color:{cfg['color']};font-weight:700;">{cfg['icon']} {entry['signal']}</span>
    </div>"""

# ═════════════════════════════════════════════════════════════════════════════
# §7  SESSION STATE  (persists across reruns)
# ═════════════════════════════════════════════════════════════════════════════
if "log"          not in st.session_state: st.session_state.log = []
if "last_refresh" not in st.session_state: st.session_state.last_refresh = 0.0

# ═════════════════════════════════════════════════════════════════════════════
# §8  SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="nx-sb-head">
      <div style="font-size:36px;margin-bottom:8px;">⚡</div>
      <div class="nx-sb-title">NEXUS</div>
      <div class="nx-sb-sub">Trading Terminal v2.0</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nx-sb-sec">📊 Analysis Settings</div>', unsafe_allow_html=True)
    symbol    = st.selectbox("Asset",     list(ASSETS.keys()),       label_visibility="collapsed")
    tf_label  = st.selectbox("Timeframe", list(TIMEFRAMES.values()), index=3, label_visibility="collapsed")
    timeframe = [k for k, v in TIMEFRAMES.items() if v == tf_label][0]

    st.markdown('<div class="nx-sb-sec">📈 RSI Configuration</div>', unsafe_allow_html=True)
    rsi_period = st.slider("RSI Period",       5,  30, 14)
    rsi_low    = st.slider("Oversold Level",  10,  45, 30)
    rsi_high   = st.slider("Overbought Level",55,  90, 70)

    st.markdown('<div class="nx-sb-sec">🔄 Auto Refresh</div>', unsafe_allow_html=True)
    auto_refresh = st.checkbox("Enable auto-refresh", value=True)
    refresh_secs = st.slider("Interval (sec)", 15, 120, 30, 5, disabled=not auto_refresh)

    st.markdown('<div class="nx-sb-sec">🖥️ Display Options</div>', unsafe_allow_html=True)
    show_chart = st.checkbox("Show price chart",  value=True)
    show_log   = st.checkbox("Show signal log",   value=True)

    st.markdown("""
    <div class="nx-conn">
      <div class="nx-conn-dot"></div>Binance · Live Feed
    </div>
    <div style="font-family:var(--mono);font-size:8.5px;color:var(--muted);
                text-align:center;margin-top:7px;letter-spacing:.07em;">
      READ-ONLY — no real orders
    </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# §9  PAGE HEADER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="nx-header">
  <div class="nx-logo">
    <div class="nx-logo-icon">⚡</div>
    <div>
      <div class="nx-title">NEXUS <span style="color:var(--cyan);">TERMINAL</span></div>
      <div class="nx-sub">Professional Crypto Signal Engine · Binance Live Data</div>
    </div>
  </div>
  <div class="nx-header-right">
    <div class="nx-clock">{datetime.now().strftime('%d %b %Y · %H:%M:%S UTC')}</div>
    <div class="nx-live-badge">
      <div class="nx-live-dot"></div>
      <div class="nx-live-text">LIVE</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# Refresh button (centred)
_, btn_col, _ = st.columns([4, 1, 4])
with btn_col:
    manual_refresh = st.button("⟳  Refresh", use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# §10  MAIN DATA FETCH + RENDER
# ═════════════════════════════════════════════════════════════════════════════
with st.spinner(""):
    try:
        # ── 1. Ticker bar ─────────────────────────────────────────────────────
        tickers = {s: _ticker_full(s) for s in ASSETS}

        bar_html = ""
        for i, (sym_key, t) in enumerate(tickers.items()):
            up      = t["change"] >= 0
            chg_col = "#00df99" if up else "#ff3255"
            chg_str = f"+{t['change']:.2f}%" if up else f"{t['change']:.2f}%"
            sep     = '<div class="nx-ticker-sep"></div>' if i < len(tickers) - 1 else ""
            bar_html += f"""
            <div class="nx-ticker-item">
              <span class="nx-ticker-sym">{sym_key.split('/')[0]}</span>
              <span class="nx-ticker-price">${t['price']:,.2f}</span>
              <span style="font-family:var(--mono);font-size:11px;
                           font-weight:600;color:{chg_col};">{chg_str}</span>
            </div>{sep}"""
        st.markdown(f'<div class="nx-ticker">{bar_html}</div>', unsafe_allow_html=True)

        # ── 2. Asset overview cards ───────────────────────────────────────────
        st.markdown(
            '<div class="nx-section">Asset Overview'
            '<div class="nx-section-line"></div></div>',
            unsafe_allow_html=True,
        )
        for card_col, sym_key in zip(st.columns(3), ASSETS.keys()):
            card_col.markdown(_h_asset(sym_key, tickers[sym_key]), unsafe_allow_html=True)

        # ── 3. Full technical analysis on selected symbol ─────────────────────
        st.markdown(
            f'<div class="nx-section">Signal Analysis · {symbol}'
            f'<div class="nx-section-line"></div></div>',
            unsafe_allow_html=True,
        )

        data = _analyze(symbol, timeframe, rsi_period, rsi_low, rsi_high)
        st.session_state.last_refresh = time.time()

        # Append to signal log
        st.session_state.log = (st.session_state.log + [{
            "time":   data["ts"],
            "symbol": symbol,
            "price":  data["price"],
            "rsi":    data["rsi"],
            "signal": data["signal"],
        }])[-40:]

        # ── 4. Two-column layout: left = signal + indicators, right = data ────
        left_col, right_col = st.columns([1, 2])

        with left_col:
            # Signal card
            st.markdown(_h_signal(data), unsafe_allow_html=True)

            # Strength row
            sig_cfg = SIGNALS[data["signal"]]
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:9px;margin:9px 0 14px;"
                f"font-family:IBM Plex Mono,monospace;font-size:9.5px;color:var(--ghost);'>"
                f"STRENGTH &nbsp;"
                f"{_h_strength(data['signal'], data['confidence'])}"
                f"</div>",
                unsafe_allow_html=True,
            )

            # Indicator panel
            st.markdown(_h_indicators(data, rsi_low, rsi_high), unsafe_allow_html=True)

        with right_col:
            # ── Metric cards (your original col1.metric preserved + extended) ──
            m1, m2, m3, m4 = st.columns(4)
            base = symbol.split("/")[0]

            m1.metric(
                label=f"💰 {base} / USDT",
                value=f"${data['price']:,.2f}",
                delta=f"{data['pct_change']:+.2f}%",
            )
            m2.metric(
                label=f"📊 RSI ({rsi_period})",
                value=f"{data['rsi']:.1f}",
                delta=f"{data['rsi'] - data['rsi_prev']:+.1f}",
                delta_color="inverse",
            )
            m3.metric(
                label="📈 MACD",
                value=f"{data['macd']:.4f}",
                delta=f"{'▲' if data['macd_hist'] > 0 else '▼'} {abs(data['macd_hist']):.4f}",
            )
            m4.metric(
                label="📦 Volume",
                value=f"{data['volume'] / 1_000_000:.2f}M",
            )

            st.markdown("---")

            # ── Bot message (your original logic preserved exactly) ───────────
            price = data["price"]   # original variable name kept

            if symbol == "BTC/USDT" and price < 60_000:
                # ← your original condition
                bot_msg  = "🤖 السعر مناسب جداً للشراء، توكل على الله!"
                bot_type = "buy"
            elif data["signal"] in ["STRONG BUY", "BUY"]:
                bot_msg  = (f"🤖 RSI في منطقة ذروة البيع "
                            f"({data['rsi']:.0f}). إشارة شراء محتملة — "
                            f"MACD {'صاعد 📈' if data['macd_hist'] > 0 else 'لم يؤكد بعد ⚠'}.")
                bot_type = "buy"
            elif data["signal"] in ["STRONG SELL", "SELL"]:
                bot_msg  = (f"🤖 RSI في منطقة ذروة الشراء "
                            f"({data['rsi']:.0f}). احذر من الانعكاس — "
                            f"MACD {'هابط 📉' if data['macd_hist'] < 0 else 'لم يؤكد بعد ⚠'}.")
                bot_type = "sell"
            else:
                bot_msg  = (f"🤖 السوق في منطقة محايدة. RSI = {data['rsi']:.0f}. "
                            f"انتظر إشارة أوضح قبل الدخول.")
                bot_type = "hold"

            bub_border = ("#00df99" if bot_type == "buy"
                          else "#ff3255" if bot_type == "sell" else "#7b8fff")
            bub_bg = (f"rgba(0,223,153,.07)"  if bot_type == "buy"
                      else f"rgba(255,50,85,.07)"   if bot_type == "sell"
                      else "rgba(123,143,255,.07)")

            st.markdown(f"""
            <div class="nx-bubble"
                 style="background:{bub_bg};
                        border:1px solid rgba(0,0,0,.15);
                        border-right:3px solid {bub_border};">
              {bot_msg}
              <div class="nx-bubble-time">
                {data['ts']} · {symbol} · {tf_label}
              </div>
            </div>""", unsafe_allow_html=True)

            # ── Chart ─────────────────────────────────────────────────────────
            if show_chart:
                st.plotly_chart(
                    _chart(data["df"].tail(100), symbol),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

        # ── 5. Signal log ─────────────────────────────────────────────────────
        if show_log and st.session_state.log:
            st.markdown(
                '<div class="nx-section">Signal Log'
                '<div class="nx-section-line"></div></div>',
                unsafe_allow_html=True,
            )
            for entry in reversed(st.session_state.log[-14:]):
                st.markdown(_h_log(entry), unsafe_allow_html=True)

        # ── 6. Footer ─────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="nx-footer">
          <span>NEXUS TERMINAL v2.0 · RSI({rsi_period}) · {timeframe.upper()} · Binance</span>
          <span>READ-ONLY — no real orders placed</span>
          <span>⚠ Not financial advice</span>
        </div>""", unsafe_allow_html=True)

    # ── Error handling (your original try/except preserved + extended) ────────
    except ccxt.NetworkError as e:
        st.error(f"🌐 Network error — check your internet connection: {e}")
    except ccxt.ExchangeError as e:
        st.error(f"📡 Binance exchange error: {e}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        with st.expander("🔍 Full stack trace"):
            st.exception(e)

# ═════════════════════════════════════════════════════════════════════════════
# §11  AUTO-REFRESH
# ═════════════════════════════════════════════════════════════════════════════
if auto_refresh:
    time.sleep(refresh_secs)
    st.rerun()

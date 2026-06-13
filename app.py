import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Institutional Breakout Core", layout="wide")

# Custom CSS for Premium Institutional Display Look
st.markdown("""
    <style>
    .metric-container {
        background-color: #0f172a;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #38bdf8;
        margin-bottom: 15px;
    }
    .signal-high { color: #22c55e; font-weight: bold; }
    .signal-low { color: #ef4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. ALGORITHMIC QUANT & FUNDAMENTAL ENGINE
@st.cache_data(ttl=900)  # 15-minute intelligence cache refreshed dynamically
def pull_institutional_intelligence(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Pull 1-Year Data Frame for Pure Technical Logic
        hist = ticker.history(period="1y")
        if hist.empty: return None
        
        # --- TECHNICAL & LIQUIDITY SHOCK CALCULATIONS ---
        latest_close = hist['Close'].iloc[-1]
        latest_vol = hist['Volume'].iloc[-1]
        
        # Trend Support Floors
        hist['200_EMA'] = hist['Close'].ewm(span=200, adjust=False).mean()
        hist['50_EMA'] = hist['Close'].ewm(span=50, adjust=False).mean()
        floor_200 = hist['200_EMA'].iloc[-1]
        floor_50 = hist['50_EMA'].iloc[-1]
        
        # Volume Shock Ratio (Current Vol vs 20-Day Liquidity Average)
        hist['20_Vol_Avg'] = hist['Volume'].rolling(window=20).mean()
        vol_avg_20 = hist['20_Vol_Avg'].iloc[-1]
        vol_shock_ratio = round(latest_vol / vol_avg_20, 2) if vol_avg_20 > 0 else 1.0
        
        # Distance from 52-Week High (Breakout Ceiling Proximity)
        high_52week = hist['High'].max()
        dist_from_high = round(((high_52week - latest_close) / high_52week) * 100, 2)
        
        # Pure Mathematical RSI Calculation (14-Day Momentum Window)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        rsi_14 = round(hist['RSI'].iloc[-1], 2) if not np.isnan(hist['RSI'].iloc[-1]) else 50.0

        # --- CORE FINANCIAL RATIOS & QUALITY ALIGNMENTS ---
        ratios = {
            "Trailing P/E": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "PEG Ratio": info.get("pegRatio", "N/A"),
            "Gross Margin (%)": round(info.get("grossMargins", 0) * 100, 2) if info.get("grossMargins") else "N/A",
            "Operating Margin (%)": round(info.get("operatingMargins", 0) * 100, 2) if info.get("operatingMargins") else "N/A",
            "Net Profit Margin (%)": round(info.get("profitMargins", 0) * 100, 2) if info.get("profitMargins") else "N/A",
            "Return on Equity (%)": round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else "N/A",
            "Debt to Equity": info.get("debtToEquity", "N/A"),
            "Current Ratio": info.get("currentRatio", "N/A"),
            "YoY Rev Growth (%)": round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else "N/A",
            "Short % of Float": round(info.get("shortPercentOfFloat", 0) * 100, 2) if info.get("shortPercentOfFloat") else "N/A"
        }

        # --- INSTITUTIONAL FLOWS & CORPORATE SCARCITY ---
        brokerage_stance = info.get("recommendationKey", "N/A").upper()
        target_price = info.get("targetMeanPrice", np.nan)
        implied_upside = round(((target_price / latest_close) - 1) * 100, 2) if target_price and latest_close else "N/A"
        
        # Scarcity Multipliers
        inst_ownership = round(info.get("heldPercentInstitutions", 0) * 100, 2) if info.get("heldPercentInstitutions") else "N/A"
        insider_ownership = round(info.get("heldPercentInsiders", 0) * 100, 2) if info.get("heldPercentInsiders") else "N/A"

        # --- GEOPOLITICAL AND MACRO SENTIMENT MONITOR ---
        news_feed = ticker.news
        macro_signals = {
            "Trump / Tariffs / Trade Policy": 0,
            "China / Geopolitics / Export Controls": 0,
            "Elon Musk / Institutional Tech Backing": 0,
            "NVIDIA / AI Data Center Demand Acceleration": 0
        }
        intercepted_headlines = []
        for article in news_feed:
            title = article.get("title", "").lower()
            hit = False
            if any(x in title for x in ["trump", "tariff", "white house", "policy"]):
                macro_signals["Trump / Tariffs / Trade Policy"] += 1
                hit = True
            if any(x in title for x in ["china", "blacklist", "beijing", "export"]):
                macro_signals["China / Geopolitics / Export Controls"] += 1
                hit = True
            if any(x in title for x in ["musk", "elon", "xai", "tesla"]):
                macro_signals["Elon Musk / Institutional Tech Backing"] += 1
                hit = True
            if any(x in title for x in ["nvidia", "huang", "blackwell", "h100", "ai server"]):
                macro_signals["NVIDIA / AI Data Center Demand Acceleration"] += 1
                hit = True
            if hit:
                intercepted_headlines.append(f"• {article.get('title')} ({article.get('publisher')})")

        # --- ALGORITHMIC CONVICTION SCORING MODEL ---
        score = 40  # Base line posture
        if latest_close > floor_200: score += 15       # Trend filter rule 1
        if latest_close > floor_50: score += 10        # Trend filter rule 2
        if vol_shock_ratio >= 1.5: score += 15         # Liquidity compression rule
        if dist_from_high <= 12.0: score += 10         # Ceiling breakout proximity rule
        if rsi_14 >= 55.0 and rsi_14 <= 72.0: score += 10  # Ideal velocity range rule

        return {
            "Ticker": ticker_symbol, "Spot": round(latest_close, 2), "50_EMA": round(floor_50, 2), "200_EMA": round(floor_200, 2),
            "Vol_Shock": vol_shock_ratio, "Ceiling_Dist": dist_from_high, "RSI": rsi_14,
            "Ratios": ratios, "Consensus": brokerage_stance, "Target": target_price, "Upside": implied_upside,
            "Institutions": inst_ownership, "Insiders": insider_ownership, "Macro": macro_signals, "Headlines": intercepted_headlines[:5], "Score": score
        }
    except: return None

# 3. INTERFACE ARCHITECTURE
st.title("🦅 Institutional Multi-Factor Breakout Engine")
st.markdown("Production-grade execution deck compiling Technical Velocity, Liquidity Shocks, Corporate Float Scarcity, and Geopolitical Sentiment Strands.")
st.divider()

# Workspace Configuration Matrix
workspace = st.sidebar.radio("Active Allocation Desk:", ["US Tech & Structural Growth", "India Local CapEx & Defense Localization"])

# High-Conviction Discovery Idea Hotkeys
st.sidebar.markdown("---")
st.sidebar.markdown("**💡 High-Conviction Idea Proxies:**")
if workspace == "US Tech & Structural Growth":
    st.sidebar.caption("Infrastructure Enablers: VRT, CLS, FN, DELL, MU, NVDA")
    default_assets = "MU,DELL,VRT,NVDA"
else:
    st.sidebar.caption("Local CapEx & Defense: BEL.NS, HAL.NS, DIXON.NS, KAYNES.NS")
    default_assets = "BEL.NS,HAL.NS,DIXON.NS"

tickers_raw = st.sidebar.text_area("Tracked Matrix Sandbox:", default_assets)
watchlist = [t.strip().upper() for t in tickers_raw.split(",") if t.strip()]

db = {}
with st.spinner("Processing live institutional data streams, technical momentum matrices, and order flows..."):
    for asset in watchlist:
        res = pull_institutional_intelligence(asset)
        if res: db[asset] = res

if db:
    # Build Master Leaderboard Arrays
    table_leaderboard = [{
        "Asset": k, "Price": v["Spot"], "Vol Shock Ratio": v["Vol_Shock"], "RSI (14)": v["RSI"],
        "Dist from 52W High": f"{v['Ceiling_Dist']}%", "Institutional Float": f"{v['Institutions']}%",
        "Algorithmic Conviction Score": v["Score"], "Wall Street Stance": v["Consensus"], "Implied Upside": f"{v['Upside']}%"
    } for k, v in db.items()]
    df_main = pd.DataFrame(table_leaderboard).sort_values(by="Algorithmic Conviction Score", ascending=False)
    
    # Render Interactive Operational Tabs
    tab_rankings, tab_fundamentals, tab_liquidity, tab_geopolitics, tab_ai_payload = st.tabs([
        "📊 Breakout Score Rankings", "📈 Core Financial Array", "💧 Liquidity & Technical Velocity", "🌍 Geopolitical Narrative Scanner", "📑 AI Prompt Payload Generator"
    ])
    
    with tab_rankings:
        st.subheader("System Portfolio Conviction Rankings")
        st.dataframe(df_main, use_container_width=True)
        
    with tab_fundamentals:
        st.subheader("Deep Quality & Capital Allocation Matrix")
        st.dataframe(pd.DataFrame({k: v["Ratios"] for k, v in db.items()}).T, use_container_width=True)
        
    with tab_liquidity:
        st.subheader("Order Flow Volume Shocks & Momentum Vectors")
        table_liq = [{
            "Asset": k, "Price": v["Spot"], "50 Day EMA": v["50_EMA"], "200 Day EMA Floors": v["200_EMA"], 
            "Volume Shock (Multiplier)": v["Vol_Shock"], "RSI Position": v["RSI"], "Proximity to Breakout Ceiling": f"{v['Ceiling_Dist']}%"
        } for k, v in db.items()]
        st.dataframe(pd.DataFrame(table_liq), use_container_width=True)
        
    with tab_geopolitics:
        st.subheader("Real-Time Policy & Intercepted Press Wire Hits")
        focus = st.selectbox("Select Target Asset to Audit:", list(db.keys()))
        col_m, col_n = st.columns([1, 2])
        with col_m:
            st.write(pd.DataFrame([db[focus]["Macro"]]).T.rename(columns={0: "Keyword Hits"}))
        with col_n:
            st.markdown("**Latest High-Relevance Intercepted Headlines:**")
            if db[focus]["Headlines"]:
                for hl in db[focus]["Headlines"]: st.caption(hl)
            else:
                st.write("*No direct geopolitical or structural policy mentions tracked within the current market cycle.*")
                
    with tab_ai_payload:
        st.subheader("Complete Multi-Factor Data Package")
        st.markdown("Copy the compiled data container block below and drop it into your AI interaction pane.")
        
        package_body = f"=== ADVANCED INSTITUTIONAL CONVICTION STOCK DATA INPUT BLOCK ===\n"
        package_body += f"METADATA: SECTOR_WORKSPACE={workspace} | COMPILED_CYCLE_DATE=2026_MATRIX\n\n"
        for k, v in db.items():
            package_body += f"## QUANT STRATEGY TARGET: {k} | ALGORITHMIC SCORE: {v['Score']}/100\n"
            package_body += f"- TECHNICAL MOMENTUM VELOCITY: Last Spot Price={v['Spot']} | 50 EMA Trend Line={v['50_EMA']} | 200 EMA Support Floor={v['200_EMA']}\n"
            package_body += f"- LIQUIDITY ALERT STIMULUS: Volume Shock Ratio={v['Vol_Shock']}x Average Daily Flow | Distance from 52-Week High Breakout Ceiling={v['Ceiling_Dist']}% | 14-Day RSI Vector={v['RSI']}\n"
            package_body += f"- SCARCITY & INSTITUTIONAL FOOTPRINT: Percent Held by Big Institutions={v['Institutions']}% | Corporate Insiders Stake={v['Insiders']}%\n"
            package_body += f"- BROKERAGE CONVERSATION PATHWAYS: Big House Consensus Stance={v['Consensus']} | Target Projections Value={v['Target']} ({v['Upside']}% Implied Growth Runway Plan)\n"
            package_body += f"- granULAR BALANCE SHEET RATIOS: {str(v['ratios'] if 'ratios' in v else v['Ratios'])}\n"
            package_body += f"- POLICY & GEOPOLITICAL EXPOSURE METRICS: {str(v['Macro'])}\n"
            package_body += "---------------------------------------------------------------------------------\n"
        package_body += "\n=== MASTER SYSTEM INSTRUCTION FOR SYSTEM ANALYST ===\n"
        package_body += "You are acting as the Chief Investment Officer and Lead Cross-Market Systematic Trader. Audit the multi-factor technical velocity vectors, institutional scarcity footprints, balance sheet growth runways, and geopolitical policy exposure datasets provided above.\n\n"
        package_body += "Isolate which specific ticker showcases the single highest structural alignment for a massive explosive breakout. Cross-reference low distance from 52-week highs with high volume shocks ($>1.5x$), strong profit margins, and macro windfalls (e.g., Trump tariff positioning, local Indian CapEx defense budgets).\n\n"
        package_body += "Compile a granular, elite trading intelligence review evaluating pricing entries and structural moats, and conclude with a razor-sharp, definitive 10-line executive summary layout summarizing precise Buy, Sell, or Avoid decisions for each target ticker."
        
        st.code(package_body, language="text")
else:
    st.error("Infrastructure online. Waiting for valid active asset ticker inputs in the text block sidebar.")

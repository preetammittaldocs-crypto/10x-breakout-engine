import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 1. PAGE SETUP & STYLE
st.set_page_config(page_title="Institutional Breakout Matrix", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background-color: #0f172a; }
    .stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. BULLETPROOF DATA ACCELERATOR
@st.cache_data(ttl=600)
def pull_safe_intelligence(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Pull 1-Year historical pricing data (Highly stable cloud endpoint)
        hist = ticker.history(period="1y")
        if hist.empty:
            return None
            
        latest_close = hist['Close'].iloc[-1]
        latest_vol = hist['Volume'].iloc[-1]
        
        # Calculate Trend Support Lines
        hist['200_EMA'] = hist['Close'].ewm(span=200, adjust=False).mean()
        hist['50_EMA'] = hist['Close'].ewm(span=50, adjust=False).mean()
        floor_200 = hist['200_EMA'].iloc[-1]
        floor_50 = hist['50_EMA'].iloc[-1]
        
        # Calculate Liquidity Volume Shock (Current Vol vs 20-Day Volume Avg)
        hist['20_Vol_Avg'] = hist['Volume'].rolling(window=20).mean()
        vol_avg_20 = hist['20_Vol_Avg'].iloc[-1]
        vol_shock = round(latest_vol / vol_avg_20, 2) if vol_avg_20 > 0 else 1.0
        
        # Calculate Proximity to Breakout Ceiling (Distance from 52-Week High)
        high_52w = hist['High'].max()
        dist_high = round(((high_52w - latest_close) / high_52w) * 100, 2)
        
        # Pure Mathematical RSI-14 Engine (Zero dependencies)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        rsi_14 = round(hist['RSI'].iloc[-1], 2) if not np.isnan(hist['RSI'].iloc[-1]) else 50.0

        # Secure Fallback Mechanism for Server Blocks
        info = {}
        try:
            info = ticker.info
            if not info or not isinstance(info, dict):
                info = {}
        except:
            info = {}

        # Extract values with clear safety nets
        ratios = {
            "Trailing P/E": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "PEG Ratio": info.get("pegRatio", "N/A"),
            "Gross Margin (%)": round(info.get("grossMargins", 0) * 100, 2) if info.get("grossMargins") else "N/A",
            "Operating Margin (%)": round(info.get("operatingMargins", 0) * 100, 2) if info.get("operatingMargins") else "N/A",
            "Debt to Equity": info.get("debtToEquity", "N/A"),
            "YoY Rev Growth (%)": round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else "N/A",
            "Short % of Float": round(info.get("shortPercentOfFloat", 0) * 100, 2) if info.get("shortPercentOfFloat") else "N/A"
        }
        
        consensus = info.get("recommendationKey", "DATA_STREAM_LAG").upper()
        target = info.get("targetMeanPrice", "N/A")
        inst_float = round(info.get("heldPercentInstitutions", 0) * 100, 2) if info.get("heldPercentInstitutions") else "N/A"

        # Algorithmic Scoring Model
        score = 40
        if latest_close > floor_200: score += 15
        if latest_close > floor_50: score += 10
        if vol_shock >= 1.5: score += 15
        if dist_high <= 10.0: score += 10
        if rsi_14 >= 53.0 and rsi_14 <= 70.0: score += 10

        return {
            "Ticker": ticker_symbol, "Spot": round(latest_close, 2), "50_EMA": round(floor_50, 2), "200_EMA": round(floor_200, 2),
            "Vol_Shock": vol_shock, "Ceiling_Dist": dist_high, "RSI": rsi_14, "Ratios": ratios,
            "Consensus": consensus, "Target": target, "Institutions": inst_float, "Score": score
        }
    except:
        return None

# 3. INTERFACE BUILDER
st.title("🦅 Institutional Multi-Factor Breakout Engine")
st.markdown("Algorithmic matrix scoring price momentum velocity, institutional volume shock flows, and consolidation breakout ceilings.")
st.divider()

# Selection Sidebar Desk
workspace = st.sidebar.radio("Active Allocation Desk:", ["US Tech & Structural Growth", "India Local CapEx & Defense Localization"])

st.sidebar.markdown("---")
st.sidebar.markdown("**💡 High-Conviction Core Watchlist:**")
if workspace == "US Tech & Structural Growth":
    st.sidebar.caption("Suggested Infrastructure: NVDA, DELL, VRT, MU, IBM")
    tickers_input = st.sidebar.text_area("Tracked Matrix Sandbox:", "NVDA,DELL,VRT,MU")
else:
    st.sidebar.caption("Suggested Structural Capex: BEL.NS, HAL.NS, DIXON.NS, KAYNES.NS")
    tickers_input = st.sidebar.text_area("Tracked Matrix Sandbox:", "BEL.NS,HAL.NS,DIXON.NS")

watchlist = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

db = {}
if watchlist:
    for asset in watchlist:
        res = pull_safe_intelligence(asset)
        if res:
            db[asset] = res

if db:
    # Build data frames
    table_rankings = [{
        "Asset": k, "Spot Price": v["Spot"], "Volume Shock Ratio": f"{v['Vol_Shock']}x", 
        "RSI (14)": v["RSI"], "Distance from 52W High": f"{v['Ceiling_Dist']}%", 
        "Algorithmic Breakout Score": v["Score"], "Brokerage Stance": v["Consensus"]
    } for k, v in db.items()]
    df_main = pd.DataFrame(table_rankings).sort_values(by="Algorithmic Breakout Score", ascending=False)

    tab_rankings, tab_liquidity, tab_fundamentals, tab_ai_payload = st.tabs([
        "📊 Breakout Score Rankings", "💧 Liquidity & Technical Velocity", "📈 Core Financial Array", "📑 AI Prompt Payload Generator"
    ])

    with tab_rankings:
        st.subheader("System Portfolio Conviction Rankings")
        st.dataframe(df_main, use_container_width=True, hide_index=True)

    with tab_liquidity:
        st.subheader("Order Flow Volume Shocks & Velocity Vectors")
        table_liq = [{
            "Asset": k, "Current Spot": v["Spot"], "50 Day EMA Trend": v["50_EMA"], "200 Day EMA Floor": v["200_EMA"],
            "Volume Shock Alert": v["Vol_Shock"], "RSI Position": v["RSI"], "Breakout Proximity": f"{v['Ceiling_Dist']}%"
        } for k, v in db.items()]
        st.dataframe(pd.DataFrame(table_liq), use_container_width=True, hide_index=True)

    with tab_fundamentals:
        st.subheader("Deep Quality & Balance Sheet Matrix")
        st.dataframe(pd.DataFrame({k: v["Ratios"] for k, v in db.items()}).T, use_container_width=True)

    with tab_ai_payload:
        st.subheader("Complete Multi-Factor Data Package")
        st.markdown("Copy the compiled data container block below and drop it into your AI interaction pane.")

        package_body = f"=== ADVANCED INSTITUTIONAL CONVICTION STOCK DATA INPUT BLOCK ===\n"
        package_body += f"METADATA: SECTOR_WORKSPACE={workspace} | DATA_CYCLE_POSTURE=2026_CORE\n\n"
        for k, v in db.items():
            package_body += f"## QUANT STRATEGY TARGET: {k} | ALGORITHMIC BREAKOUT SCORE: {v['Score']}/100\n"
            package_body += f"- TECHNICAL MOMENTUM VELOCITY: Last Spot Price={v['Spot']} | 50 EMA Trend Line={v['50_EMA']} | 200 EMA Support Floor={v['200_EMA']}\n"
            package_body += f"- LIQUIDITY ALERT STIMULUS: Volume Shock Ratio={v['Vol_Shock']}x Average Daily Flow | Distance from 52-Week High Breakout Ceiling={v['Ceiling_Dist']}% | 14-Day RSI Vector={v['RSI']}\n"
            package_body += f"- SCARCITY & INSTITUTIONAL FOOTPRINT: Percent Held by Big Institutions={v['Institutions']}%\n"
            package_body += f"- BROKERAGE CONVERSATION PATHWAYS: Big House Consensus Stance={v['Consensus']} | Target Projections Value={v['Target']}\n"
            package_body += f"- GRANULAR BALANCE SHEET RATIOS: {str(v['Ratios'])}\n"
            package_body += "---------------------------------------------------------------------------------\n"
        package_body += "\n=== MASTER SYSTEM INSTRUCTION FOR SYSTEM ANALYST ===\n"
        package_body += "You are acting as the Chief Investment Officer and Lead Cross-Market Systematic Trader. Audit the multi-factor technical velocity vectors, volume shocks, and consolidation breakout ceilings provided above.\n\n"
        package_body += "Isolate which specific ticker showcases the single highest structural alignment for a massive explosive breakout. Cross-reference low distance from 52-week highs with high volume shocks ($>1.5x$), strong profit margins, and market momentum.\n\n"
        package_body += "Compile a granular, elite trading intelligence review evaluating pricing entries and structural trends, and conclude with a razor-sharp, definitive 10-line executive summary layout summarizing precise Buy, Sell, or Avoid decisions for each target ticker."

        st.code(package_body, language="text")
else:
    st.info("Input recognized. Pulling data streams from market exchanges... If it stays blank, type a stock ticker manually in the sidebar sandbox box.")

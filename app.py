import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 1. PAGE SETUP
st.set_page_config(page_title="Alpha Macro & Micro Ingestion Command", layout="wide")

st.markdown("""
    <style>
    .macro-card {
        background-color: #0f172a;
        color: #38bdf8;
        padding: 15px;
        border-radius: 8px;
        font-family: monospace;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ADVANCED DATA INGESTION ENGINE
@st.cache_data(ttl=1200)
def pull_comprehensive_intelligence_desk(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Live Price Tape & Trend Posture
        hist = ticker.history(period="1y")
        if hist.empty: return None
        latest_close = hist['Close'].iloc[-1]
        latest_vol = hist['Volume'].iloc[-1]
        hist['200_EMA'] = hist['Close'].ewm(span=200, adjust=False).mean()
        hist['20_Vol_Avg'] = hist['Volume'].rolling(window=20).mean()
        
        # 12+ Institutional Financial Ratios
        ratios = {
            "Trailing P/E": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "PEG Ratio": info.get("pegRatio", "N/A"),
            "Price to Sales": info.get("priceToSalesTrailing12Months", "N/A"),
            "EV/EBITDA": info.get("enterpriseToEbitda", "N/A"),
            "Gross Margin (%)": round(info.get("grossMargins", 0) * 100, 2) if info.get("grossMargins") else "N/A",
            "Operating Margin (%)": round(info.get("operatingMargins", 0) * 100, 2) if info.get("operatingMargins") else "N/A",
            "Net Profit Margin (%)": round(info.get("profitMargins", 0) * 100, 2) if info.get("profitMargins") else "N/A",
            "Return on Equity (%)": round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else "N/A",
            "Debt to Equity": info.get("debtToEquity", "N/A"),
            "Current Ratio": info.get("currentRatio", "N/A"),
            "YoY Rev Growth (%)": round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else "N/A",
            "Short % of Float": round(info.get("shortPercentOfFloat", 0) * 100, 2) if info.get("shortPercentOfFloat") else "N/A"
        }

        # Brokerage Ratings & Big House Consensus Target Prices
        brokerage_consensus = info.get("recommendationKey", "N/A").upper()
        target_price = info.get("targetMeanPrice", np.nan)
        implied_upside = ((target_price / latest_close) - 1) * 100 if target_price and latest_close else 0
        total_firms = info.get("numberOfAnalystOpinions", 0)

        # Macro Narrative Scanners (Live News Scanning)
        news_feed = ticker.news
        macro_signals = {
            "Donald Trump / Tariffs / Trade Policy": 0,
            "China / Geopolitics / Blacklists": 0,
            "Elon Musk / Big Tech Founders": 0,
            "NVIDIA / Jensen Huang / AI Demand": 0,
            "Corporate Strategic Pivot": 0
        }
        intercepted_headlines = []

        for article in news_feed:
            title = article.get("title", "").lower()
            hit = False
            if any(x in title for x in ["trump", "tariff", "white house", "policy"]):
                macro_signals["Donald Trump / Tariffs / Trade Policy"] += 1
                hit = True
            if any(x in title for x in ["china", "blacklist", "beijing", "tariff"]):
                macro_signals["China / Geopolitics / Blacklists"] += 1
                hit = True
            if any(x in title for x in ["musk", "elon", "tesla", "bezos", "amazon"]):
                macro_signals["Elon Musk / Big Tech Founders"] += 1
                hit = True
            if any(x in title for x in ["nvidia", "huang", "ai server", "chips"]):
                macro_signals["NVIDIA / Jensen Huang / AI Demand"] += 1
                hit = True
            if any(x in title for x in ["pivot", "restructure", "acquire", "spin-off", "shift"]):
                macro_signals["Corporate Strategic Pivot"] += 1
                hit = True
            if hit:
                intercepted_headlines.append(f"• {article.get('title')} ({article.get('publisher')})")

        # System Scoring
        score = 50
        if latest_close > hist['200_EMA'].iloc[-1]: score += 25
        if latest_vol > hist['20_Vol_Avg'].iloc[-1] * 1.3: score += 25

        return {
            "Ticker": ticker_symbol, "Spot": round(latest_close, 2), "200_EMA": round(hist['200_EMA'].iloc[-1], 2),
            "Ratios": ratios, "Consensus": brokerage_consensus, "Target": round(target_price, 2) if not np.isnan(target_price) else "N/A",
            "Upside": round(implied_upside, 2), "Coverage": total_firms, "Macro": macro_signals, "Headlines": intercepted_headlines[:5], "Score": score
        }
    except: return None

# 3. INTERFACE BUILDER
st.title("🦅 Alpha Multi-Factor Ingestion Workspace")
st.markdown("Automated system parsing real-time technical indicators, 12+ metrics, brokerage trends, and political news streams.")
st.hr()

workspace = st.sidebar.radio("Active Desk Desk:", ["US Secular Growth Core", "Indian Structural Rotations"])
default_tickers = "MU,DELL,IBM,NVDA,NOK" if workspace == "US Secular Growth Core" else "BEL.NS,HAL.NS,DIXON.NS"
tickers_raw = st.sidebar.text_area("Tracked Assets (Comma Separated):", default_tickers)
watchlist = [t.strip().upper() for t in tickers_raw.split(",") if t.strip()]

db = {}
with st.spinner("Compiling live fundamental, technical, and macro news streams..."):
    for asset in watchlist:
        res = pull_comprehensive_intelligence_desk(asset)
        if res: db[asset] = res

if db:
    table_data = [{"Asset": k, "Price": v["Spot"], "200 EMA Floor": v["200_EMA"], "Conviction Score": v["Score"], "Big House Consensus": v["Consensus"], "Implied Growth Upside": f"{v['Upside']}%"} for k, v in db.items()]
    df_main = pd.DataFrame(table_data).sort_values(by="Conviction Score", ascending=False)
    
    tab_leaderboard, tab_ratios, tab_macro, tab_ai_payload = st.tabs(["📊 Conviction Leaderboard", "📈 12-Core Financial Ratios", "🌍 Geopolitical News Monitor", "📑 AI Code Prompt Generator"])
    
    with tab_leaderboard:
        st.subheader("System Portfolio Conviction Rankings")
        st.dataframe(df_main, use_container_width=True)
        
    with tab_ratios:
        st.subheader("Deep Granular Fundamental Matrix")
        st.dataframe(pd.DataFrame({k: v["Ratios"] for k, v in db.items()}).T, use_container_width=True)
        
    with tab_macro:
        st.subheader("Macro Policy & Founder Context Tracking")
        focus = st.selectbox("Select Target Asset to Inspect:", list(db.keys()))
        col_metrics, col_news = st.columns([1, 2])
        with col_metrics:
            st.write(pd.DataFrame([db[focus]["Macro"]]).T.rename(columns={0: "Keyword Hits Found"}))
        with col_news:
            st.markdown("**Relevant Intercepted Headlines:**")
            if db[focus]["Headlines"]:
                for hl in db[focus]["Headlines"]: st.caption(hl)
            else:
                st.write("*No direct political or founder mentions identified in this 24-hour window.*")
        
    with tab_ai_payload:
        st.subheader("Copy-Paste Data Prompt Package")
        st.markdown("Copy the entire code text container below and drop it into your external AI window.")
        
        package_body = f"=== CONVICTION STOCK DATA INPUT BLOCK ===\n"
        package_body += f"METADATA: TARGET_WORKSPACE={workspace}\n\n"
        for k, v in db.items():
            package_body += f"## ASSET TRACKER: {k}\n"
            package_body += f"- TECHNICAL POSTURE: Spot Price={v['Spot']} (200 EMA Support Floor={v['200_EMA']})\n"
            package_body += f"- SYSTEMIC CONVICTION SCORE: {v['Score']}/100\n"
            package_body += f"- BROKERAGE VECTORS: Consensus Rating Stance={v['Consensus']}, Target Price Projection={v['Target']} ({v['Upside']}% Implied Growth Runway) across {v['Coverage']} firms\n"
            package_body += f"- KEY FINANCIAL RATIOS: {str(v['Ratios'])}\n"
            package_body += f"- GEOPOLITICAL SENTIMENT EXPOSURE: {str(v['Macro'])}\n"
            package_body += "---------------------------------------------------------\n"
        package_body += "\n=== SYSTEM INSTRUCTION ===\n"
        package_body += "You are acting as an elite Institutional Technology and Macro Equity Analyst. Process the real-time financial metrics, brokerage actions, and geopolitical policy keyword data blocks supplied above.\n\n"
        package_body += "Provide a comprehensive market analysis report detailing which companies show clear indicators of 10x breakout potential. Highlight corporate transitions, macro trade policy alignments, and valuation margins.\n\n"
        package_body += "Conclude your analysis with a strict 10-line executive summary report summarizing all major metric changes, technical support floor breakouts, and your definitive buy/avoid decisions for each ticker."
        
        st.code(package_body, language="text")
else:
    st.error("Connection established, but no stock metrics were pulled. Verify your ticker spellings in the sidebar container.")

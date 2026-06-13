import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Alpha Command Center", layout="wide")

@st.cache_data(ttl=1200)
def pull_comprehensive_intelligence_desk(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        hist = ticker.history(period="1y")
        if hist.empty: return None
        
        latest_close = hist['Close'].iloc[-1]
        latest_vol = hist['Volume'].iloc[-1]
        hist['200_EMA'] = hist['Close'].ewm(span=200, adjust=False).mean()
        hist['20_Vol_Avg'] = hist['Volume'].rolling(window=20).mean()
        
        ratios = {
            "Trailing P/E": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "PEG Ratio": info.get("pegRatio", "N/A"),
            "YoY Rev Growth (%)": round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else "N/A",
            "Short % of Float": round(info.get("shortPercentOfFloat", 0) * 100, 2) if info.get("shortPercentOfFloat") else "N/A"
        }

        news_feed = ticker.news
        macro_signals = {"Trump / Policy": 0, "China / Geopolitics": 0, "AI / Infrastructure": 0}

        for article in news_feed:
            title = article.get("title", "").lower()
            if any(x in title for x in ["trump", "tariff", "trade"]): macro_signals["Trump / Policy"] += 1
            if any(x in title for x in ["china", "blacklist"]): macro_signals["China / Geopolitics"] += 1
            if any(x in title for x in ["nvidia", "huang", "ai"]): macro_signals["AI / Infrastructure"] += 1

        score = 50
        if latest_close > hist['200_EMA'].iloc[-1]: score += 25
        if latest_vol > hist['20_Vol_Avg'].iloc[-1] * 1.3: score += 25

        return {
            "Ticker": ticker_symbol, "Spot": round(latest_close, 2), "200_EMA": round(hist['200_EMA'].iloc[-1], 2),
            "Ratios": ratios, "Macro": macro_signals, "Score": score
        }
    except: return None

st.title("🦅 Alpha Core Ingestion Matrix")
workspace = st.sidebar.radio("Active Desk:", ["US Secular Growth Core", "Indian Structural Rotations"])
default_tickers = "MU,DELL,IBM,NVDA" if workspace == "US Secular Growth Core" else "BEL.NS,HAL.NS,DIXON.NS"
tickers_raw = st.sidebar.text_area("Tracked Assets:", default_tickers)
watchlist = [t.strip().upper() for t in tickers_raw.split(",") if t.strip()]

db = {}
for asset in watchlist:
    res = pull_comprehensive_intelligence_desk(asset)
    if res: db[asset] = res

if db:
    table_data = [{"Asset": k, "Price": v["Spot"], "200 EMA Floor": v["200_EMA"], "Breakout Score": v["Score"]} for k, v in db.items()]
    df_main = pd.DataFrame(table_data).sort_values(by="Breakout Score", ascending=False)
    
    tab_boards, tab_ratios, tab_ai_payload = st.tabs(["📊 Strategy Leaderboard", "📈 Core Metrics", "📑 AI Code Prompt"])
    
    with tab_boards:
        st.dataframe(df_main, use_container_width=True)
    with tab_ratios:
        st.dataframe(pd.DataFrame({k: v["Ratios"] for k, v in db.items()}).T, use_container_width=True)
    with tab_ai_payload:
        package_body = f"=== CONVICTION STOCK DATA INPUT BLOCK ===\n"
        for k, v in db.items():
            package_body += f"## ASSET: {k} | SCORE: {v['Score']}/100\n- Price: {v['Spot']} (200 EMA: {v['200_EMA']})\n- Metrics: {str(v['Ratios'])}\n- Macro Mentions: {str(v['Macro'])}\n\n"
        package_body += "=== INSTRUCTION ===\nProvide a thorough macro structural analysis based on these metrics and compile a concise 10-line executive summary report."
        st.code(package_body, language="text")

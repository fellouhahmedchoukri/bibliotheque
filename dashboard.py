import streamlit as st
from core.trading_engine import TradingEngine

engine = TradingEngine()
st.title("Dashboard de Trading")

# Afficher les positions ouvertes
positions = engine.get_open_positions()
st.subheader(f"Positions ouvertes: {len(positions)}")
st.dataframe(positions)

# Performance des stratégies
performance = engine.get_strategy_performance()
st.bar_chart(performance.set_index('strategy')['profit'])

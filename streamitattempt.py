import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Coherix.utils.wavelet_utils import pull_data, workflow  # reuse your existing functions

# -- API Key --
API_KEY = 'jjeryxeZXNkBhTEQF0SDj8uBBI_N1dBM'

st.title("Wavelet Coherence Visualizer")

ticker1 = st.text_input("Stock 1 Ticker", "CL")
ticker2 = st.text_input("Stock 2 Ticker", "ES")

max_period = st.slider("Max Period (days)", min_value=20, max_value=250, value=125, step=5)
min_period = st.slider("Min Period (days)", min_value=2, max_value=50, value=8, step=1)

show_phase = st.checkbox("Show Phase Arrows", value=True)

if st.button("Run Analysis"):
    try:
        sig1 = pull_data(ticker1, API_KEY)[2]
        sig2 = pull_data(ticker2, API_KEY)[2]
        bounds = (max_period, min_period)

        freqs, S12, coh = workflow(sig1, sig2, bounds, phase=show_phase)

        # Streamlit needs to render plots explicitly
        st.pyplot(plt.gcf())

    except Exception as e:
        st.error(f"Error: {e}")

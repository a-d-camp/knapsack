import streamlit as st
import pandas as pd
import os
from knapsack import *

st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 25px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

st.title("Solve the Knapsack Problem")
ortools_url = 'https://developers.google.com/optimization/pack/knapsack?hl=en'
github_url = 'https://github.com/a-d-camp/knapsack'
st.markdown("Built by [Andrew Camp](%s) &nbsp; | &nbsp; Solved with [Google OR Tools](%s)" % (github_url, ortools_url))

# read data
df_summary = pd.read_csv('./data/knapsack_summary.csv')

# download summary
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df_summary)
st.download_button(
    label="Download Summary Results for All Files",
    data=csv,
    file_name='knapsack_results.csv',
    mime='text/csv',
)

# file selector
pth = './data/knapsack-data'
files = os.listdir(pth)
option = st.selectbox(
    'Select a knapsack data file to solve a single problem', files, index = 1)

# solve model
kp_mod = knapsack_model(os.path.join(pth, option))
kp_mod.solve_model()
data = kp_mod.parse_output()
data['solve_time'] = round(data['solve_time'], 3) if data['solve_time'] < 1 else round(data['solve_time'], 1)

# display packed items
df = pd.DataFrame({
    'Packed Item Index': data['packed_items'],
    'Weight': data['packed_weights'],
    'Value': data['packed_values']
    })

# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# display metrics
st.header('Solution Metrics')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Available Items", data['n_avail_items'], 'items')
col2.metric("Packed Items", len(data['packed_items']), 'items')
col3.metric("Solve Time", data['solve_time'], "seconds")
col4.metric("Knapsack Value", data['obj_val'], 'objective')
col5.metric("Knapsack Capacity", data['capacity'], 'max weight')

# display dataframe
st.header('Packed Item Results')
styler = df.style.hide_index().format(decimal=',')
st.write(styler.to_html(), unsafe_allow_html=True)

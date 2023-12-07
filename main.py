import pandas as pd
import streamlit as st
import plotly.express as px
from secondary_defs import *
st.set_page_config(
    layout = "wide"
)

@st.cache_resource(
        show_spinner = """
Reading data for graphs. Please, wait
"""
)
def read_total_data():
    df_registration_dynamic_by_country = read_registration_dynamic_by_country()

    return df_registration_dynamic_by_country


df_registration_dynamic_by_country = read_total_data()


def draw_graph_registration_dynamic_by_country(
        df_registration_dynamic_by_country: pd.DataFrame
) -> None:
    fig = px.line(
        df_registration_dynamic_by_country,
        x = "date",
        y = "new_registration_count",
        color = "country",
        markers = True,
        symbol = "country",
        title = "Dynamics of new registrations by country"
    )

    fig.update_xaxes(
        title_text = "Date"
    )

    fig.update_yaxes(
        title_text = "New registration count"
    )
    
    st.plotly_chart(
        fig,
        use_container_width = True
    )


### FIRST ###

graph, table = st.tabs(
    [
        "Graph",
        "Table"
    ]
)
with graph:
    draw_graph_registration_dynamic_by_country(df_registration_dynamic_by_country)
with table:
    st.dataframe(
        df_registration_dynamic_by_country,
        use_container_width = True,
        hide_index = True,
        column_config = {
            "date": st.column_config.DateColumn()
        }
    )
st.divider()



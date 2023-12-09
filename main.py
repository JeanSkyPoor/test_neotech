import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from secondary_defs import *

st.set_page_config(
    layout = "wide"
)

@st.cache_data(
        ttl = 3600,
        show_spinner = """
Reading data for graphs. Please, wait
"""
)
def read_total_data():
    df_registration_dynamic_by_country = read_registration_dynamic_by_country()
    df_first_deposits_dynamic_by_country = read_first_deposits_dynamic_by_country()
    df_conversion_from_regist_to_deposit = read_conversion_from_regist_to_deposit()
    df_same_date_deposit = read_same_date_deposit()
    df_funnel_area = read_funnel_area()

    returned_tuple = (
        df_registration_dynamic_by_country,
        df_first_deposits_dynamic_by_country,
        df_conversion_from_regist_to_deposit,
        df_same_date_deposit,
        df_funnel_area
    )

    return returned_tuple


total_data = read_total_data()


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
        title_text = "Date",
        showspikes = True
    )

    fig.update_yaxes(
        title_text = "New registration count",
        showspikes = True
    )
    
    st.plotly_chart(
        fig,
        use_container_width = True
    )


def draw_graph_first_deposits_dynamic_by_country(
        df_first_deposits_dynamic_by_country: pd.DataFrame
) -> None:
    fig = px.line(
        df_first_deposits_dynamic_by_country,
        x = "date",
        y = "first_deposit_count",
        color = "country",
        markers = True,
        symbol = "country",
        title = "Dynamics of first deposits by country"
    )

    fig.update_xaxes(
        title_text = "Date",
        showspikes = True

    )

    fig.update_yaxes(
        title_text = "First deposits count",
        showspikes = True

    )

    st.plotly_chart(
        fig,
        use_container_width = True
    )


def draw_graph_conversion_from_regist_to_deposit(
        df_conversion_from_regist_to_deposit: pd.DataFrame
) -> None:
    fig = px.line(
        df_conversion_from_regist_to_deposit,
        x = "date",
        y = "conversion, %",
        color = "country",
        markers = True,
        symbol = "country",
        title = "Conversion, %"
    )

    fig.update_xaxes(
        title_text = "Date",
        showspikes = True

    )

    fig.update_yaxes(
        title_text = "Conversion from registration to deposit, %",
        showspikes = True

    )

    st.plotly_chart(
        fig,
        use_container_width = True
    )


def draw_graph_same_date_deposit(
        df_same_date_deposit: pd.DataFrame
) -> None:
    fig = px.pie(
        df_same_date_deposit,
        values = "same_date_deposit, %",
        names = "country",
        title = "Same date deposit by country, aug 2023, percentage",
        hole = 0.1
    )

    fig.update_traces(
        textinfo = "label+value",
        marker = dict(
            line = dict(
                width = 3
            )
        )
    )
    st.plotly_chart(
        fig,
        use_container_width = True
    )


def draw_graph_funnel_area(
        df_selected_country: pd.DataFrame,
        selected_country: str
) -> None:
    fig = go.Figure()
    fig.add_trace(
        go.Funnel(
        x = df_selected_country["total_deposited, usd"],
        y = df_selected_country["deposit_number"],
        textinfo = "percent initial"
        )
    )
    fig.update_layout(
        title = f"First seven deposits by {selected_country}"
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
    draw_graph_registration_dynamic_by_country(total_data[0])
with table:
    st.dataframe(
        total_data[0],
        use_container_width = True,
        hide_index = True,
        column_config = {
            "date": st.column_config.DateColumn()
        }
    )
st.divider()


### SECOND ###

graph, table = st.tabs(
    [
        "Graph",
        "Table"
    ]
)
with graph:
    draw_graph_first_deposits_dynamic_by_country(total_data[1])
with table:
    st.dataframe(
        total_data[1],
        use_container_width = True,
        hide_index = True,
        column_config = {
            "date": st.column_config.DateColumn()
        }
    )
st.divider()


### THIRD ###

graph, table = st.tabs(
    [
        "Graph",
        "Table"
    ]
)
with graph:
    draw_graph_conversion_from_regist_to_deposit(total_data[2])
with table:
    st.dataframe(
        total_data[2],
        use_container_width = True,
        hide_index = True,
        column_config = {
            "date": st.column_config.DateColumn()
        }
    )
with st.expander(
    "Немного описания, как я делал 3-е задание"
):
    st.write(
        """
Первоначально я думал, что надо просто кол-во людей, сделавших депозит в день группировки, поделить на кол-во новых регистраций.
Таким образом, у меня получалась конверсия в 272%, что кажется явной ошибкой.
Как пример: 2023-08-10 в стране Х было 100 новых регистраций и 100 пользователей совершили свой первый депозит. По этой логике, у меня
конверсия будет 100%, но среди этой второй сотни, может и не быть никого из первой сотни. Поэтому такой показатель неинформативен полностью.
"""
    )

    _,col,_ = st.columns(3)
    with col:
        st.image(
            "conversion_bug.jpg"
        )

    st.write(
        """
Поэтому было решено применить логику и здравый смысл. Суть заключается в том, что мы будем смотреть конверсию именно тех пользователей, которые зарегистрировались.
Период в задании дан весь август, поэтому я "обрезал" даты регистрации и первого депозита целым августом.
Например, возьмем 2023-08-01 и страну KZ. Мой % конверсии говорит о том, какой % пользователей, которые зарегистрировались 2023-08-01 в стране KZ
совершили свой первый депозит за период целого августа.
"""
    )
st.divider()

col_1, col_2 = st.columns(2)
with col_1:
    graph, table = st.tabs(
        [
            "Graph",
            "Table"
        ]
    )
    with graph:
        draw_graph_same_date_deposit(total_data[3])
    with table:
        st.dataframe(
            total_data[3],
            hide_index = True,
            column_config = {
                "date": st.column_config.DateColumn()
            }
        )

with col_2:
    df_funnel_area = total_data[4]
    selected_country = st.selectbox(
        "Select country",
        options = sorted(
            df_funnel_area["country"].unique()
        )
    )
    
    df_selected_country = df_funnel_area[
        df_funnel_area["country"] == selected_country
    ]

    graph, table = st.tabs(
            [
                "Graph",
                "Table"
            ]
        )
    with graph:
        draw_graph_funnel_area(
            df_selected_country,
            selected_country
        )
    with table:
        st.dataframe(
            df_selected_country,
            hide_index = True
        )
st.divider()
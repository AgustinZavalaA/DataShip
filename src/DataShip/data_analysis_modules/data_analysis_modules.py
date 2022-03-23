import numpy as np
import pandas as pd
import sklearn
from typing import Callable
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def get_active_modules() -> dict[str, tuple[Callable[..., None], bool]]:
    return {
        "Mean": (mean_module, False),
        "Median": (median_module, False),
        "Mode": (mode_module, False),
        "Standard Deviation": (std_module, False),
        "Variance": (var_module, False),
        "Linear Regression": (linear_regression_module, False),
        "Clusterization": (cluster_module, False),
        "Graphing": (graph_module, False),
    }


def mean_module(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the mean of a dataframe
    """
    return dataframe.mean().rename("Mean")


def median_module(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the median of a dataframe
    """
    return dataframe.median().rename("Median")


def mode_module(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the mode of a dataframe
    """
    return dataframe.mode(axis=0)


def std_module(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the standard deviation of a dataframe
    """
    return dataframe.std().rename("Standard Deviation")


def var_module(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the variance of a dataframe
    """
    return dataframe.var().rename("Variance")


def linear_regression_module(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the linear regression of a dataframe using sklearn
    """
    return pd.DataFrame(
        sklearn.linear_model.LinearRegression()
        .fit(dataframe, dataframe)
        .predict(dataframe)
    ).rename("Linear Regression")


def cluster_module(dataframe: pd.DataFrame, n_clusters: int) -> pd.DataFrame:
    """
    Calculate the cluster of a dataframe using sklearn
    """
    return pd.DataFrame(
        sklearn.cluster.KMeans(n_clusters=n_clusters).fit_predict(dataframe)
    ).rename("Cluster")


def graph_module(dataframe: pd.DataFrame, enable_st: bool = True) -> pd.DataFrame:
    """
    Calculate the graph of a dataframe using plotly
    """
    fig_types = ["Scatter", "Bar", "Box", "Histogram", "Pie", "Line", "Violin"]
    if enable_st:
        selected_fig_type = st.selectbox("Select a figure type", fig_types)
    else:
        selected_fig_type = fig_types[0]

    if selected_fig_type == "Scatter":
        fig = px.scatter(dataframe)
    elif selected_fig_type == "Bar":
        fig = px.bar(dataframe)
    elif selected_fig_type == "Box":
        fig = px.box(dataframe)
    elif selected_fig_type == "Histogram":
        fig = px.histogram(dataframe)
    elif selected_fig_type == "Pie":
        fig = px.pie(dataframe)
    elif selected_fig_type == "Line":
        fig = px.line(dataframe)
    else:
        fig = px.violin(dataframe)

    if enable_st:
        st.plotly_chart(fig, use_container_width=True)
    return pd.DataFrame()

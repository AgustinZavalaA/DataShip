import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from typing import Callable
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def get_active_modules() -> dict[str, tuple[Callable[..., pd.DataFrame], bool]]:
    """This function returns a dictionary of all the modules and their status"""
    return {
        "Mean": (mean_module, False),
        "Median": (median_module, False),
        "Mode": (mode_module, False),
        "Standard Deviation": (std_module, False),
        "Variance": (var_module, False),
        "Linear Regression": (linear_regression_module, False),
        "Clusterization": (cluster_module, False),
        "Graphing": (graph_module, False),
        "Mapping": (map_module, False),
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
    if len(dataframe.columns) == 1:
        # add a column of range to the dataframe
        dataframe["range"] = np.arange(len(dataframe))
        dataframe = dataframe[["range", dataframe.columns[0]]]

    if len(dataframe.columns) != 2:
        st.error(
            "Linear Regression can only be applied to dataframes with 1 or 2 columns"
        )
        return pd.DataFrame()

    # Create linear regression object
    regr = LinearRegression()

    # Train the model using the training sets
    regr.fit(dataframe.iloc[:, 0].values.reshape(-1, 1), dataframe.iloc[:, 1].values)
    y_pred = regr.predict(dataframe.iloc[:, 0].values.reshape(-1, 1))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dataframe.iloc[:, 0], y=dataframe.iloc[:, 1], mode="markers", name="Data"
        )
    )
    fig.add_trace(
        go.Scatter(x=dataframe.iloc[:, 0], y=y_pred, mode="lines", name="Prediction")
    )
    st.write(f"Linear Regression of {dataframe.columns[0]} over {dataframe.columns[1]}")
    st.plotly_chart(fig, use_container_width=True)
    return pd.DataFrame()


def cluster_module(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the cluster of a dataframe using sklearn
    """
    if len(dataframe.columns) != 3:
        st.error("Clusterization can only be applied to dataframes with 3 columns")
        return pd.DataFrame()

    class_column = st.selectbox("Select a class column", dataframe.columns)
    X = dataframe.drop(class_column, axis=1)
    y = dataframe[class_column]

    n_clusters = st.slider("Select the number of clusters", min_value=2, max_value=10)

    kmeans = KNeighborsClassifier(n_neighbors=n_clusters)

    try:
        kmeans.fit(X.values, y)

        # create meshgrid
        mesh_steps = 500
        margin = 0.25
        x_min, x_max = X.iloc[:, 0].min() - margin, X.iloc[:, 0].max() + margin
        y_min, y_max = X.iloc[:, 1].min() - margin, X.iloc[:, 1].max() + margin
        x_range = np.linspace(x_min, x_max, mesh_steps)
        y_range = np.linspace(y_min, y_max, mesh_steps)
        xx, yy = np.meshgrid(x_range, y_range)

        # fill in the grid with the cluster labels
        Z = kmeans.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
        Z = Z.reshape(xx.shape)

        fig = go.Figure(go.Scatter(x=X.iloc[:, 0], y=X.iloc[:, 1], mode="markers"))
        fig.add_trace(
            go.Contour(
                x=x_range, y=y_range, z=Z, colorscale="RdBu", showscale=True, opacity=0.8
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error("An error occurred while trying to cluster the data. Please try again or select a valid class column.")

    return pd.DataFrame()


def graph_module(dataframe: pd.DataFrame, enable_st: bool = True) -> pd.DataFrame:
    """
    Calculate the graph of a dataframe using plotly
    """
    fig_types = ["Scatter", "Bar", "Box", "Histogram", "Line", "Violin"]
    if enable_st:
        selected_fig_type = st.selectbox("Select a figure type", fig_types)
    else:
        selected_fig_type = fig_types[0]

    try:
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
    except Exception as e:
        st.error(
            "An error occurred while plotting the graph, please try again with fewer columns of the same type"
        )
    return pd.DataFrame()


def map_module(dataframe: pd.DataFrame, enable_st: bool = True) -> pd.DataFrame:
    """
    Represent a dataframe as a map using streamlit API
    """
    if len(dataframe.columns) != 2:
        st.error("Mapping can only be applied to dataframes with 2 columns")
        return pd.DataFrame()

    dataframe.rename(
        columns={dataframe.columns[0]: "lat", dataframe.columns[1]: "lon"}, inplace=True
    )
    st.write("The first column is the latitude and the second column is the longitude")
    st.map(dataframe)
    return pd.DataFrame()

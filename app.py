
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="Retail Sales Analytics Dashboard", layout="wide")
sns.set_theme(style="whitegrid", context="talk", palette="colorblind")

st.title("📊 Retail Sales Analytics Dashboard")
uploaded = st.file_uploader("Upload retail sales CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    for col in ["Order Date","Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    c1,c2,c3 = st.columns(3)
    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing", int(df.isna().sum().sum()))

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(include="all").T)

    if {"Order Date","Sales","Product Category"}.issubset(df.columns):
        temp=df.copy()
        temp["YearMonth"]=temp["Order Date"].dt.to_period("M").dt.to_timestamp()
        monthly=temp.groupby(["YearMonth","Product Category"],as_index=False)["Sales"].sum()
        fig,ax=plt.subplots(figsize=(18,6))
        sns.lineplot(data=monthly,x="YearMonth",y="Sales",hue="Product Category",marker="o",linewidth=2.5,ax=ax)
        ax.set_title("Monthly Sales Over Time by Product Category")
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
        plt.xticks(rotation=45)
        st.pyplot(fig)

    if {"Profit","Product Category"}.issubset(df.columns):
        fig,ax=plt.subplots(figsize=(12,6))
        sns.boxplot(data=df,x="Product Category",y="Profit",ax=ax)
        ax.set_title("Profit Distribution by Product Category")
        st.pyplot(fig)

    num=df.select_dtypes(include="number")
    if not num.empty:
        fig,ax=plt.subplots(figsize=(10,8))
        sns.heatmap(num.corr(),annot=True,cmap="RdBu_r",center=0,ax=ax)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)
else:
    st.info("Upload a retail sales CSV to begin.")

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder  # Import LabelEncoder





file = st.file_uploader("upload nyour data as csv file ",type=["csv"])


st.write("Exploratory Data Analysis.")

if file is not None:
    df=pd.read_csv(file)
    st.write(df)
    
    st.multiselect("select columns to show",df.columns)
    st.subheader("Basic Statistics")
    st.write(df.describe())
        # Show column names
    st.subheader("Column Names")
    st.write(df.columns)
    
    # Show data types
    st.subheader("Data Types")
    st.write(df.dtypes)
    
    # Show missing values
    st.subheader("Missing Values")
    st.write(df.isnull().sum())
    
     # Allow user to drop columns
    st.subheader("Drop Columns")
    columns_to_drop = st.multiselect("Select columns to drop", df.columns)
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
        st.write("Updated DataFrame")
        st.write(df)
        
        
# Detect column types
    categorical_cols = list(df.select_dtypes(include='object').columns)
    continuous_cols = list(df.select_dtypes(include=['int', 'float']).columns)
    
   
 # Detect columns with missing values
    missing_cols = df.columns[df.isnull().any()].tolist()
    
    if len(missing_cols) > 0:
        st.subheader("Handle Missing Values")

        # Handle missing values for categorical columns
        categorical_cols = df[missing_cols].select_dtypes(include='object').columns.tolist()
        for col in categorical_cols:
            fill_method = st.selectbox(f"Select method to fill missing values for {col}", ["mode", "additional class"], key=f"{col}_missing")
            if fill_method == "mode":
                df[col].fillna(df[col].mode()[0], inplace=True)
            elif fill_method == "additional class":
                additional_class = st.text_input(f"Enter additional class for {col}")
                df[col].fillna(additional_class, inplace=True)

        # Handle missing values for continuous columns
        continuous_cols = df[missing_cols].select_dtypes(include=['int', 'float']).columns.tolist()
        for col in continuous_cols:
            fill_method = st.selectbox(f"Select method to fill missing values for {col}", ["mean", "median", "mode"], key=f"{col}_missing")
            if fill_method == "mean":
                df[col].fillna(df[col].mean(), inplace=True)
            elif fill_method == "median":
                df[col].fillna(df[col].median(), inplace=True)
            elif fill_method == "mode":
                df[col].fillna(df[col].mode()[0], inplace=True)

        # Show updated missing values
        st.subheader("Updated Missing Values")
        st.write(df[missing_cols].isnull().sum())
    else:
        st.subheader("No Missing Values Found")


    # Show handled columns
    st.subheader("Columns with Handled Missing Values")
    st.write(df[missing_cols])
    
    
    # Encode categorical data
    st.subheader("Encode Categorical Data")
    encode_method = st.selectbox("Select encoding method", ["one hot", "label encoding"])
    if encode_method == "one hot":
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    elif encode_method == "label encoding":
        encoder = LabelEncoder()
        for col in categorical_cols:
            df[col] = encoder.fit_transform(df[col])
    
    # Show final encoded dataframe
    st.subheader("Final Encoded DataFrame")
    st.write(df)
    
  # Select columns to plot
    st.subheader("Select Columns to Plot")
    columns = df.columns.tolist()
    x_axis = st.selectbox("Select X-axis", columns)
    y_axis = st.selectbox("Select Y-axis", columns)
    
    if st.button("Generate Plot"):
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
        st.pyplot(fig)




import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px


image = Image.open('elucidata-logo.png')
st.image(image)
st.title("Elucidata practical assesment task")  # title 
st.header("A web application to develop graphical plots") #sub header of the web app
st.write("**Select to view datasets :**")

@st.cache
def get_dataset(dataset):

    if dataset == "chronos":
        data = pd.read_csv("./datasets/chronos.csv")
    elif dataset == "expression":
        data = pd.read_csv("./datasets/expression.csv")
    else:
        data = pd.read_csv("./datasets/cn.csv")
    return data

@st.cache
def convert_df(df):

    return df.to_csv().encode('utf-8')

view_data = st.selectbox(" ",("chronos", "copy number", "expression"))
vd = get_dataset(view_data)
if st.checkbox('Show datasets'): 
    st.write(vd)
    st.write(f"***{view_data}*** dataset has **{len(vd.axes[0])}** rows and **{len(vd.axes[1])}** columns")
csv = convert_df(vd)
st.download_button(label="Download dataset",data=csv,mime='text/csv')

metadata = pd.read_csv("./datasets/metadata.csv") 
st.write("**select checbox to view Metadata: **") 
st.write(metadata)
st.write(f"***Metadata*** has **{len(metadata.axes[0])}** rows and **{len(metadata.axes[1])}** columns") # used string formatting to display number of columns and rows.
csv1 = convert_df(metadata)
st.download_button(label="Download metadata",data=csv,mime='text/csv')

select_plot = st.sidebar.radio("Select Plot:", ("scatter plot", "Box/Violin plot")) #select type of plot

def get_plot(select_plot):

    if select_plot == "scatter plot":
        st.sidebar.subheader(select_plot) 
        dataset1 = st.sidebar.selectbox("Select Dataset 1:", ("chronos", "copy number", "expression")) # select the dataset from the dropdown menu that will get stored in dataset_name 
        dataset2 = st.sidebar.selectbox("Select Dataset 2:", ("chronos", "copy number", "expression")) # select the dataset from the dropdown menu that will get stored in dataset_name 
        x1 = get_dataset(dataset1) #function call from own_modules
        x2 = get_dataset(dataset2)
        select_column1 = st.sidebar.selectbox('Choose gene from Dataset 1 (x-axis):', x1.columns.to_list()[1:])
        select_column2 = st.sidebar.selectbox('Choose gene from Dataset 2 (y-axis):', x2.columns.to_list()[1:])
        metadata_columns = st.sidebar.selectbox('select your metadata info:', metadata.columns.to_list())
        st.header("Data Visualization:")

        if st.sidebar.button("Submit"):
            fig = px.scatter(x=x1[select_column1], y=x2[select_column2],color = metadata[metadata_columns], labels=dict(x=select_column1,y=select_column2))
            st.write(fig)
            st.write(f"scatter plot is between gene  ***{select_column1}*** from ***{dataset1}*** dataset and gene  ***{select_column2}*** from ***{dataset2}*** dataset ")

    else:
        st.sidebar.subheader(select_plot)
        dataset1 = st.sidebar.selectbox("Select Dataset :", ("chronos", "copy number", "expression"))
        x1 = get_dataset(dataset1)
        select_column1 = st.sidebar.selectbox('Choose gene from Dataset (x-axis):', x1.columns.to_list()[1:]) # convert column names to list and [1:] used to exclude Sample_ID
        metadata_columns = st.sidebar.selectbox('select your metadata info:',metadata.columns.to_list())
        st.header("Data Visualization:")
        if st.sidebar.button("Submit"):
            fig = px.violin(x =x1[select_column1], y = metadata[metadata_columns], color = metadata[metadata_columns], box = True, points= 'all',labels=dict(x=select_column1,y=metadata_columns))
            st.write(fig)
            st.write(f"violin plot is between gene ***{select_column1}*** from ***{dataset1}*** dataset and ***{metadata_columns}*** from metadata information")
st.write(get_plot(select_plot))
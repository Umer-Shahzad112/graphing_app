import streamlit as st
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

if 'data_names' not in st.session_state:
    while True:
        try:
            st.session_state.data_names = sns.get_dataset_names()
            st.session_state.data_names.insert(0,'None')
        except:
            continue
        else:
            break

st.radio('How import dataset',options=['Use Built-in Datasets','Upload my Data (csv or excel)'],key='how')


@st.cache
def load(name):
    df = sns.load_dataset(name)
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0',inplace=True,axis = 1)
    return df

pallets = ['bright','deep','muted','hls','rocket','Blues']
available = False
if st.session_state.how == 'Use Built-in Datasets':
    name = st.selectbox('Which data set do you want to work on?',options=st.session_state.data_names,index=0,)
    if name != 'None':
        df = load(name)
        available = True
        if st.checkbox('Preview Data'):
            st.write(df)
            st.write(f'{len(df)} Data entries')
elif st.session_state.how == 'Upload my Data (csv or excel)':
    file = st.file_uploader('Upload Data file here',type=['csv','xlsx'])
    if file:
        if file.type == 'text/csv':
            df = pd.read_csv(file)
        elif file.type == 'text/xlsx':
            df = pd.read_excel(file)
        available = True
        if st.checkbox('Preview Data'):
            st.write(df)
            st.write(f'{len(df)} Data entries')


if available:
    if st.checkbox('Do you want to change data type of any feature?'):
        try:
            colname = st.selectbox('Select a feature to change its data type',df.columns)
            st.write(f'Data type of {colname} is {df[colname].dtype.name}')
            dtype = st.selectbox('Select Data Type',options=['float','str'])
            df[colname] = df[colname].astype(dtype)
        except:
            st.warning('Data type can not be converted')

    graph_type = st.multiselect('What do you wants to create',options=['Line Graph','Bar Graph'])

    if 'Line Graph' in graph_type:
        st.header('Line Graph')
        container1 = st.container()
        container2 = st.container()
        with container1:
            columns = list(df.columns)
            columns.insert(0,'None')
            x = st.selectbox('What should represent x axis?',options=columns,index=0,key='line1')
            columns = list(df.columns)
            for i in list(df.columns):
                if df[i].dtype == 'O':
                    columns.remove(i)
            y = st.multiselect('What should be represent y axis?',options= columns)
            p1 = st.selectbox('Select Palette',options=pallets,index=0,key='line2')
            if len(y) !=0:
                fig= plt.figure()
                if x == 'None':
                    sns.lineplot(data=df[y],palette=p1)
                    xmin,xmax = 0,len(df)
                else:
                    sns.lineplot(data = pd.DataFrame(np.array(df[y]),index = df[x],columns=y),palette=p1)

                    try:
                        xmin,xmax = df[x].min(),df[x].max()
                    except:
                        pass
        with container2:
            if len(y) !=0:
                if x !='None' and df[x].dtype.name not in ['object','category']:
                    # try:
                    if st.checkbox('Do you want to set x limits?',key='limits'):
                        if 'xmin' not in st.session_state:
                            st.session_state.xmin = float(xmin)
                        if 'xmax' not in st.session_state:
                            st.session_state.xmax = float(xmax)
                        col1 ,col2 = st.columns(2)
                        with col1:
                            st.slider('X lower limit',float(xmin),float(xmax),key='xmin')
                        with col2:
                            st.slider('X upper limit',float(xmin),float(xmax),key= 'xmax')
                        plt.xlim(st.session_state.xmin,st.session_state.xmax)
                    # except:
                    #     st.warning(body = 'You can not set xlim',icon='⚠️')
        with container1:
            if len(y) !=0:
                st.pyplot(fig)

    if 'Bar Graph' in graph_type:
        st.header('Bar Graph')
        columnsx = list(df.columns)
        columnsx.insert(0,'None')
        for i in df.columns:
            if df[i].dtype.name not in ['object','category']:
                columnsx.remove(i)
        x = st.selectbox('What should represent x axis?',options=columnsx,index=0,key='bar1')
        if x != 'None':
            columnsy = list(df.columns)
            columnsy.insert(0,'None')
            for i in list(df.columns):
                if df[i].dtype.name in ['object','category']:
                    columnsy.remove(i)
            y = st.selectbox('What should be represent y axis?',options= columnsy,index=0)
            hue = st.selectbox('What should be represent hue?',options= columnsx,index=0)
            p2 = st.selectbox('Select Palette',options=pallets,index = 0)

            fig= plt.figure()
            if y == 'None':
                if hue != 'None':
                    sns.countplot(x = df[x],hue=df[hue],palette=p2)
                else:
                    sns.countplot(x = df[x],palette=p2)
            else:
                if hue != 'None':
                    sns.barplot(x = df[x],y = df[y],hue=df[hue],palette=p2)
                else:
                    sns.barplot(x = df[x],y = df[y],palette=p2)
            st.pyplot(fig)

        




            
            








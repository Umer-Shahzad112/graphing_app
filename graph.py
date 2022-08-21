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

if 'df' not in st.session_state:
    st.session_state.df = ''

if 'lastfile' not in st.session_state:
    st.session_state.lastfile = ''
if 'lastname' not in st.session_state:
    st.session_state.lastname = ''
    

st.radio('How import dataset',options=['Use Built-in Datasets','Upload my Data (csv or excel)'],key='how')


@st.cache
def load(name):
    dof = sns.load_dataset(name)
    if 'Unnamed: 0' in dof.columns:
        dof.drop('Unnamed: 0',inplace=True,axis = 1)
    return dof

pallets = ['bright','deep','muted','hls','rocket','Blues']
available = False
if st.session_state.how == 'Use Built-in Datasets':
    name = st.selectbox('Which data set do you want to work on?',options=st.session_state.data_names,index=0,)
    if name != 'None':
        if st.session_state.lastname != name:
            st.session_state.df = load(name)
            st.session_state.lastname = name
        available = True
        if st.checkbox('Preview Data'):
            st.write(st.session_state.df)
            st.write(f'{len(st.session_state.df)} Data entries')
elif st.session_state.how == 'Upload my Data (csv or excel)':
    file = st.file_uploader('Upload Data file here',type=['csv','xlsx'])
    if file:
        if st.session_state.lastfile != file:
            if file.type == 'text/csv':
                st.session_state.df = pd.read_csv(file)
            elif file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                st.session_state.df = pd.read_excel(file)
            else:
                st.warning('Warning: File Type not supported')
            st.session_state.lastfile = file
      
        available = True
        if st.checkbox('Preview Data'):
            try:
                st.write(st.session_state.df)
            except:
                st.warning('Could not show preview try using different csv file format')
            st.write(f'{len(st.session_state.df)} Data entries')


if available:
    if st.checkbox('Do you want to change data type of any feature?'):
        try:
            colname = st.selectbox('Select a feature to change its data type',st.session_state.df.columns)
            st.write(f'Data type of {colname} is {st.session_state.df[colname].dtype.name}')
            dtype = st.selectbox('Select Data Type',options=['float','str'])
            st.session_state.df[colname] = st.session_state.df[colname].astype(dtype)
        except:
            st.warning('Data type can not be converted')

    graph_type = st.multiselect('What do you wants to create',options=['Line Graph','Bar Graph'])

    if 'Line Graph' in graph_type:
        st.header('Line Graph')
        container1 = st.container()
        container2 = st.container()
        with container1:
            columns = list(st.session_state.df.columns)
            columns.insert(0,'None')
            x = st.selectbox('What should represent x axis?',options=columns,index=0,key='line1')
            columns = list(st.session_state.df.columns)
            for i in list(st.session_state.df.columns):
                if st.session_state.df[i].dtype == 'O':
                    columns.remove(i)
            y = st.multiselect('What should be represent y axis?',options= columns)
            p1 = st.selectbox('Select Palette',options=pallets,index=0,key='line2')
            if len(y) !=0:
                fig= plt.figure()
                if x == 'None':
                    sns.lineplot(data=st.session_state.df[y],palette=p1)
                    xmin,xmax = 0,len(st.session_state.df)
                else:
                    sns.lineplot(data = pd.DataFrame(np.array(st.session_state.df[y]),index = st.session_state.df[x],columns=y),palette=p1)

                    try:
                        xmin,xmax = st.session_state.df[x].min(),st.session_state.df[x].max()
                    except:
                        pass
        with container2:
            if len(y) !=0:
                if x !='None' and st.session_state.df[x].dtype.name not in ['object','category']:
                    # try:
                    if st.checkbox('Do you want to set x limits?',key='limits'):
                        if 'xmin' not in st.session_state:
                            st.session_state.xmin = float(xmin)
                        if 'xmax' not in st.session_state:
                            st.session_state.xmax = float(xmax)
                        col1 ,col2 = st.columns(2)
                        with col1:
                            st.slider('X lower limit',float(xmin),float(xmax),key='xmin')
                            if st.checkbox('Set X log scale'):
                                plt.xscale('log')
                        with col2:
                            st.slider('X upper limit',float(xmin),float(xmax),key= 'xmax')
                            if st.checkbox('Set Y log scale'):
                                plt.yscale('log')
                        plt.xlim(st.session_state.xmin,st.session_state.xmax)
                    # except:
                    #     st.warning(body = 'You can not set xlim',icon='⚠️')
        with container1:
            with col1:
                if st.checkbox('Set X log scale'):
                    plt.xscale('log')
            with col2:
                if st.checkbox('Set Y log scale'):
                    plt.yscale('log')
            if len(y) !=0:
                st.pyplot(fig)

    if 'Bar Graph' in graph_type:
        st.header('Bar Graph')
        columnsx = list(st.session_state.df.columns)
        columnsx.insert(0,'None')
        for i in st.session_state.df.columns:
            if st.session_state.df[i].dtype.name not in ['object','category']:
                columnsx.remove(i)
        x = st.selectbox('What should represent x axis?',options=columnsx,index=0,key='bar1')
        if x != 'None':
            columnsy = list(st.session_state.df.columns)
            columnsy.insert(0,'None')
            for i in list(st.session_state.df.columns):
                if st.session_state.df[i].dtype.name in ['object','category']:
                    columnsy.remove(i)
            y = st.selectbox('What should be represent y axis?',options= columnsy,index=0)
            hue = st.selectbox('What should be represent hue?',options= columnsx,index=0)
            p2 = st.selectbox('Select Palette',options=pallets,index = 0)

            fig= plt.figure()
            if y == 'None':
                if hue != 'None':
                    sns.countplot(x = st.session_state.df[x],hue=st.session_state.df[hue],palette=p2)
                else:
                    sns.countplot(x = st.session_state.df[x],palette=p2)
            else:
                if hue != 'None':
                    sns.barplot(x = st.session_state.df[x],y = st.session_state.df[y],hue=st.session_state.df[hue],palette=p2)
                else:
                    sns.barplot(x = st.session_state.df[x],y = st.session_state.df[y],palette=p2)
            st.pyplot(fig)

        




            
            







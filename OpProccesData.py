# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 03:14:41 2023

@author: ACER
"""

import streamlit as st
import hydralit_components as hc
import datetime
import base64
import pandas as pd
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

############################################################################################################################################################################################################################

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def colorlist(color1, color2, num):
    """Generate list of num colors blending from color1 to color2"""
    result = [np.array(color1), np.array(color2)]
    while len(result) < num:
        temp = [result[0]]
        for i in range(len(result)-1):
            temp.append(np.sqrt((result[i]**2+result[i+1]**2)/2))
            temp.append(result[i+1])
        result = temp
    indices = np.linspace(0, len(result)-1, num).round().astype(int)
    return [result[i] for i in indices] 


#####################################################################################################################################################

font_path = 'Resources/keymer-bold.otf'  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop2 = font_manager.FontProperties(fname=font_path)

font_path2 = 'Resources/BasierCircle-Italic.ttf'  # Your font path goes here
font_manager.fontManager.addfont(font_path2)
prop3 = font_manager.FontProperties(fname=font_path2)

#####################################################################################################################################################


###########################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################

#make it look nice from the start
st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
    }
   .sidebar .sidebar-content {
        background: url("https://images.app.goo.gl/LFCobouKtT7oZ7Qv7")
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
# specify the primary menu definition
menu_data = [
    {'id': "EventingData", 'label':"Eventing Data"},
    {'id': "ActionsData", 'label':"Extract ActionsData"},
    {'id': "PassesData", 'label':"Extract PassesData"},
    {'id': "ProMatchStats", 'label':"ProMatchStats"},
    {'id': "Dashboard", 'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"} #can add a tooltip message]
]
over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    login_name='Logout',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

############################################################################################################################################################################################################################
############################################################################################################################################################################################################################
############################################################################################################################################################################################################################

if menu_id == "EventingData":
    with st.sidebar:
        with open("Resources/win.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
            st.sidebar.markdown(
                f"""
                <div style="display:table;margin-top:-20%">
                    <img src="data:image/png;base64,{data}" width="300">
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.markdown("""---""")    
        
        with st.form(key='form'):
            plt = st.text_area('Paste your Source Code')

            TableName = st.text_input("Ingrese Nombre del Archivo",
                                      key="filename"
                                      )   

            MatchID = st.text_input("Ingrese MatchID:",
                                    key="matchid"
                                    )   

            Matchday = st.text_input("Ingrese Matchday:",
                                     key="matchday"
                                     )   

            CompetitionID = st.text_input("Ingrese CompetitionID:",
                                          key="competitionid"
                                          )   
            
            submit_button = st.form_submit_button(label='Aceptar')  
     
            
    #df = pd.read_excel(Table)

    st.markdown("""---""")
    st.markdown("<style> div { text-align: center } </style>", unsafe_allow_html=True)
    
    datos = plt.split("</g>")
    #st.write(datos)
    df = pd.DataFrame(datos, columns=["EVENT"])
    df.drop(df.tail(2).index,inplace=True)
    df1 = df[df.EVENT.str.contains('<line')].reset_index()
    df1idx = df1['index']
    df1evecoor = df1['EVENT'].str.split("line", expand = True)
    df1evecoor.columns = ['zero', 'one', 'two' ]
    df1evecoor = df1evecoor.drop(['zero', 'two'], axis = 1)
    df1evecoor = df1evecoor['one'].str.split(" ", expand = True)
    df1evecoor.columns = ['a', 'X1', 'Y1', 'X2', 'Y2', 'b', 'c', 'd']
    df1evecoor = df1evecoor.drop(['a', 'b', 'c', 'd'], axis = 1)
    df1evecoor['X1'] = df1evecoor['X1'].str[4:]
    df1evecoor['X1'] = df1evecoor['X1'].str[:-1]
    df1evecoor['X2'] = df1evecoor['X2'].str[4:]
    #df1evecoor['X2'] = df1evecoor['X2 '].str[:-1]
    df1evecoor['Y1'] = df1evecoor['Y1'].str[4:]
    df1evecoor['Y1'] = df1evecoor['Y1'].str[:-1]
    df1evecoor['Y2'] = df1evecoor['Y2'].str[4:]
    df1evecoor['Y2'] = df1evecoor['Y2'].str[:-1]
    df1evecoor['X2'] = df1evecoor['X2'].str[:-1]
    df1event = df1['EVENT'].str.split("Opta-Tooltip-Key", expand = True)
    df1event.columns = ['Code', 'Event']
    df1event = df1event['Event'].str.split("</span>", expand = True)
    df1event.columns = ['Event', 'Minute', 'PlayerID', 'Player', 'Team']
    df1event['Event'] = df1event['Event'].map(lambda x: x.lstrip('">').rstrip('\n '))
    df1event['Event'] = df1event['Event'].map(lambda x: x.lstrip('\n ').rstrip(''))
    df1event['Minute'] = df1event['Minute'].str[12:-12]
    df1event['Minute'] = df1event['Minute'].map(lambda x: x.lstrip('<span class="Opta-Tooltip-Value">').rstrip("'</abbr>‎"))
    df1event['Minute'] = df1event['Minute'].map(lambda x: x.lstrip('').rstrip('<abbr title="Minute" class="">'))
    df1event['Minute'] = df1event['Minute'].str[12:]
    df1event['PlayerID'] = df1event['PlayerID'].str[40:]
    df1event['PlayerID'] = df1event['PlayerID'].map(lambda x: x.lstrip('<span class="Opta-Image-Holder Opta-Image-Player Opta-Image-Player-').rstrip('Opta-Image-Player-Small"></span>'))
    df1events = df1event['PlayerID'].str.split("Opta-Image", expand=True)
    df1events.columns = ['PlayerID', 'k']
    df1event['PlayerID'] = df1events['PlayerID']
    df1event['Player'] = df1event['Player'].str[10:]
    df1event['Player'] = df1event['Player'].map(lambda x: x.lstrip('').rstrip('class=" Opta-Image-Team-Small"></span>'))
    df1events = df1event['Player'].str.split("</p>", expand=True)
    df1events.columns = ['Player', 'k']
    df1event['Player'] = df1events['Player']
    df1event['Player'] = df1event['Player'].str[:-9]
    df1event['Team'] = df1event['Team'].str[10:]
    df1event['Team'] = df1event['Team'].map(lambda x: x.lstrip('').rstrip('\n</p>\n</div></text></g>'))
    df1event['Team'] = df1event['Team'].str[:-20]
    #st.write(df1event)
    df1eventos = pd.concat([df1idx, df1event, df1evecoor], axis = 1)
    df2 = df[~df["EVENT"].str.contains("<line")].reset_index()
    df2idx = df2['index']
    df2evecoor = df2['EVENT'].str.split("class", expand = True)
    #st.write(df2evecoor)
    df2evecoor.columns = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'onc']
    df2evecoor = df2evecoor.drop(['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'onc'], axis=1)
   
    df2evecoor['one'] = df2evecoor['one'].map(lambda x: x.lstrip('<g transform="translate(').rstrip(')" '))
    df2evecoor = df2evecoor['one'].str.split(",", expand = True)
    df2evecoor.columns = ['X1', 'Y1']
    df2event = df2['EVENT'].str.split("Opta-Tooltip-Key", expand = True)
    df2event.columns = ['Code', 'Event']
    df2event = df2event['Event'].str.split("</span>", expand = True)
    df2event.columns = ['Event', 'Minute', 'PlayerID', 'Player', 'Team']
    #df2event['Event'] = df2event['Event'].map(lambda x: x.lstrip('">').rstrip('\n '))
    #df2event['Event'] = df2event['Event'].str[15:]
    df2event['Event'] = df2event['Event'].map(lambda x: x.lstrip('">').rstrip(' \n '))
    df2event['Event'] = df2event['Event'].map(lambda x: x.lstrip('\n ').rstrip(''))
    #df2event['Event'] = df2event['Event'].str[14:-1]
    df2event['Minute'] = df2event['Minute'].str[12:-12]
    df2event['Minute'] = df2event['Minute'].map(lambda x: x.lstrip('<span class="Opta-Tooltip-Value">').rstrip("'</abbr>‎"))
    df2event['Minute'] = df2event['Minute'].map(lambda x: x.lstrip('').rstrip('<abbr title="Minute" class="">'))
    df2event['Minute'] = df2event['Minute'].str[12:]
    df2event['PlayerID'] = df2event['PlayerID'].str[40:]
    df2event['PlayerID'] = df2event['PlayerID'].map(lambda x: x.lstrip('<span class="Opta-Image-Holder Opta-Image-Player Opta-Image-Player-').rstrip('Opta-Image-Player-Small"></span>'))
    df2events = df2event['PlayerID'].str.split("Opta-Image", expand=True)
    df2events.columns = ['PlayerID', 'k']
    df2event['PlayerID'] = df2events['PlayerID']
    df2event['Player'] = df2event['Player'].str[10:]
    df2event['Player'] = df2event['Player'].map(lambda x: x.lstrip('').rstrip('class=" Opta-Image-Team-Small"></span>'))
    df2events = df2event['Player'].str.split("</p>", expand=True)
    df2events.columns = ['Player', 'k']
    df2event['Player'] = df2events['Player']
    df2event['Player'] = df2event['Player'].str[:-9]
    df2event['Team'] = df2event['Team'].str[10:]
    df2event['Team'] = df2event['Team'].map(lambda x: x.lstrip('').rstrip('\n</p>\n</div></text></g>'))
    df2event['Team'] = df2event['Team'].str[:-20]
    #st.write(df2event)
    df2evecoorcopy = df2evecoor.copy()
    df2evecoorcopy.columns = ['X2', 'Y2']
    df2eventos = pd.concat([df2idx, df2event, df2evecoor, df2evecoorcopy], axis = 1)
    df = pd.concat([df1eventos, df2eventos], axis=0)
    df = df.sort_values('index', ascending=True)
    df = df.reset_index()
    df = df.drop(['level_0'], axis=1)
    lst = []
    for i in range(len(df)):
        lst.append(MatchID)
    dfpss = pd.DataFrame([lst]).T
    dfpss.columns = ['MatchID']
    dfidx = df['index']
    dfTTT = pd.concat([dfidx, dfpss, df.iloc[:,1:]], axis = 1)
    lst2 = []
    for i in range(len(df)):
        lst2.append(Matchday)
    dfpss2 = pd.DataFrame([lst2]).T
    dfpss2.columns = ['Matchday']
    dfidx2 = df['index']
    dfTTT2 = pd.concat([dfidx2, dfpss, dfpss2, df.iloc[:,1:]], axis = 1)
    lst3 = []
    for i in range(len(df)):
        lst3.append(CompetitionID)
    dfpss3 = pd.DataFrame([lst3]).T
    dfpss3.columns = ['CompetitonID']
    dfidx3 = df['index']
    dfTTT3 = pd.concat([dfidx3, dfpss, dfpss2, dfpss3, df.iloc[:,1:]], axis = 1)
    df = dfTTT3
    df['X1'] = df['X1'].astype(float) 
    df['X2'] = df['X2'].astype(float) 
    df['Y1'] = df['Y1'].astype(float) 
    df['Y2'] = df['Y2'].astype(float) 
    df.rename(columns={'index': 'ActionID'}, inplace=True)
    dfbk = df
    st.write(df)

    but0, but1 = st.columns(2)
    with but0:
        name = Filename
        df_xlsx = to_excel(df)
        st.download_button(label='Descargar Archivo Excel',
                           data=df_xlsx,
                           file_name= ""+ name +".xlsx")

    with but1:
        df_csv = convert_df(df)
        st.download_button(label="Descargar Archivo CSV",
                           data=df_csv,
                           file_name=""+ name +".csv",
                           mime='text/csv')
   
        
    css='''
    [data-testid="metric-container"] {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] label {
        width: fit-content;
        margin: auto;
    }
    '''
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
        
   
    
    st.markdown("""---""")
    
    
        
    #st.markdown("<style> div { text-align: center; color: #FFFFFF } </style>", unsafe_allow_html=True)
  
    
    # I usually dump any scripts at the bottom of the page to avoid adding unwanted blank lines
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)

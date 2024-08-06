import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd 
import plotly.express as px
import requests
import json 
from PIL import Image



# Dataframe Creation

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 )


print(mydb)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("USE Phonepe_data")


#Aggregated_insurance
mycursor.execute("select * from aggregated_insurance;")
mydb.commit()
table7 = mycursor.fetchall()

Aggre_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#Aggregated_transsaction
mycursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1 = mycursor.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
mycursor.execute("select * from aggregated_user")
mydb.commit()
table2 = mycursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_insurance
mycursor.execute("select * from map_insurance")
mydb.commit()
table3 = mycursor.fetchall()

map_insurance = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_transaction
mycursor.execute("select * from map_transaction")
mydb.commit()
table3 = mycursor.fetchall()
map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
mycursor.execute("select * from map_user")
mydb.commit()
table4 = mycursor.fetchall()
map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_insurance
mycursor.execute("select * from top_insurance")
mydb.commit()
table5 = mycursor.fetchall()

top_insurance = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction
mycursor.execute("select * from top_transaction")
mydb.commit()
table5 = mycursor.fetchall()
top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
mycursor.execute("select * from top_user")
mydb.commit()
table6 = mycursor.fetchall()
top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))


def Transaction_amount_count_Y(df, year):

    tacy= df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(fig_count)


    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):

    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    

    fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width= 600)
    st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]: 
                states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                    height= 600,width= 600)
        fig_india_1.update_geos(visible= True)
        st.plotly_chart(fig_india_1)

    with col2: 
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Rainbow",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION COUNT", fitbounds= "locations",
                                    height= 600,width= 600)
        fig_india_2.update_geos(visible= True)
        st.plotly_chart(fig_india_2)


    
    return tacy

            
def Aggre_Tran_Transaction_type(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                            width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                            width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)

    return tacy 


# Aggre_User_analysis_1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title=  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


#Map_insurance_district
def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


#Map_insurance_district
def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "District", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy


# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "District", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "District", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)


# top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)



#SQL Connection

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 database= "Phonepe_data",
 password="",
 )

mycursor = mydb.cursor(buffered=True)

#PLOT 1 
def top_chart_transaction_amount(table_name):
    query1 = f'''SELECT States, SUM(Insurance_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_amount DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()


    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    #PLOT 2 

    query2 = f'''SELECT States, SUM(Insurance_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_amount 
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()


    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))


    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                            color_discrete_sequence=px.colors.sequential.YlGn_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)


    #PLOT 3 

    query3 = f'''SELECT States, AVG(Insurance_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_amount;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()


    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))



    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation="h",
                                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#PLOT 1 
def top_chart_transaction_count(table_name):
    query1 = f'''SELECT States, SUM(Insurance_count) AS Insurance_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_count DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()


    df_1= pd.DataFrame(table_1, columns=("states", "Insurance_count"))


    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="Insurance_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    #PLOT 2 

    query2 = f'''SELECT States, SUM(Insurance_count) AS Insurance_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_count
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()


    df_2= pd.DataFrame(table_2, columns=("states", "Insurance_count"))


    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="Insurance_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                                            color_discrete_sequence=px.colors.sequential.YlGn_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #PLOT 3 

    query3 = f'''SELECT States, AVG(Insurance_count) AS Insurance_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Insurance_count;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()


    df_3= pd.DataFrame(table_3, columns=("states", "Insurance_count"))



    fig_amount_3= px.bar(df_3, y="states", x="Insurance_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation="h",
                                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_3)

#PLOT 1
def top_chart_transaction_amount_1(table_name):
    query4 = f'''SELECT States, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    mycursor.execute(query4)
    table_4 = mycursor.fetchall()
    mydb.commit()


    df_4= pd.DataFrame(table_4, columns=("states", "transaction_amount"))



    fig_amount= px.bar(df_4, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
    fig_amount.show()


    #PLOT 2 

    query5 = f'''SELECT States, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY transaction_amount 
                LIMIT 10;'''

    mycursor.execute(query5)
    table_5 = mycursor.fetchall()
    mydb.commit()


    df_5= pd.DataFrame(table_5, columns=("states", "transaction_amount"))



    fig_amount_5= px.bar(df_5, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                        color_discrete_sequence=px.colors.sequential.YlGn_r, height= 650,width= 600)
    fig_amount_5.show()

    #PLOT 3 

    query6 = f'''SELECT States, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY transaction_amount;'''

    mycursor.execute(query6)
    table_6 = mycursor.fetchall()
    mydb.commit()


    df_6= pd.DataFrame(table_6, columns=("states", "transaction_amount"))



    fig_amount_6= px.bar(df_6, y="states", x="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states", orientation="h",
                                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_6)


    #plot_1
def top_chart_transaction_count_1(table_name):    
    query7= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    mycursor.execute(query7)
    table_7= mycursor.fetchall()
    mydb.commit()

    df_7= pd.DataFrame(table_7, columns=("states", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount_7= px.bar(df_7, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount_7)

    #plot_2
    query8= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    mycursor.execute(query8)
    table_8= mycursor.fetchall()
    mydb.commit()

    df_8= pd.DataFrame(table_8, columns=("states", "transaction_count"))

    with col2:
        fig_amount_8= px.bar(df_8, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_8)

    #plot_3
    query9= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    mycursor.execute(query9)
    table_9= mycursor.fetchall()
    mydb.commit()

    df_9= pd.DataFrame(table_9, columns=("states", "transaction_count"))

    fig_amount_9= px.bar(df_9, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_9)


  #plot_1
    
#PLOT 1 
def top_chart_registered_user(table_name , state):
    query1 = f'''SELECT Districts, SUM(registereduser) AS registeredUser
                FROM {table_name}
                WHERE States = '{state}'
                GROUP BY Districts
                ORDER BY registeredUser DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()


    df_1= pd.DataFrame(table_1, columns=("Districts", "registeredUser"))


    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="Districts", y="registeredUser", title="TOP 10 OF REGISTERED USER", hover_name= "Districts",
                                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    #PLOT 2 

    query2 = f'''SELECT Districts, SUM(registereduser) AS registeredUser
                FROM {table_name}
                WHERE States = '{state}'
                GROUP BY Districts
                ORDER BY registeredUser 
                LIMIT 10'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()


    df_2= pd.DataFrame(table_2, columns=("Districts", "registeredUser"))


    with col2:  
        fig_amount_2= px.bar(df_2, x="Districts", y="registeredUser", title=" LAST 10 OF REGISTERED USER", hover_name= "Districts",
                                            color_discrete_sequence=px.colors.sequential.YlGn_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #PLOT 3 

    query3 = f'''SELECT Districts, AVG(registereduser) AS registeredUser
                FROM {table_name}
                WHERE States = '{state}'
                GROUP BY Districts
                ORDER BY registeredUser;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()


    df_3= pd.DataFrame(table_3, columns=("Districts", "registeredUser"))



    fig_amount_3= px.bar(df_3, y="Districts", x="registeredUser", title="AVERAGE OF REGISTERED USER", hover_name= "Districts", orientation="h",
                                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


#PLOT 1 
def top_chart_appopens(table_name , state):
    query1 = f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                FROM {table_name}
                WHERE States = '{state}'
                GROUP BY Districts
                ORDER BY AppOpens DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()


    df_1= pd.DataFrame(table_1, columns=("Districts", "AppOpens"))


    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="Districts", y="AppOpens", title="TOP 10 OF APPOPENS", hover_name= "Districts",
                                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    #PLOT 2 

    query2 = f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                FROM {table_name}
                WHERE States = '{state}'
                GROUP BY Districts
                ORDER BY AppOpens 
                LIMIT 10'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()


    df_2= pd.DataFrame(table_2, columns=("Districts", "AppOpens"))


    with col2:  
        fig_amount_2= px.bar(df_2, x="Districts", y="AppOpens", title=" LAST 10 OF APPOPENS", hover_name= "Districts",
                                            color_discrete_sequence=px.colors.sequential.YlGn_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #PLOT 3 

    query3 = f'''SELECT Districts, AVG(AppOpens) AS AppOpens
                FROM {table_name}
                WHERE States = '{state}'
                GROUP BY Districts
                ORDER BY AppOpens;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()


    df_3= pd.DataFrame(table_3, columns=("Districts", "AppOpens"))



    fig_amount_3= px.bar(df_3, y="Districts", x="AppOpens", title="AVERAGE OF APPOPENS", hover_name= "AppOpens", orientation="h",
                                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



#PLOT 1 
def top_chart_registered_users(table_name):
    query1 = f'''SELECT States, SUM(RegisteredUser) AS registeredusers
                FROM top_user
                GROUP BY States
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    mycursor.execute(query1)
    table_1 = mycursor.fetchall()
    mydb.commit()


    df_1= pd.DataFrame(table_1, columns=("states", "registeredusers"))


    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)


    #PLOT 2 

    query2 = f'''SELECT States, SUM(RegisteredUser) AS registeredusers
                FROM top_user
                GROUP BY States
                ORDER BY registeredusers 
                LIMIT 10;'''

    mycursor.execute(query2)
    table_2 = mycursor.fetchall()
    mydb.commit()


    df_2= pd.DataFrame(table_2, columns=("states", "registeredusers"))


    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title=" LAST 10 OF REGISTERED USERS", hover_name= "states",
                                            color_discrete_sequence=px.colors.sequential.YlGn_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #PLOT 3 

    query3 = f'''SELECT States, AVG(RegisteredUser) AS registeredusers
                FROM top_user
                GROUP BY States
                ORDER BY registeredusers;'''

    mycursor.execute(query3)
    table_3 = mycursor.fetchall()
    mydb.commit()


    df_3= pd.DataFrame(table_3, columns=("states", "registeredusers"))



    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "registeredusers", orientation="h",
                                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



#Streamlit part


st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


with st.sidebar:
    select= option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
        col1,col2= st.columns(2)

        with col1:
            st.header("PHONEPE")
            st.subheader("INDIA'S BEST TRANSACTION APP")
            st.markdown("PhonePe  is an Indian digital payments and financial technology company PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.")
            st.write("****FEATURES****")
            st.write("****Credit & Debit card linking****")
            st.write("****Bank Balance check****")
            st.write("****Money Storage****")
            st.write("****PIN Authorization****")
            st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        with col2:
            st.image(Image.open(r"/Users/naveenmoorthy/Desktop/Code/Naveen/Phonepe Image.png"),width= 500)
   
        col3,col4= st.columns(2)

        with col3:
            st.image(Image.open(r"/Users/naveenmoorthy/Desktop/Code/Naveen/Phonepe Image 1.webp"),width=400)

        with col4:
            st.write("****Easy Transactions****")
            st.write("****One App For All Your Payments****")
            st.write("****Your Bank Account Is All You Need****")
            st.write("****Multiple Payment Modes****")
            st.write("****PhonePe Merchants****")
            st.write("****Multiple Ways To Pay****")
            st.write("****1.Direct Transfer & More****")
            st.write("****2.QR Code****")
            st.write("****Earn Great Rewards****")  

        col5,col6= st.columns(2)

        with col5:
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.write("****No Wallet Top-Up Required****")
            st.write("****Pay Directly From Any Bank To Any Bank A/C****")
            st.write("****Instantly & Free****")

        with col6:
            st.image(Image.open(r"/Users/naveenmoorthy/Desktop/Code/Naveen/PhonePe Image 2.webp"),width= 400)




elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",tac_Y["Quarter"].min(), tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)

        elif method == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)
        
        elif method == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggre_user["Years"].min(), Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)


            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    with tab2:

        method_2= st.radio("Select The Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year__",map_insurance["Years"].min(), map_insurance["Years"].max(),map_insurance["Years"].min())
            map_insur_tac_Y= Transaction_amount_count_Y(map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", map_insur_tac_Y["States"].unique())


        elif method_2 == "Map Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",map_transaction["Years"].min(), map_transaction["Years"].max(),map_transaction["Years"].min())
            map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_tran_tac_Y["States"].unique())


        elif method_2 == "Map User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_",map_user["Years"].min(), map_user["Years"].max(),map_user["Years"].min())
            map_user_Y= map_user_plot_1(map_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_",map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_", map_user_Y_Q["States"].unique())


    with tab3:

        method_3= st.radio("Select The Method",["Top Insurance", "Top Transaction"])

        if method_3 == "Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_ti",top_insurance["Years"].min(), top_insurance["Years"].max(),top_insurance["Years"].min())
            top_insur_tac_Y= Transaction_amount_count_Y(top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ti", top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu",top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)

            

        elif method_3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tt",top_transaction["Years"].min(), top_transaction["Years"].max(),top_transaction["Years"].min())
            top_tran_tac_Y= Transaction_amount_count_Y(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_tt",top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)

        elif method_3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tu",top_user["Years"].min(), top_user["Years"].max(),top_user["Years"].min())
            top_user_Y= top_user_plot_1(top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y, states)

elif select == "TOP CHARTS":
    
        question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                        "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User",
                                                    ])
           

        if question == "1. Transaction Amount and Count of Aggregated Insurance":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("aggregated_insurance")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_insurance")

        elif question == "2. Transaction Amount and Count of Map Insurance":
        
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount_1("map_insurance")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count_1("map_insurance")

        
        elif question == "3. Transaction Amount and Count of Top Insurance":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount_1("top_insurance")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count_1("top_insurance")

        elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount_1("aggregated_transaction")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count_1("aggregated_transaction")

        
        elif question == "5. Transaction Amount and Count of Map Transaction":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount_1("map_transaction")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count_1("map_transaction")

        elif question == "6. Transaction Amount and Count of Top Transaction":
            
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount_1("top_transaction")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count_1("top_transaction")

        elif question == "7. Transaction Count of Aggregated User":

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_user")

        elif question == "8. Registered users of Map User":
        
            states= st.selectbox("Select the State", map_user["States"].unique())   
            st.subheader("REGISTERED USERS")
            top_chart_registered_user("map_user", states)

        
        elif question == "9. App opens of Map User":
        
            states= st.selectbox("Select the State", map_user["States"].unique())   
            st.subheader("APPOPENS")
            top_chart_appopens("map_user", states)

        
        elif question == "10. Registered users of Top User":
            
            st.subheader("REGISTERED USERS")
            top_chart_registered_users("top_user")
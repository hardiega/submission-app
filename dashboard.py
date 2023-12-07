import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='white')

#Preparing the Datasets
 
def create_hourly(df):
    df_bike_hourly = df.groupby(by="hr").agg({"registered":"mean","casual":"mean","cnt":"mean"}).reset_index()
    return df_bike_hourly
    
def create_dailly(df):
    df_bike_dailly = df.groupby(by="day").agg({"registered":"mean","casual":"mean","cnt":"mean"}).reset_index()
    return df_bike_dailly
        
def create_by_season(df):
    df_bike_by_season = df.groupby(by="season_name").agg({"registered":"mean","casual":"mean","cnt":"mean"}).reset_index()
    return df_bike_by_season
        
def create_holiday(df):
    df_bike_holiday = df.groupby(by="is_holiday").agg({"registered":"mean","casual":"mean","cnt":"mean"}).reset_index()
    return df_bike_holiday
       
def create_corr(df):
    df_bike_corr = df.select_dtypes(include='number')
    columns_to_drop = ['registered', 'casual', 'atemp', 'instant', 'yr']
    df_bike_corr.drop(columns=columns_to_drop, inplace=True)
    df_bike_corr = pd.DataFrame(df_bike_corr.corr().cnt)
    df_bike_corr = df_bike_corr.sort_values(by='cnt', ascending=False)
    return df_bike_corr

def create_users(df):
    df_bike_user = df[["registered", "casual"]].sum()
    return df_bike_user
   
#import data
df_bike=pd.read_csv("https://raw.githubusercontent.com/hardiega/submission-app/main/data_all.csv")

df_bike_hourly = create_hourly(df_bike)
df_bike_dailly = create_dailly(df_bike)
df_bike_by_season = create_by_season(df_bike)
df_bike_holiday = create_holiday(df_bike)
df_bike_corr = create_corr(df_bike)
df_bike_user = create_users(df_bike)


#TITLE
st.title("Bike Share Dashboard")
#TABS
tab1, tab2  =st.tabs(["Users Spreads","Users Analytic"])
with tab1:
        st.header("User Spreads")
        #SELECT BOX
        bar_chart = st.selectbox(
            label = "User Type",
            options=("All","Registered","Unregistered")
        )
        
        if bar_chart == "All":
            y="cnt"
        elif bar_chart == "Registered":
            y="registered"
        elif bar_chart == "Unregistered":
            y="casual"
         
        
        st.subheader("Average Bike Share Users - Hourly")
        
        fig1, ax = plt.subplots(figsize=(20, 6))
        sns.barplot(y=y, x="hr", data=df_bike_hourly, ax=ax )
        ax.set_ylabel(None)
        ax.set_xlabel("Hour of the day" , size=15)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=20)
        st.pyplot(fig1)
                
        st.subheader("Average Bike Share Users - Dailly")
        
        fig1, ax = plt.subplots(figsize=(20, 6))
        sns.barplot(y=y, x="day", data=df_bike_dailly, ax=ax )
        ax.set_ylabel(None)
        ax.set_xlabel("Day of the week" , size=15)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=20)
        st.pyplot(fig1)
        
        
        #KOLOM
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Average User By Seasons')
            fig2, ax = plt.subplots(figsize=(15, 10))
            sns.barplot(y=y, x="season_name", data=df_bike_by_season, ax=ax )
        
            ax.set_ylabel(None)
            ax.set_xlabel("", size=15)
            ax.tick_params(axis='x', labelsize=30)
            ax.tick_params(axis='y', labelsize=30)
        
            st.pyplot(fig2)
            
        with col2:
            st.subheader('User By Holiday vs Workday')
            fig2, ax = plt.subplots(figsize=(15, 10))
        
            sns.barplot(y=y, x="is_holiday", data=df_bike_holiday, ax=ax )
        
            ax.set_ylabel(None)
            ax.set_xlabel("" , size=15)
            ax.tick_params(axis='x', labelsize=30)
            ax.tick_params(axis='y', labelsize=30)
        
            st.pyplot(fig2)
 
with tab2:
    st.header("Users Analytic")
    
    st.subheader("Users Compotition")


    labels = ['Registered', 'Unregistered']
    sizes = [df_bike_user['registered'], df_bike_user['casual']]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels)
    st.write(fig)
    
    st.subheader("Factors That Affect Users Interest in Using Bike Share")
    fig, ax = plt.subplots()
    sns.heatmap(df_bike_corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.xlabel('User Count')
    plt.ylabel(None)
    st.write(fig)
     
     
st.caption('Copyright (c) Hardian For Dicoding 2023')

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import pandasql as ps

def run_query(query):
    return ps.sqldf(query, globals())

application = pd.read_csv('/Users/velmurugan/Desktop/@/python_works/bank loan analysis/Preprocessed_app.csv')
previous = pd.read_csv('/Users/velmurugan/Desktop/@/python_works/bank loan analysis/Preprocessed_prev_app.csv')

#Univariate analysis
def univariate_categorical(feature,ylog=False,label_rotation=False,horizontal_layout=True):
    temp = application[feature].value_counts()
    df1 = pd.DataFrame({feature: temp.index,'Number of contracts': temp.values})

    # Calculate the percentage of target=1 per category value
    cat_perc = application[[feature, 'TARGET']].groupby([feature],as_index=False).mean()
    cat_perc["TARGET"] = cat_perc["TARGET"]*100
    cat_perc.sort_values(by='TARGET', ascending=False, inplace=True)
    
    if(horizontal_layout):
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(9,2))
    else:
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(9,9))
        
    # 1. Subplot 1: Count plot of categorical column

    s = sns.countplot(ax=ax1, 
                    x = feature, 
                    data=application,
                    hue ="TARGET",
                    order=cat_perc[feature],
                    palette=['g','r'])
    
    
    ax1.set_title(feature, fontdict={'fontsize' : 6, 'fontweight' : 3, 'color' : 'Blue'}) 
    ax1.legend(['Repayer','Defaulter'])
    
    # If the plot is not readable, use the log scale.
    if ylog:
        ax1.set_yscale('log')
        ax1.set_ylabel("Count (log)",fontdict={'fontsize' : 6, 'fontweight' : 3, 'color' : 'Blue'})   
    
    
    if(label_rotation):
        s.set_xticklabels(s.get_xticklabels(),rotation=90)
    
    # 2. Subplot 2: Percentage of defaulters within the categorical column
    s = sns.barplot(ax=ax2, 
                    x = feature, 
                    y='TARGET', 
                    order=cat_perc[feature], 
                    data=cat_perc,
                    palette='Set2')
    
    if(label_rotation):
        s.set_xticklabels(s.get_xticklabels(),rotation=90)
    plt.ylabel('Percent of Defaulters [%]', fontsize=7)
    plt.tick_params(axis='both', which='major', labelsize=10)
    ax2.set_title(feature + " Defaulter %", fontdict={'fontsize' : 7, 'fontweight' : 5, 'color' : 'Blue'}) 

    st.pyplot(plt)


#streamlit part

st.set_page_config(page_title="Finance Analysis",page_icon='🏭',layout='wide')

#setting up the bg color

def setting_bg():
    st.markdown(f""" <style>.stApp {{
                background: linear-gradient(to bottom, #006400, #00FF00);
            }}
           </style>""",
        unsafe_allow_html=True)

setting_bg()

st.markdown("<h1 style='text-align: center; color: #333333;'>Finance Analysis</h1>", unsafe_allow_html=True)

options = option_menu('Predictions',['Home','Queries','Insights'],icons=["cash-coin", "award-fill"])

if options == 'Home':
    st.title('Objective')
    st.write('  This case study aims to give an idea of applying EDA in a real business scenario. In this case study, we will develop a basic understanding of risk analytics in banking and financial services and understand how data is used to minimise the risk of losing money while lending to customers.')
    
    st.title('AIM')
    st.write("  This case study aims to identify patterns which indicate if a client has difficulty paying their installments which may be used for taking actions such as denying the loan, reducing the amount of loan, lending (to risky applicants) at a higher interest rate, etc. This will ensure that the consumers capable of repaying the loan are not rejected. Identification of such applicants using EDA is the aim of this case study. In other words, the company wants to understand the driving factors (or driver variables) behind loan default, i.e. the variables which are strong indicators of default. The company can utilise this knowledge for its portfolio and risk assessment.")

elif options == 'Queries':
    queries = st.selectbox("Select Query",("1.Different types of credit offered by the bank",
                                           "2.Loan amounts for clients applying for cash loans",
                                           "3.Distribution of clients across different age groups",
                                           "4.Income distribution and statistics for each credit type",
                                           "5.Analyze income distribution and statistics for each credit type"))
    
    if queries == '1.Different types of credit offered by the bank':
        query = "SELECT DISTINCT NAME_CONTRACT_TYPE AS Credit_Types FROM application"
        result = run_query(query)
        st.write(result)

    elif queries == "2.Loan amounts for clients applying for cash loans":
        query = "SELECT NAME_CONTRACT_TYPE, SUM(AMT_CREDIT) AS total_amount FROM application GROUP BY NAME_CONTRACT_TYPE"
        result = run_query(query)
        st.write(result)
    
    elif queries == '3.Distribution of clients across different age groups':
        query = 'SELECT AGE_GROUP, COUNT(*) as Total_Persons FROM application GROUP BY AGE_GROUP'
        result = run_query(query)
        st.write(result)
    
    elif queries == '4.Income distribution and statistics for each credit type':
        query = '''SELECT NAME_CONTRACT_TYPE as Credit_Type, AVG(AMT_INCOME_TOTAL)*100000 as Avg_Income,
                    MIN(AMT_INCOME_TOTAL)*100000 as Min_Income, MAX(AMT_INCOME_TOTAL)*100000 as Max_Income
                    FROM application
                    GROUP BY NAME_CONTRACT_TYPE'''
        result = run_query(query)
        st.write(result)
    
    elif queries =='5.Analyze income distribution and statistics for each credit type':
        query = 'SELECT DISTINCT AMT_INCOME_TOTAL_RANGE AS Income_Range FROM application'
        result = run_query(query)
        st.write(result)
        query = '''SELECT NAME_CONTRACT_TYPE as Credit_Type, AVG(AMT_INCOME_TOTAL)*100000 as Avg_Income,
                    MIN(AMT_INCOME_TOTAL)*100000 as Min_Income, MAX(AMT_INCOME_TOTAL)*100000 as Max_Income
                    FROM application
                    GROUP BY NAME_CONTRACT_TYPE'''
        result = run_query(query)
        st.write(result)


                                           
            


elif options == 'Insights':
    tab1,tab2,tab3=st.tabs(["Imbalance Analysis","Categorical Variable Analysis","Numeric Variable Analysis"])

    with tab1:
        Imbalance = application['TARGET'].value_counts().reset_index()
        Imbalance.columns = ['Loan Repayment Status', 'Count']

        # Replace numeric status with descriptive labels
        Imbalance['Loan Repayment Status'] = Imbalance['Loan Repayment Status'].map({0: 'Repayer', 1: 'Defaulter'})

        # Plotting the imbalance
        plt.figure(figsize=(9, 3))
        sns.barplot(x='Loan Repayment Status', y='Count', data=Imbalance, palette=['g', 'r'])
        plt.xlabel('Loan Repayment Status')
        plt.ylabel('Count of Repayers & Defaulters')
        plt.title('Imbalance Plotting')
        st.pyplot(plt)

        st.header('Insight:')
        st.write('Ratios of imbalance in percentage with respect to Repayer and Defaulter datas are: 91.93 and 8.07')

    with tab2:
        univariate_categorical('NAME_CONTRACT_TYPE',True)

        st.header('Inference')
        st.write('Revolving loans are just a small fraction (10%) from the total number of loans; in the same time, a larger amount of Revolving loans, comparing with their frequency, are not repaid.')

        univariate_categorical('CODE_GENDER')
        st.header('Inference')
        st.write('The number of female clients is almost double the number of male clients. Based on the percentage of defaulted credits, males have a higher chance of not returning their loans (~10%), comparing with women (~7%)')

        univariate_categorical('FLAG_OWN_REALTY')
        st.header('Inference')
        st.write("The clients who own real estate are more than double of the ones that don't own. But the defaulting rate of both categories are around the same (~8%). Thus there is no correlation between owning a reality and defaulting the loan.")

        univariate_categorical("NAME_EDUCATION_TYPE",True,True,True)
        st.header('Inference')
        st.write('The people with Academic degree have less than 2% defaulting rate.')

        univariate_categorical("AGE_GROUP",False,False,True)
        st.header('Inference')
        st.write('People above age of 50 have low probability of defailting')

    
    with tab3:
        cols_for_correlation = ['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 
                        'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE', 
                        'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS',
                        'NAME_HOUSING_TYPE', 'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 
                        'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH', 'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT',
                        'REGION_RATING_CLIENT_W_CITY', 'WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START',
                        'REG_REGION_NOT_LIVE_REGION', 'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 
                        'REG_CITY_NOT_LIVE_CITY', 'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'ORGANIZATION_TYPE',
                        'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE', 'DAYS_LAST_PHONE_CHANGE', 'FLAG_DOCUMENT_3', 
                        'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY', 'AMT_REQ_CREDIT_BUREAU_WEEK',
                        'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT', 'AMT_REQ_CREDIT_BUREAU_YEAR']


        Repayer_df = application.loc[application['TARGET']==0, cols_for_correlation] 
        Defaulter_df = application.loc[application['TARGET']==1, cols_for_correlation] 

        # Plotting the numerical columns related to amount as distribution plot to see density
        amount = application[[ 'AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY', 'AMT_GOODS_PRICE']]

        fig = plt.figure(figsize=(12,10))

        for i,col in enumerate(amount):
            plt.subplot(2,2,i+1)
            sns.distplot(Defaulter_df[col], hist=False, color='r',label ="Defaulter")
            sns.distplot(Repayer_df[col], hist=False, color='g', label ="Repayer")
            plt.title(col, fontdict={'fontsize' : 8, 'fontweight' : 3, 'color' : 'Blue'}) 
            
        plt.legend()

        st.pyplot(plt)

        st.header('Inference:')
        st.write('Credit amount of the loan is mostly less then 10 lakhs')
        st.write('The repayers and defaulters distribution overlap in all the plots and hence we cannot use any of these variables in isolation to make a decision')

        




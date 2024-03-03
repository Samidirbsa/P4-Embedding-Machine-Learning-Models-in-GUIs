import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

st.set_page_config(
    page_title='Predict Page',
    page_icon=':',
    layout='wide'
)

# Load models
@st.cache_data(show_spinner='Model Loading')
def logistic_regression_pipeline():
    model = joblib.load('./models/logistic_regression_pipeline.pkl')
    return model

@st.cache_data(show_spinner='Model Loading')
def random_forest_pipeline():
    model = joblib.load('./models/random_forest_pipeline.pkl')
    return model

@st.cache_resource(show_spinner='Model Loading')
def load_encoder():
    encoder = joblib.load('./models/label_encoder.pkl')
    return encoder

def select_model():
    column1, column2 = st.columns(2)
    
    with column1:
        model_name = st.selectbox('Select a Model', options=['Logistic Regression', 'Random Forest'])
        if model_name == 'Logistic Regression':
            selected_model = logistic_regression_pipeline()   
        elif model_name == 'Random Forest':
            selected_model = random_forest_pipeline()
        encoder = load_encoder()
    with column2:
        pass
        
    return selected_model, encoder

def make_prediction(model, encoder):
    df = st.session_state['df']
    prediction = model.predict(df)
    st.session_state['prediction'] = prediction
    
    if isinstance(model, LogisticRegression):
        model_name = "Logistic Regression"
    elif isinstance(model, RandomForestClassifier):
        model_name = "Random Forest"
    elif isinstance(model, Pipeline):
        # Check if the pipeline contains Logistic Regression or Random Forest
        pipeline_steps = model.named_steps.values()
        if any(isinstance(step, LogisticRegression) for step in pipeline_steps):
            model_name = "Logistic Regression"
        elif any(isinstance(step, RandomForestClassifier) for step in pipeline_steps):
            model_name = "Random Forest"
        else:
            model_name = "Unknown Model: Pipeline"
    else:
        model_name = "Unknown Model: " + str(type(model))
        print("Unknown Model: ", type(model))
        
    # Save prediction to history CSV file
    save_prediction_to_csv(df, prediction, model_name)
    return prediction




def predict():
    if 'prediction' not in st.session_state:
        st.session_state['prediction'] = None
    
    # Dictionary to store input features
    model, encoder = select_model()
    st.session_state['model_name'] = model.__class__.__name__  # Store the selected model name
    
    with st.form('input feature'):
        # Form inputs...

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write('### Personal Information')
            # Add input fields and store values in input_features dictionary
            gender = st.selectbox('gender', options=['Male', 'Female'], key='gender')
            SeniorCitizen = st.selectbox('SeniorCitizen', options=['Yes', 'No'], key='SeniorCitizen')
            Partner = st.selectbox('Partner', options=['Yes', 'No'], key='Partner')
            Dependents = st.selectbox('Dependents', options=['Yes', 'No'], key='Dependents')
            tenure = st.number_input('tenure', min_value=0, max_value=71, step=1, key='tenure')  
        
        with col2:
            st.write('### Subscriptions')
            # Input fields for subscription-related features
            PhoneService = st.selectbox('PhoneService', options=['Yes', 'No'], key='PhoneService') 
            MultipleLines = st.selectbox('MultipleLines', options=['Yes', 'No'], key='MultipleLines') 
            InternetService = st.selectbox('InternetService', options=['Fiber optic', 'DSL'], key='InternetService') 
            OnlineSecurity = st.selectbox('OnlineSecurity', options=['Yes', 'No'], key='OnlineSecurity') 
            OnlineBackup = st.selectbox('OnlineBackup', options=['Yes', 'No'], key='OnlineBackup')
            DeviceProtection = st.selectbox('DeviceProtection', options=['Yes', 'No'], key='DeviceProtection') 
            TechSupport = st.selectbox('TechSupport', options=['Yes', 'No'], key='TechSupport') 
            StreamingTV = st.selectbox('StreamingTV', options=['Yes', 'No'], key='StreamingTV') 
            StreamingMovies = st.selectbox('StreamingMovies', options=['Yes', 'No'], key='StreamingMovies')  
        
        with col3:
            st.write('### Payment Options')
            # Input fields for payment-related features
            Contract = st.selectbox('Contract', options=['Month-to-month', 'Two year', 'One year'], key='Contract') 
            PaperlessBilling = st.selectbox('PaperlessBilling', options=['Yes', 'No'], key='PaperlessBilling') 
            PaymentMethod = st.selectbox('PaymentMethod', options=['Electronic check', 'Credit card (automatic)', 'Mailed check', 'Bank transfer (automatic)'], key='PaymentMethod') 
            MonthlyCharges = st.number_input('MonthlyCharges', min_value=0, key='MonthlyCharges')
            TotalCharges = st.number_input('TotalCharges', min_value=0, key='TotalCharges') 
   
        input_features = pd.DataFrame({
            'gender': [gender], 
            'SeniorCitizen': [SeniorCitizen], 
            'Partner': [Partner], 
            'Dependents': [Dependents], 
            'tenure': [tenure],
            'PhoneService': [PhoneService],
            'MultipleLines': [MultipleLines], 
            'InternetService': [InternetService],
            'OnlineSecurity': [OnlineSecurity],
            'OnlineBackup': [OnlineBackup], 
            'DeviceProtection': [DeviceProtection], 
            'TechSupport': [TechSupport], 
            'StreamingTV': [StreamingTV],
            'StreamingMovies': [StreamingMovies], 
            'Contract': [Contract], 
            'PaperlessBilling': [PaperlessBilling], 
            'PaymentMethod': [PaymentMethod],
            'MonthlyCharges': [MonthlyCharges], 
            'TotalCharges': [TotalCharges]
        })
        st.session_state['df'] = input_features
        st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(model=model, encoder=encoder))
   
def save_prediction_to_csv(df, prediction, model_name):
    churn_label = "Churn" if prediction[0] == 1 else "Not Churn"
    
    # Concatenate input features, model name, and churn label
    prediction_df = pd.DataFrame({
        'Gender': df['gender'],
        'SeniorCitizen': df['SeniorCitizen'],
        'Partner': df['Partner'],
        'Dependents': df['Dependents'],
        'Tenure': df['tenure'],
        'PhoneService': df['PhoneService'],
        'MultipleLines': df['MultipleLines'],
        'InternetService': df['InternetService'],
        'OnlineSecurity': df['OnlineSecurity'],
        'OnlineBackup': df['OnlineBackup'],
        'DeviceProtection': df['DeviceProtection'],
        'TechSupport': df['TechSupport'],
        'StreamingTV': df['StreamingTV'],
        'StreamingMovies': df['StreamingMovies'],
        'Contract': df['Contract'],
        'PaperlessBilling': df['PaperlessBilling'],
        'PaymentMethod': df['PaymentMethod'],
        'MonthlyCharges': df['MonthlyCharges'],
        'TotalCharges': df['TotalCharges'],
        'Model': model_name,
        'Churn': churn_label
    })
    
    # Save to CSV file
    prediction_df.to_csv('data/history.csv', mode='a', header=not os.path.exists('data/history.csv'), index=False)





# Call the predict function directly
if __name__ == '__main__':
    st.title('Make a Prediction')
    predict()

prediction = st.session_state['prediction']
if prediction is not None:
    if prediction[0] == 1:
        st.write("The customer will churn.")
    else:
        st.write("The customer will not churn.")

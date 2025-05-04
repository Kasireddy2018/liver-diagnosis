import streamlit as st
import json
import os
import re
import numpy as np
import string
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder,MinMaxScaler

import pickle
session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0


def signup(json_file_path="data.json"):
    st.title("Signup Page")
    with st.form("signup_form"):
        st.write("Fill in the details below to create an account:")
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=120)
        sex = st.radio("Sex:", ("Male", "Female", "Other"))
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")

        if st.form_submit_button("Signup"):
            if password == confirm_password:
                user = create_account(name, email, age, sex, password, json_file_path)
                session_state["logged_in"] = True
                session_state["user_info"] = user
            else:
                st.error("Passwords do not match. Please try again.")

def check_login(username, password, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        for user in data["users"]:
            if user["email"] == username and user["password"] == password:
                session_state["logged_in"] = True
                session_state["user_info"] = user
                st.success("Login successful!")
                render_dashboard(user)
                return user

        st.error("Invalid credentials. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error checking login: {e}")
        return None
def initialize_database(json_file_path="data.json"):
    try:
        # Check if JSON file exists
        if not os.path.exists(json_file_path):
            # Create an empty JSON structure
            data = {"users": []}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)
    except Exception as e:
        print(f"Error initializing database: {e}")
        
def create_account(name, email, age, sex, password, json_file_path="data.json"):
    try:
        # Check if the JSON file exists or is empty
        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            data = {"users": []}
        else:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

        # Append new user data to the JSON structure
        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "sex": sex,
            "password": password,

        }
        data["users"].append(user_info)

        # Save the updated data to JSON
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        st.success("Account created successfully! You can now login.")
        return user_info
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return None

def login(json_file_path="data.json"):
    st.title("Login Page")
    username = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    login_button = st.button("Login")

    if login_button:
        user = check_login(username, password, json_file_path)
        if user is not None:
            session_state["logged_in"] = True
            session_state["user_info"] = user
        else:
            st.error("Invalid credentials. Please try again.")

def get_user_info(email, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for user in data["users"]:
                if user["email"] == email:
                    return user
        return None
    except Exception as e:
        st.error(f"Error getting user information: {e}")
        return None


def render_dashboard(user_info, json_file_path="data.json"):
    try:
        st.title(f"Welcome to the Dashboard, {user_info['name']}!")
        st.subheader("User Information:")
        st.write(f"Name: {user_info['name']}")
        st.write(f"Sex: {user_info['sex']}")
        st.write(f"Age: {user_info['age']}")

    except Exception as e:
        st.error(f"Error rendering dashboard: {e}")
    
def preprocess(text): 
    pass
    
mean_data = {
    'Age': [45.690355],
    'Gender': [0.230964],
    'Total_Bilirubin': [3.438832],
    'Direct_Bilirubin': [1.545178],
    'Alkaline_Phosphotase': [287.553299],
    'Alamine_Aminotransferase': [75.685279],
    'Aspartate_Aminotransferase': [93.180203],
    'Total_Protiens': [6.401523],
    'Albumin': [3.089340],
    'Albumin_and_Globulin_Ratio': [0.936574]
}   

std_data = {
    'Age': [15.974712],
    'Gender': [0.421986],
    'Total_Bilirubin': [6.648116],
    'Direct_Bilirubin': [2.909393],
    'Alkaline_Phosphotase': [236.907876],
    'Alamine_Aminotransferase': [164.237315],
    'Aspartate_Aminotransferase': [173.810682],
    'Total_Protiens': [1.096141],
    'Albumin': [0.795847],
    'Albumin_and_Globulin_Ratio': [0.309450]
}
                            
def main(json_file_path="data.json"):
    st.sidebar.title("Liver Disease Prediction")
    page = st.sidebar.radio(
        "Go to",
        ("Signup/Login", "Dashboard", "Liver Disease Prediction"),
        key="Liver Disease Prediction",
    )

    if page == "Signup/Login":
        st.title("Signup/Login Page")
        login_or_signup = st.radio(
            "Select an option", ("Login", "Signup"), key="login_signup"
        )
        if login_or_signup == "Login":
            login(json_file_path)
        else:
            signup(json_file_path)

    elif page == "Dashboard":
        if session_state.get("logged_in"):
            render_dashboard(session_state["user_info"])
        else:
            st.warning("Please login/signup to view the dashboard.")

    elif page == "Liver Disease Prediction":
        if session_state.get("logged_in"):
            st.title("Liver Disease Prediction")
            sel1 = ['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin',
       'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
       'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin',
       'Albumin_and_Globulin_Ratio']
            a=[]
            Age = st.number_input('Age')
            Gender = st.selectbox('Gender:', ['Female', 'Male'])
            Total_Bilirubin= st.number_input('Total_Bilirubin:')
            Direct_Bilirubin=st.number_input('Direct_Bilirubin')
            Alkaline_Phosphotase = st.number_input('Alkaline_Phosphotase')
            Alamine_Aminotransferase= st.number_input( 'Alamine_Aminotransferase:')
            Aspartate_Aminotransferase=st.number_input('Aspartate_Aminotransferase:')
            Total_Protiens = st.number_input('Total_Protiens:')
            Albumin = st.number_input('Albumin:')
            Albumin_and_Globulin_Ratio = st.number_input('Albumin_and_Globulin_Ratio:')
            
            
            a=[Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]
            
            data = pd.DataFrame([a], columns=sel1)
            def partition(x):
                if x =='Male':
                    return 0
                return 1

            data['Gender'] = data['Gender'].map(partition)
            
                
            if st.button("Submit"):
                with open('rf.pkl', 'rb') as f:
                    model1 = pickle.load(f)
                for column in data.columns:
                    if column in mean_data and column in std_data:
                        data[column] = (data[column] - mean_data[column]) / std_data[column]
                prediction= model1.predict(data)
                
                if prediction==1:
                    st.markdown('<p style="font-size:20px; font-weight:bold; color:red;">The Patient is Diagnosed with Liver Disease</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="font-size:20px; font-weight:bold; color:green;">The Patient is Not Diagnosed with Liver Disease</p>', unsafe_allow_html=True)
                
               
        else:
            st.warning("Please login/signup to use a app!!")
            



if __name__ == "__main__":
    initialize_database()
    main()

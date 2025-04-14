import streamlit as st
import requests
import time

API_URL = 'http://localhost:5000'

st.title("Crowdfunding Platform")

menu = ['Create Project', 'Contribute to Project', 'Check Funding Status']
choice = st.sidebar.selectbox("Menu", menu)

if choice == 'Create Project':
    st.subheader("Create a New Project")
    sender_address = st.text_input("Your Wallet Address")
    owner = st.text_input("Project Owner Address")
    goal = st.number_input("Funding Goal", min_value=1)

    if st.button("Create"):
        try:
            response = requests.post(f"{API_URL}/create_project", 
                                  json={
                                      'sender_address': sender_address,
                                      'owner': owner, 
                                      'goal': goal
                                  })
            if response.status_code == 201:
                st.success("Project created successfully.")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the backend server is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif choice == 'Contribute to Project':
    st.subheader("Contribute to a Project")
    sender_address = st.text_input("Your Wallet Address")
    owner = st.text_input("Project Owner Address")
    amount = st.number_input("Contribution Amount", min_value=1)

    if st.button("Contribute"):
        try:
            response = requests.post(f"{API_URL}/contribute", 
                                  json={
                                      'sender_address': sender_address,
                                      'owner': owner, 
                                      'amount': amount
                                  })
            if response.status_code == 200:
                st.success("Contribution successful.")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the backend server is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

elif choice == 'Check Funding Status':
    st.subheader("Check if a Project is Funded")
    owner = st.text_input("Project Owner Address")

    if st.button("Check"):
        try:
            response = requests.get(f"{API_URL}/is_funded/{owner}")
            if response.status_code == 200:
                is_funded = response.json().get('is_funded')
                if is_funded:
                    st.success("The project is fully funded!")
                else:
                    st.info("The project is not yet fully funded.")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the backend server is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

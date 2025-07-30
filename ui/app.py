import streamlit as st
import requests
import os

st.title("Supply Chain Optimizer Agent")

query = st.text_input("Enter your query:", "Simulate the impact if Shanghai suppliers are delayed by 5 days.")

if st.button("Invoke Agent"):
    with st.spinner("Agent is thinking..."):
        api_url = os.getenv("API_URL", "http://localhost:8080")
        response = requests.post(f"{api_url}/invoke", json={"query": query})
        try:
            st.json(response.json())
        except Exception as e:
            st.error(f"Agent error: {e}")
            st.write("Response Text:", response.text)


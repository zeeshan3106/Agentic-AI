import streamlit as st
import requests
import json
st.title("Chat Assistance")

input = st.text_input("Enter")

if st.button("Submit"):
    API = 'http://localhost:8000/get'
    res = requests.post(API, input)
    data = res.json()
    st.write(data['problem'])
    st.write(data['cause'])
    st.write(data['resolving'])
    st.write(data['tone'])
    st.write(data['urgency'])


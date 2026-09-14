import streamlit as st
import requests
import json
st.title("Marriage Budget Planning")

input = st.text_input("Enter")

if st.button("Submit"):
    API = 'http://localhost:8000/get'
    res = requests.post(API, input)
    data = res.json()
    st.write(data['query'])
    st.write(data['budget'])
    st.write(data['response'])
    # st.write(data['tone'])
    # st.write(data['urgency'])
    # st.write(data)


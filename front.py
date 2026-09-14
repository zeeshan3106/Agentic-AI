import streamlit as st
import requests
import json
st.title("Marriage Budget Planning")

input = st.text_input("Enter")

if st.button("Submit"):
    API = 'http://localhost:8000/get'
    res = requests.post(API, input)
    data = res.json()
    st.write(data['title'])
    st.write(data['outline'])
    st.write(data['blog'])
    st.write(data['status'])
    st.write(data['aproved'])


import streamlit as st
import requests
import json
st.title("blog writer")

input = st.text_input("Enter")

if st.button("Submit"):
    API = 'http://localhost:8000/blog'
    res = requests.post(API, input)
    data = res.json()
    st.write(data['outline'])
    st.write(data['blog'])


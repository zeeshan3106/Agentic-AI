import streamlt as st
import requests 
import json

st.title("MTHC AI Receptionist")
input = st.text_input("Enter the query")
API = ""
if st.button("Submit"):
    res = requests.post(API, input)
    final = res.json()
    st.write(final)
    

    

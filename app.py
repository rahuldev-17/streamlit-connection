import streamlit as st 

import weaviate
from connection import weaviateConnection

#secrects for local dev
#from dotenv import dotenv_values
#secrets = dotenv_values(".env")

url = "https://test-3xb8jtfz.weaviate.network"  # Replace with your endpoint


api_key = st.secrets["api_key"]
auth_client_secret=weaviate.AuthApiKey(api_key=api_key)#  Replace w/ your Weaviate instance API key

conn = weaviateConnection("weaviate", type=weaviateConnection, url=url, api_key=auth_client_secret)
# streamlit app starts

st.title("App to Bring Questions from weaviate Database")
st.caption("This is a minimalist streamlit application to showcase the implemented database connection class for vector database weaviate.")
st.markdown('The data was populated in the weaviate data base following [this tutorial](https://weaviate.io/developers/weaviate/quickstart).' )

st.caption("Select the input from the sidebar form, and press the `Questions` button.")

with st.sidebar.form('input'):
    concept = st.selectbox('concepts', ('Physics', 'Biology','Chemistry'  ))
    numberQuestions = st.number_input('number of questions', min_value = 1 , max_value = 10, step = 1)
    btnResult = st.form_submit_button('Questions')

if btnResult:
    nearText = {"concepts": [concept]}
    data_dict = conn.query( "Question", ["question", "answer", "category"],nearText, numberQuestions)
    questions = data_dict['data']['Get']
    st.write(f'{concept} related {numberQuestions} Questions')
    st.divider()
    st.write(questions)




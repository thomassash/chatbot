
import json
import streamlit as st
from supabase import create_client
import time


@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)



def process(question):
    # Create a Supabase connection using the API key.
    # Initialize connection.
    # Uses st.cache_resource to only run once.
    supabase_client = init_connection()
    response = supabase_client.functions.invoke(
        "ask-custom-data",
        invoke_options={"body": json.dumps({ "query": question })})
    return response


def stream_data(string_in):
    for word in string_in.split(" "):
        yield word + " "
        time.sleep(0.02)
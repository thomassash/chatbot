import streamlit as st
from openai import OpenAI
import json
from backend import process_question

col1, col2 = st.columns(2)

with col1:
    # Show title and description.
    st.title("💬 Chatbot")
    st.write(
        "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
        "THIS IS A TEST APPLICATION AND IS NOT INTENDED FOR PRODUCTION USE."
    )

    # Ask user for their OpenAI API key via `st.text_input`.
    # Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
    # via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    else:
        company = st.text_input("What company are you interested in?")
        if not company:
            st.info("Please add a company name to continue.", icon="🏢")
        else:
            st.session_state.company = company
            # # Create an OpenAI client.
            # client = OpenAI(api_key=openai_api_key)

            # Create a session state variable to store the chat messages. This ensures that the
            # messages persist across reruns.
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display the existing chat messages via `st.chat_message`.
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Create a chat input field to allow the user to enter a message. This will display
            # automatically at the bottom of the page.
            if prompt := st.chat_input("What is up?"):

                # Store and display the current prompt.
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # # Generate a response using the OpenAI API.
                # stream = client.chat.completions.create(
                #     model="gpt-3.5-turbo",
                #     messages=[
                #         {"role": m["role"], "content": m["content"]}
                #         for m in st.session_state.messages
                #     ],
                #     stream=True,
                # )

                # Generate a response using the Supabase function
                stream = json.loads(process_question.process(prompt + "If the question is not about " + company + ", please say 'I am only able to discuss the company selected.'."))
                st.info(str(stream))
                response = stream['text'].replace("\n", "")
                context = stream['contextText'].replace("\n", "")

                # Stream the response to the chat using `st.write_stream`, then store it in 
                # session state.
                with st.chat_message("assistant"):
                    st.write_stream(process_question.stream_data(response))
                st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    if not company:
        pass
    else:
        st.title(company + " Information")
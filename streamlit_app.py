import streamlit as st
from openai import OpenAI
import json
from backend import process_question
from backend import finance_charts

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)




with col1:
    # Show title and description.
    st.markdown("### 💬 Company Chatbot")
    st.write(
        "This is a simple chatbot/dashboard that uses OpenAI's GPT-4o-mini model to generate responses about specific companies and ask questions particularly about their recent earnings calls. "
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
        "THIS IS A TEST APPLICATION AND IS NOT INTENDED FOR PRODUCTION USE. CAN CURRENTLY JUST TYPE ANY OPENAI KEY AND WILL WORK."
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
            #st.info("Note: loading company information (left hand side) may take a moment.")
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
                stream = json.loads(process_question.process(prompt + " Only answer questions about " + st.session_state.company + "."))
                #st.info(str(stream))
                response = stream['text'].replace("\n", "")
                context = stream['contextText'].replace("\n", "")

                # Stream the response to the chat using `st.write_stream`, then store it in 
                # session state.
                with st.chat_message("assistant"):
                    st.write_stream(process_question.stream_data(response))
                st.session_state.messages.append({"role": "assistant", "content": response})


with col2:
    if "company" not in st.session_state:
        pass
    else:
        st.markdown("### " + st.session_state.company + " Information")
        ma_window = 14
        stock_fig = finance_charts.stock_chart(st.session_state.company, ma_window)
        st.markdown(f"##### Closing Price with {ma_window}-Day Moving Average")
        st.pyplot(stock_fig)

        # Provides summary of most recent earnings call
        st.markdown("##### " + st.session_state.company + ": Last earnings call, short summary")
        # Provides date of earnings call
        stream1 = json.loads(process_question.process("What is the date of the latest earnings call of " + st.session_state.company + "? Provide only the date and time as output in format month-day-year time."))
        response1 = stream1['text']
        st.markdown("Date: " + response1)
        # Provides summary of most recent earnings call
        stream2 = json.loads(process_question.process("Provide a three bullet summary of the most recent earnings call for " + st.session_state.company + ". Each bullet should be one short line only."))
        response2 = stream2['text']
        st.markdown(response2)

        # Provides summary of penultimate earnings call
        st.markdown("##### " + st.session_state.company + ": Penultimate earnings call, short summary")
        # Provides date of earnings call
        stream3 = json.loads(process_question.process("What is the date of the last but one earnings call of " + st.session_state.company + "? Provide only the date and time as output in format month-day-year time."))
        response3 = stream3['text']
        st.markdown("Date: " + response3)
        # Provides summary of penultimate earnings call
        stream4 = json.loads(process_question.process("Provide a three bullet summary of the last but one earnings call for " + st.session_state.company + ". Each bullet should be one short line only."))
        response4 = stream4['text']
        st.markdown(response4)


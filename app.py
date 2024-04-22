import streamlit as st
from openai import OpenAI

def main():
    st.title("IBAIT GPT")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    model_options = ['gpt-3.5-turbo','gpt-4','gpt-4-turbo-2024-04-09']
    
    st.session_state["openai_model"] = st.selectbox('Choose your Model',model_options, index=0 )
    model_temperature = st.slider('Temperature',0.0,2.0,0.7)


    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    if prompt := st.chat_input("I am grateful to offer my assistance"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(    
        model=st.session_state["openai_model"],
        messages= [{"role" : m["role"], "content": m["content"]}
                   for m in st.session_state.messages],
        temperature= model_temperature,
        stream=True 
            ) 
            answer = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": answer})

#def OpenAIAPIcall_chat(messages):
    

if __name__ == "__main__":
    main()

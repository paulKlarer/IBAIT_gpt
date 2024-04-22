import streamlit as st
from openai import OpenAI
from IPython.display import Audio
import io

def main():
    st.title("IBAIT GPT")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    with st.sidebar:
        st.title("IBAIT GPT Customizing")
        model_options = ['gpt-3.5-turbo','gpt-4','gpt-4-turbo-2024-04-09']
        st.session_state["openai_model"] = st.selectbox('Choose your Model',model_options, index=0 )
        st.session_state["model_temperature"] = st.slider('Temperature',0.0,2.0,0.7)
        st.session_state["frequency_penalty"] = st.slider('Frequncy Penalty',-2.0,2.0,0.0)
        st.session_state["presence_penalty"] = st.slider('Presence Penalty',-2.0,2.0,0.0)
        st.session_state["top_p"] = st.slider('Top_p Value', 0.0, 1.0, 0.9)
        st.session_state["max_tokens"]=st.number_input("Max Tokens",0,16000,1000,250)

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    printMessages(st.session_state["messages"])

    if prompt := st.chat_input("I am grateful to offer my assistance"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(    
        model=st.session_state["openai_model"],
        messages= [{"role" : m["role"], "content": m["content"]}
                   for m in st.session_state.messages],
        temperature= st.session_state["model_temperature"],
        frequency_penalty=st.session_state["frequency_penalty"],
        top_p=st.session_state["top_p"],
        presence_penalty=st.session_state["presence_penalty"],
        max_tokens=st.session_state["max_tokens"],
        stream=True 
            ) 
            answer = st.write_stream(stream)
        if st.button("read aloud"):
            st.write("generating audio")
            st.audio(read_aloud(answer,client))
            st.audio("read_audio")
        st.session_state.messages.append({"role": "assistant", "content": answer})

def printMessages(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
def read_aloud(text,client):
    response=client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file("/generated_audiofiles/response.mp3")
    audio_data=io.BytesIO(response)
    return audio_data
    

if __name__ == "__main__":
    main()

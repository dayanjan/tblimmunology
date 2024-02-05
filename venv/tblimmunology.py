import openai
import streamlit as st
from streamlit_chat import message
import os

# Setting page title and header
hide_streamlit_style = """ <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>"""
st.set_page_config(page_title="TBL Immunology", page_icon=":Robot:")
header_html = """
    <img src='https://pharmacy.vcu.edu/media/pharmacy/images/homepage/bm_SchoolOfPharmacy_RF_rd_hz_4c_rev.png' 
    alt='VCU School of Pharmacy Logo' style='width:100%; height:auto; margin-bottom:100px;'>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(header_html, unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Hi, I am an AI that will help you with this assignment Please start by introducing yourself!</h3>", unsafe_allow_html=True)

# Set org ID and API key
openai.api_key = st.secrets["openai"]["api_key"]

# Function to get all text files from a directory
def get_text_files(directory):
    return [os.path.splitext(f)[0] for f in os.listdir(directory) if f.endswith('.txt')]

# In the sidebar section, add a file selector
text_files = get_text_files('systemmessages')  # replace with your path
selected_file = st.sidebar.selectbox("Choose The Exercise You Will Attempt Today:", text_files)

# Add vertical space
for _ in range(5):  # adjust the range value to add more or less space
    st.sidebar.markdown("&nbsp;")

# Load the selected system message file
with open(os.path.join('systemmessages', selected_file + '.txt'), 'r') as f:
    system_message = f.read()

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": system_message}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Model selection and cost tracking")
model_name = st.sidebar.radio("Choose a model:", ("GPT-4", "GPT-3.5"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
       {"role": "system", "content": system_message}
        ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages'],
        temperature=0.7  # Added temperature parameter set to 0.7
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

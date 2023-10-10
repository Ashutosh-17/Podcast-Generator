# Import from standard library
import os
import logging

# Import from 3rd party libraries
import streamlit as st

# Import modules from the local package
from _langchain import get_response
from _elevenlabs import with_custom_voice, with_premade_voice, get_voices

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Configure Streamlit page and state
st.set_page_config(page_title="iPodcast", page_icon="🎧")

# Store the initial value of widgets in session state
if "podcast_generate" not in st.session_state:
    st.session_state.podcast_generate = ""

if "output_file_path" not in st.session_state:
    st.session_state.output_file_path = ""

if "input_file_path" not in st.session_state:
    st.session_state.input_file_path = ""

if "text_error" not in st.session_state:
    st.session_state.text_error = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"

# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Give a title to the app
st.title("Eleven Labs + Langchain Tutorial")

# Give a description to the app
st.markdown(
    "This is a demo of the Eleven Labs + Langchain Tutorial."
)

file = st.file_uploader(label="Upload file", type=["mp3",])
if file is not None:
    filename = "sample.mp3"
    with open(filename, "wb") as f:
        f.write(file.getbuffer())
    st.session_state.input_file_path = "sample.mp3"

    # Create a dropdown.
# Note: `get_voices()` is a helper function that we created in Step 5. It returns all available voices. So we can choose any voice from the dropdown.
voice = st.selectbox('Choose your voice', (i for i in get_voices()))

# Create a column layout to make UX better.
col1, col2 = st.columns(2)

# First one is for podcaster name: `Ex. Lex Fridman`.
with col1:
    podcaster = st.text_input(label="Podcaster", placeholder="Ex. Lex Fridman")

# Second one is for guest name: `Ex. Elon Musk`.
with col2:
    guest = st.text_input(label="Guest", placeholder="Ex. Elon Musk")

# Create a text area to describe actual podcast topic, information or brief explanation.
prompt = st.text_area(label="Podcast info", placeholder="Ex. Elon Musk joins Lex Fridman in conversation about AI, Autopilot, Neuralink, Tesla, and his personal history.", height=100)




# Shows loading icon while podcast and audio are being generated
text_spinner_placeholder = st.empty()

# Shows error message if any error occurs
if st.session_state.text_error:
    st.error(st.session_state.text_error)


# Output generated podcast transcription
if st.session_state.podcast_generate:
    st.markdown("""---""")
    st.subheader("Read Podcast")
    st.text_area(label="You may read podcast while audio being generated.", value=st.session_state.podcast_generate,)


# Output generated podcast audio
if st.session_state.output_file_path:
    st.markdown("""---""")
    st.subheader("Listen to Podcast")

    with open(st.session_state.output_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mp3', start_time=0)

def generate_podcast_text(prompt, podcaster, guest):
    return get_response(prompt=prompt, podcaster=podcaster, guest=guest)


def generate_podcast(voice, prompt, podcaster, guest):

    if prompt == "":
        st.session_state.text_error = "Please enter a prompt."
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            g_podcast = generate_podcast_text(prompt=prompt, podcaster=podcaster, guest=guest)

            st.session_state.podcast_generate = (g_podcast)
    
    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):

            if st.session_state.input_file_path != "":
                audio_path = with_custom_voice(podcaster=podcaster, guest=guest, description=prompt, prompt=st.session_state.podcast_generate, file_path=st.session_state.input_file_path)

                if audio_path != "":
                    st.session_state.output_file_path = audio_path

            else:

                audio_path = with_premade_voice(prompt=st.session_state.podcast_generate, voice=voice)

                if audio_path != "":
                    st.session_state.output_file_path = audio_path

# Create a button to generate podcast.
st.button(
    label="Generate Podcast",  # name on the button
    help="Click to generate podcast",  # hint text (on hover)
    key="generate_podcast",  # key to be used for the button
    type="primary",  # red default streamlit button
    on_click=generate_podcast,  # function to be called on click
    args=(voice, prompt, podcaster, guest),  # arguments to be passed to the function
)
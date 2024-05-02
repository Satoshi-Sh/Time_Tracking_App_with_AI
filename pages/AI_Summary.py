import streamlit as st
import time
import replicate


# Function for generating Snowflake Arctic response
def generate_arctic_response():
    task_times = (
        st.session_state["task_time_df"].groupby("Task")["Time"].sum().to_json()
    )
    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input={
            "prompt": f"I'll give you my activity data. Can you give a encouraging feedback on my activity? Time is in second by the way. No need to mention about the time stamp. {task_times}",
            "prompt_template": r"{prompt}",
            "temperature": 0.3,
            "top_p": 0.9,
        },
    ):
        yield str(event)


st.set_page_config(page_title="AI Summary", page_icon="🖊️", layout="wide")

if "summary" not in st.session_state:
    st.session_state["summary"] = ""


def stream_data():
    for word in st.session_state["summary"].split(" "):
        yield word + " "
        time.sleep(0.04)


st.header("Your Activity Summary", divider="rainbow")

st.markdown(
    """
    <style>
    [data-testid=stChatMessageContent]{
    position: relative;
	background: #1ac853;
	border-radius: .4em;
    padding:20px;
    font-size:30px !important;
    font-weight: 500 !important;
    }
    [data-testid=stChatMessageContent]:after{
    content: '';
	position: absolute;
	left: 0;
	top: 50%;
	width: 0;
	height: 0;
	border: 20px solid transparent;
	border-right-color: #1ac853;
	border-left: 0;
	border-bottom: 0;
	margin-top: -10px;
	margin-left: -20px;
    }
    .stChatMessage{
    margin-top:100px;
    display:flex;
    gap:25px;
    align-items:center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if len(st.session_state["task_time_df"]) > 1:
    message_board = st.empty()
    if "REPLICATE_API_TOKEN" in st.secrets:
        message = message_board.chat_message("assistant")
        message.write_stream(generate_arctic_response())
    else:
        st.warning(
            "Could you provide me with your API token in the main page.",
            icon="🤖",
        )
else:
    st.warning(
        "Need more activity data to make a summary.",
        icon="🤖",
    )

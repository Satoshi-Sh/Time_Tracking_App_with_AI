import streamlit as st
import pandas as pd
import asyncio
import time


## This blocks the timer count
## Couldn't find the solution so far
def stream_data():
    for word in st.session_state["robot_messages"][-1].split(" "):
        yield word + " "
        time.sleep(0.04)


st.set_page_config(layout="wide", page_title="Timer Tracking", page_icon="⏲️")
background_color = "#ADD8E6"
if "total_time" not in st.session_state:
    st.session_state["total_time"] = 0
if "running" not in st.session_state:
    st.session_state["running"] = False
if "selected_task" not in st.session_state:
    st.session_state["selected_task"] = ""
if "tasks" not in st.session_state:
    st.session_state["tasks"] = ["Break"]
if "task_time_df" not in st.session_state:
    st.session_state["task_time_df"] = pd.DataFrame(columns=["Task", "Time"])
if "robot_messages" not in st.session_state:
    st.session_state["robot_messages"] = ["Welcome to my Application!!"]

st.markdown(
    """
    <style>
    .time-div{
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: white;
        border: solid 2px black;
        border-radius: 20px;
    }
    .time {
        font-size: 60px !important;
        font-weight: 500 !important;
        color: #ec5953 !important;
        margin:0;
    }
    .row-widget{
       margin: 20px;
       display:flex;
       align-items:center;
       justify-content:center;
    }
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


def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02d}:{seconds:02d}"


def add_task():
    task = st.session_state.task_input
    tasks = st.session_state["tasks"]

    if task.strip() != "" and task not in tasks:
        tasks += [task]


def add_record(task, time):
    temp = st.session_state["task_time_df"]
    new_df = pd.concat(
        [temp, pd.DataFrame({"Task": [task], "Time": [time]})], ignore_index=True
    )
    st.session_state["task_time_df"] = new_df


def handle_click(task):
    if st.session_state["selected_task"] != task:
        if st.session_state["total_time"] != 0:
            add_record(
                st.session_state["selected_task"], st.session_state["total_time"]
            )
        add_robot_message(f"Go for {task}!!")
        st.session_state["selected_task"] = task
        st.session_state["total_time"] = 0


def add_robot_message(message):
    temp = st.session_state["robot_messages"]
    temp.append(message)
    st.session_state["robot_messages"] = temp


async def watch(test):
    while True:
        if st.session_state["selected_task"] != "":
            st.session_state["total_time"] += 1
        test.markdown(
            f"""
            <div class="time-div">
            <p class="time">
                {str(format_time(st.session_state["total_time"]))}
            </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if (
            st.session_state["total_time"] % 30 == 7
            and st.session_state["total_time"] != 0
        ):
            add_robot_message(
                f"test at {st.session_state['total_time']} Hello there I'm a robot and sending a message. This is not produced by AI so far but please come back to check it."
            )
            message = message_board.chat_message("assistant")
            message.write_stream(stream_data)
        await asyncio.sleep(1)


st.title("⏲️ Task Time Tracker with AI")

# popover
with st.popover("Add Task"):
    task = st.chat_input("Enter new task", on_submit=add_task, key="task_input")

if len(st.session_state["tasks"]) > 1:
    cols = st.columns(4)
    for index, task in enumerate(st.session_state["tasks"]):
        i = index % 4
        if cols[i].button(task, use_container_width=True):
            handle_click(task)

else:
    st.caption("Please add a task⬆️")

if st.session_state["selected_task"] != "":
    st.header(f'Current Task: {st.session_state["selected_task"]}', divider="rainbow")
else:
    if len(st.session_state["tasks"]) > 1:
        st.caption("Click button to start your task!!")
test = st.empty()
message_board = st.empty()
message = message_board.chat_message("assistant")
message.write_stream(stream_data)

# sidebar
with st.sidebar:
    st.header("Tracker Config")
    work_session = st.number_input(
        "Enter Work Time(min)", step=5, value=15, format="%d"
    )
    break_session = st.number_input(
        "Enter Break Time(min)", step=1, value=5, format="%d"
    )


asyncio.run(watch(test))

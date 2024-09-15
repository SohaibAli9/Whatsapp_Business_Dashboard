import os
import streamlit as st
from whatsapp_api import get_groups, get_group_chats
from chat_summary import generate_summary
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("token")

st.set_page_config(page_title="WhatsApp Group Chat Summarizer", layout="wide")

st.title("WhatsApp Group Chat Summarizer")

# Step 1: Get the list of groups and show them in a dropdown
groups = get_groups(token)
group_options = groups
selected_group_name = st.selectbox("Select a WhatsApp Group:", list(group_options.keys()))

# Step 2: When a group is selected, retrieve chats
if selected_group_name:
    selected_group_id = group_options[selected_group_name]
    chats = get_group_chats(selected_group_id, token)
    
    # Display the retrieved chat messages in a table format
    st.subheader(f"Chat Messages from {selected_group_name}")
    print(f"chats: {chats}")
    st.dataframe(chats)
    
    # Step 3: Generate and display the summary
    if st.button("Generate Summary"):
        summary = generate_summary(chats)
        st.subheader("Summary")
        st.markdown(summary)

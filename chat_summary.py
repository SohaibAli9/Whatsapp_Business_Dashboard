from openai import OpenAI
client = OpenAI()


def generate_summary(structured_df, group_name):
    messages = []
    for index, row in structured_df.iterrows():
        from_name = row['from']
        message = f"**From:** {from_name}, **Message:** '{row['text']}'"
        messages.append(message)

    # Join the list into a single string
    messages_string = "\n".join(messages)

    # Create the final prompt string
    old_prompt = f'''
    "I have a series of group chat messages that I need to summarize. The messages are from a WhatsApp group and cover various interactions. Please analyze the following text messages and provide a summary that includes:

    1. **Key Events:** What is happening in the group chat?
    2. **Intent:** What are the participants trying to achieve or communicate?
    3. **Actions:** What actions, decisions, or plans are being discussed or made?

    Here are the messages:

    {messages_string}

    Please summarize the chat by highlighting what is happening in the conversation, the intent behind the messages, and any actions or decisions discussed."
    '''

    prompt = f'''
    "I have a series of group chat messages from a WhatsApp group covering various business interactions (e.g., sales, exports, etc.). Please analyze the following text messages and provide a structured summary that includes:

    1. **Key Events:** What significant events are occurring in the conversation?
    2. **Intent:** What are the participants trying to achieve, communicate, or resolve?
    3. **Actions & Decisions:** What specific actions, plans, or decisions are being discussed or finalized? Highlight any urgent or time-sensitive actions.
    4. **Categorization by Business Area:** Organize the summary by relevant business areas, such as Sales, Export, Logistics, or Others.
    5. **Opportunities & Risks:** Identify any business opportunities or potential risks that emerge from the conversation.

    The Group Name is: {group_name}

    Here are the messages:

    {messages_string}

    Please summarize the chat in a way that emphasizes urgent actions, clear decisions, and the specific business context (e.g., sales, export, etc.). Add group name in the title"
    '''

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are skilled in figuring out the context of whatsapp group messages and then summarizing them"},
        {"role": "user", "content": f"{prompt}"}
    ])
    message_content = completion.choices[0].message.content
    return message_content
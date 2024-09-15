from openai import OpenAI
client = OpenAI()


def generate_summary(structured_df):
    messages = []
    for index, row in structured_df.iterrows():
        from_name = row['from']
        message = f"**From:** {from_name}, **Message:** '{row['text']}'"
        messages.append(message)

    # Join the list into a single string
    messages_string = "\n".join(messages)

    # Create the final prompt string
    prompt = f'''
    "I have a series of group chat messages that I need to summarize. The messages are from a WhatsApp group and cover various interactions. Please analyze the following text messages and provide a summary that includes:

    1. **Key Events:** What is happening in the group chat?
    2. **Intent:** What are the participants trying to achieve or communicate?
    3. **Actions:** What actions, decisions, or plans are being discussed or made?

    Here are the messages:

    {messages_string}

    Please summarize the chat by highlighting what is happening in the conversation, the intent behind the messages, and any actions or decisions discussed."
    '''

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are skilled in figuring out the context of whatsapp group messages and then summarizing them"},
        {"role": "user", "content": f"{prompt}"}
    ])
    message_content = completion.choices[0].message.content
    return message_content
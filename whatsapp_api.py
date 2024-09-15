import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
openapi_key = os.getenv("openapi_key")
os.environ['OPENAI_API_KEY'] = openapi_key


def get_group_chats(group_id, token):
        url = f"https://gate.whapi.cloud/messages/list/{group_id}?token={token}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            group_msg_df = pd.DataFrame(json.loads(response.text).get('messages', []))
            text_df = group_msg_df[group_msg_df['type'] == 'text']
            structured_df = text_df[['from', 'text', 'timestamp']].copy()
            structured_df['text'] = structured_df['text'].apply(lambda x: x['body'] if isinstance(x, dict) else '')
            structured_df = structured_df.sort_values(by='timestamp')
            structured_df.reset_index(drop=True, inplace=True)
            return structured_df
        else:
            print(f"Failed to get messages from group {group_id}. Status code: {response.status_code}")
            return []


def get_groups(token):
        url = f"https://gate.whapi.cloud/groups?token={token}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            groups_data = json.loads(response.text)['groups']
            groups_data_df = pd.DataFrame(groups_data)
            group_ids = groups_data_df['id']
            print(len(group_ids))
            group_names = groups_data_df['name']
            print(len(group_names))
            group_dict = dict(zip(group_names, group_ids))
            return group_dict
            # return {group['name']: group['id'] for group in groups_data['groups']}
        else:
            print(f"Failed to get groups. Status code: {response.status_code}")
            return []


# groups_data = get_groups('pkzNy0VfmWdbZyZMKlFLy1hgehOW3EPF')
# groups_data_df = pd.DataFrame(groups_data)
# group_ids = groups_data_df['id']
# # print(group_ids.head())

# group_msg_df = pd.DataFrame(get_group_chats(group_ids[2], 'pkzNy0VfmWdbZyZMKlFLy1hgehOW3EPF'))
# group_msg_df.to_excel('group_msg_df.xlsx', index=False)


# text_df = group_msg_df[group_msg_df['type'] == 'text']
# structured_df = text_df[['from', 'text', 'timestamp']].copy()
# structured_df['text'] = structured_df['text'].apply(lambda x: x['body'] if isinstance(x, dict) else '')
# structured_df = structured_df.sort_values(by='timestamp')
# structured_df.reset_index(drop=True, inplace=True)

# print(structured_df)

# group_texts = group_msg_df['text']
# print(group_msg_df.head())
# print(group_texts.head())
# print(len(group_texts))
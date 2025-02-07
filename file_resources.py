import os
import json

class FileManager:
    def __init__(self, file_path='user_data.json'):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({'messages': [], 'context': ''}, file, indent=4)

    def save_message(self, message):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        data['messages'].append(message)
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_last_messages(self, count=5):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data['messages'][-count:]

    def get_context(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data['context']

    def update_context(self, context):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        data['context'] = context
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

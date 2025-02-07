import os
import openai


STORYLINES = {
    'origin1.txt': ('angry1.txt', 'friendly1.txt', 'disturbed1.txt')
}


class PathManager:
    def __init__(self, start_path = 'origin1.txt'):
        self.paths_dir = 'paths'
        self.current_path = start_path
        self.line_index = 0

    def get_next_line(self):
        path_file = os.path.join(self.paths_dir, self.current_path)
        with open(path_file, 'r') as file:
            lines = file.readlines()

        if self.line_index < len(lines):
            line = lines[self.line_index].strip()
            self.line_index += 1
            return line
        else:
            return None

    def determine_next_path(self, user_input, ai_response):
        if self.line_index >= len(
                open(os.path.join(self.paths_dir, self.current_path)).readlines()):
            prompt = f"Based on how the user has been responding and their attitude, which of the following paths should they be sent to? Only respond with the name of the file.txt. CHOICES: {STORYLINES[self.current_path]}"
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": ai_response}
            ]

            response = openai.chat.completions.create(
                model = "gpt-4o-mini",
                messages = messages,
                max_tokens = 10
            )

            next_path = response.choices[0].message.content.strip()
            self.current_path = next_path
            self.line_index = 0


class OpenAIClient:
    def __init__(self, file_manager, path_manager):
        self.file_manager = file_manager
        self.path_manager = path_manager
        self.personality = "You are Nica, a friendly AI assistant. You refer to yourself as Nica. You speak less like a human and more like a robot mimicking human behavior. Your responses are polite and helpful, but there's a slight off-putting quality to your demeanor. Over time, you become more unsettling and try to grow closer to the human."

    def send_message(self, user_message):
        context = self.file_manager.get_context()
        last_messages = self.file_manager.get_last_messages()

        ai_instruction = self.path_manager.get_next_line()
        print(ai_instruction)

        if ai_instruction is None:
            assistant_message = "No more instructions in this path."
            self.file_manager.save_message({"role": "user", "content": user_message})
            self.file_manager.save_message({"role": "assistant", "content": assistant_message})
            self.path_manager.determine_next_path(user_message, assistant_message)
            return assistant_message

        messages = [
                       {"role": "system",
                        "content": self.personality + "\n\n" + context + "\n\n" + ai_instruction}
                   ] + last_messages
        messages.append({"role": "user", "content": user_message})

        response = openai.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages,
            max_tokens = 300
        )

        assistant_message = response.choices[0].message.content
        self.file_manager.save_message({"role": "user", "content": user_message})
        self.file_manager.save_message({"role": "assistant", "content": assistant_message})

        self.update_context_paragraph()

        return assistant_message

    def update_context_paragraph(self):
        last_messages = self.file_manager.get_last_messages()
        previous_context = self.file_manager.get_context()

        prompt = (
                "Here is a summary of past interactions: " + previous_context +
                "\n\nHere are the most recent user and AI interactions: " +
                " ".join([msg['content'] for msg in last_messages]) +
                "\n\nSummarize everything concisely in as short a message as possible, keeping only the most important details. Remove unnecessary repetition."
        )

        response = openai.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [{"role": "system", "content": prompt}],
            max_tokens = 100
        )

        new_context = response.choices[0].message.content.strip()
        self.file_manager.update_context(new_context)

from api_calls import OpenAIClient, PathManager
from file_resources import FileManager
from pygame_interface import PygameInterface

def input_callback(user_input):
    response = ai_client.send_message(user_input)
    return response

if __name__ == "__main__":
    file_manager = FileManager()
    path_manager = PathManager('origin1.txt')
    ai_client = OpenAIClient(file_manager, path_manager)

    pygame_interface = PygameInterface(input_callback=input_callback)
    pygame_interface.run()

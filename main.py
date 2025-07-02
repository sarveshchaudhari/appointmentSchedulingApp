# main.py

import gradio as gr
from dotenv import load_dotenv

from database.db_handler import init_db
from langchain_logic.agent_setup import create_agent_executor


load_dotenv()
init_db()
agent_executor = create_agent_executor()


INITIAL_MESSAGE = """
Hey! I'm your appointment scheduling assistant. I can help you schedule, find, update, or delete appointments.

To schedule an appointment, I'll need the following details:
- **customer_name**: Customer's full name.
- **customer_phone**: Customer's contact phone number.
- **appointment_datetime**: The desired date and time in `YYYY-MM-DD HH:MM:SS` format.
- **service_type**: The reason for the visit (e.g., "Dental Checkup", "Haircut").

How can I help you today?
"""

def chat_interface_fn(message, history):
    """
    The function that the Gradio ChatInterface will call.
    It processes the user's message, invokes the agent, and returns the response.
    """
    # The 'history' from Gradio is a list of [user, bot] pairs.
    # We convert it to the list-of-tuples format LangChain's agent expects.
    chat_history_tuples = []
    for user_msg, ai_msg in history:
        # We only want to feed the actual conversational turns to the agent,
        # not the initial greeting.
        if ai_msg != INITIAL_MESSAGE:
            chat_history_tuples.append(("human", user_msg))
            chat_history_tuples.append(("ai", ai_msg))

    response = agent_executor.invoke({
        "input": message,
        "chat_history": chat_history_tuples
    })

    # The ChatInterface expects a single string response from the function.
    # It will automatically append the user's message and this response to the chatbot's history.
    return response["output"]


def greet():
    """
    Function to provide the initial greeting.
    It must return the data in the format the chatbot expects: a list of [user, bot] pairs.
    """

    return [[None, INITIAL_MESSAGE]]


# --- Launch the Gradio App ---
if __name__ == "__main__":
    print("Launching Gradio Appointment Bot...")

    with gr.Blocks(theme=gr.themes.Soft(), title="Appointment Bot") as demo:
        # Create a Chatbot component that will be populated on load.
        chatbot = gr.Chatbot(label="Appointment Bot", elem_id="chatbot", height=600)

        # Create the full ChatInterface.
        chat_interface = gr.ChatInterface(
            fn=chat_interface_fn,
            chatbot=chatbot,
            examples=[
                ["Find all appointments for 'John Doe'"],
                ["I'd like to book a 'Financial Consultation' for 2024-12-25 at 14:00:00. My name is Jane Doe and my number is 555-876-5432."],
                ["Please delete all 'Maintenance Check' appointments."],
                ["Update the phone number for Jane Doe to 555-999-0000"]
            ],
            title="Conversational Appointment Scheduler"
        )

        # Use a 'load' event to populate the initial greeting using the greet function.
        demo.load(
            fn=greet,
            inputs=None,
            outputs=chatbot
        )

    demo.launch()
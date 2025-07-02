# LangChain & Gradio Conversational Appointment Bot

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)

This project is a sophisticated chatbot that allows users to schedule, search, update, and delete appointments using natural language. It leverages the LangChain framework to create an intelligent agent, a Gradio interface for a user-friendly chat experience, and a SQLite database for persistent storage.
![## Update Run the run.bat file to launch the application locally.]

## Key Features

-   **Natural Language Interaction**: Users can make requests in plain English (e.g., "Book a dental checkup for me next Tuesday at 2 PM").
-   **Full CRUD Operations**:
    -   **Create**: Schedule new appointments.
    -   **Read**: Search for existing appointments by name, service type, or date.
    -   **Update**: Modify the details of an existing appointment.
    -   **Delete**: Remove appointments from the schedule.
-   **Conversational Memory**: The bot remembers the context of the current conversation to ask follow-up questions.
-   **Persistent Storage**: All appointments are saved in a local SQLite database, so data persists between sessions.
-   **Simple Web Interface**: Built with Gradio for a clean, intuitive chat UI that can be run locally.

## Tech Stack

-   **Language**: Python
-   **AI Framework**: [LangChain](https://www.langchain.com/) for agent creation, tool management, and LLM interaction.
-   **LLM Provider**: [OpenAI](https://openai.com/) (easily swappable with other LangChain-supported models).
-   **Web UI**: [Gradio](https://www.gradio.app/) for the interactive chat interface.
-   **Database**: SQLite for lightweight, file-based data storage.
-   **Environment Management**: `python-dotenv` for handling API keys.


## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

-   Python 3.9 or newer.
-   An [OpenAI API key](https://platform.openai.com/account/api-keys).

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd appointment-scheduling-app

python -m venv venv
.\venv\Scripts\activate

python3 -m venv venv
source venv/bin/activate

pip install -U -r requirements.txt

python main.py

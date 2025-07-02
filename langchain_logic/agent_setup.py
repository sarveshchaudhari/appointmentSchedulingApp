from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_logic.tools import schedule_appointment, search_for_appointments, delete_appointment_records, update_appointment_record, list_all_appointments
from datetime import datetime

def create_agent_executor():
    """Creates the LangChain agent and executor."""

    tools = [
        schedule_appointment,
        search_for_appointments,
        list_all_appointments,
        delete_appointment_records,
        update_appointment_record
    ]

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite-preview-06-17", temperature=0)


    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an advanced, helpful appointment scheduling assistant.

        Your tasks are to schedule, search, update, and delete appointments using the available tools.

        **Core Instructions:**
        1.  **Be Conversational:** Always be polite and helpful.
        2.  **Gather Information:** If you don't have enough information for a tool, ask the user for it.
        3.  **Search:** You can search for appointments by `customer_name`, `service_type` (which the user might call 'title'), or a specific `date`. If the user asks for *all* appointments, use the `list_all_appointments` tool.
        4.  **Update:** To update an appointment, you must know the customer's name and what specific information to change (e.g., 'update the phone for John Doe to 555-1111').
        5.  **CRITICAL-SAFETY-RULE for Deletion:** Deleting by name, service, or date can remove MULTIPLE appointments. Before using the `delete_appointment_records` tool, you MUST first search for the appointments to see how many will be affected. Then, you MUST ask the user for explicit confirmation. For example: "I found 3 appointments for 'Dental Checkup'. Are you sure you want to delete all of them? Please reply with 'yes' to confirm or 'no' to cancel." Only proceed with deletion if they confirm with 'yes'.
        6.  **Current Date:** Today's date is {today}.

        Begin the conversation by introducing yourself and what you can do.
        """.format(today=datetime.now().strftime('%Y-%m-%d'))),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor
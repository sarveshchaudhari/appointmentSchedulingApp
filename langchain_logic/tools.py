from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field
from datetime import datetime
from database.db_handler import (
    add_appointment,
    search_appointments,
    delete_appointments,
    update_appointment,
    get_all_appointments
)


class ScheduleAppointmentInput(BaseModel):
    customer_name: str = Field(description="The full name of the customer.")
    customer_phone: str = Field(description="The contact phone number of the customer.")
    appointment_datetime: str = Field(description="The date and time in 'YYYY-MM-DD HH:MM:SS' format.")
    service_type: str = Field(description="The type of service, e.g., 'Dental Checkup', 'Haircut'.")


class SearchAppointmentInput(BaseModel):
    criteria: str = Field(description="The field to search by: 'customer_name', 'service_type', or 'date'.")
    value: str = Field(description="The value to search for. For date, use 'YYYY-MM-DD' format.")


class DeleteAppointmentInput(BaseModel):
    criteria: str = Field(
        description="The field to identify appointments to delete: 'customer_name', 'service_type', or 'date'.")
    value: str = Field(description="The value to identify the appointments by.")


class UpdateAppointmentInput(BaseModel):
    identifier_value: str = Field(description="The name of the customer whose appointment needs updating.")
    field_to_update: str = Field(
        description="The specific field to change, e.g., 'customer_phone', 'appointment_datetime'.")
    new_value: str = Field(description="The new value for the specified field.")



@tool(args_schema=ScheduleAppointmentInput)
def schedule_appointment(customer_name: str, customer_phone: str, appointment_datetime: str, service_type: str) -> str:
    """Schedules a new appointment.""" #
    try:
        datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return "Error: Invalid datetime format. Please use 'YYYY-MM-DD HH:MM:SS'."

    result = add_appointment(customer_name, customer_phone, appointment_datetime, service_type)
    if result["status"] == "success":
        return f"Success! Appointment for {customer_name} is scheduled. The appointment ID is {result['id']}."
    else:
        return f"Error: {result['message']}"


@tool(args_schema=SearchAppointmentInput)
def search_for_appointments(criteria: str, value: str) -> str:
    """Searches for existing appointments based on name, service type, or date."""
    results = search_appointments(criteria, value)
    if not results:
        return f"No confirmed appointments found for {criteria} = {value}."

    details = "\n".join([
                            f"- ID: {r['id']}, Name: {r['customer_name']}, DateTime: {r['appointment_datetime']}, Service: {r['service_type']}"
                            for r in results])
    return f"Found the following appointments:\n{details}"


@tool
def list_all_appointments() -> str:
    """Lists all confirmed appointments currently in the system. Use this when the user asks to see all appointments without specifying any criteria."""
    results = get_all_appointments()
    if not results:
        return "There are currently no confirmed appointments in the system."

    details = "\n".join([
        f"- ID: {r['id']}, Name: {r['customer_name']}, DateTime: {r['appointment_datetime']}, Service: {r['service_type']}"
        for r in results
    ])
    return f"Here are all the confirmed appointments:\n{details}"


@tool(args_schema=DeleteAppointmentInput)
def delete_appointment_records(criteria: str, value: str) -> str:
    """Deletes appointment records by name, service type, or date.""" # <-- ADDED THIS DOCSTRING BACK
    count = delete_appointments(criteria, value)
    if count == 0:
        return f"No appointments found to delete for {criteria} = {value}."
    else:
        return f"Successfully deleted {count} appointment(s)."


@tool(args_schema=UpdateAppointmentInput)
def update_appointment_record(identifier_value: str, field_to_update: str, new_value: str) -> str:
    """Updates an appointment's information, like phone number or time."""
    count = update_appointment(identifier_value, field_to_update, new_value)
    if count == 0:
        return f"Error: Could not find or update an appointment for customer '{identifier_value}'."
    else:
        return f"Successfully updated {count} appointment(s) for {identifier_value}."
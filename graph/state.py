from typing import TypedDict, Optional

class AppointmentState(TypedDict):

    user_input: str

    intent: Optional[str]

    patient_name: Optional[str]

    doctor_name: Optional[str]

    appointment_date: Optional[str]

    appointment_time: Optional[str]

    response: Optional[str]

    available: Optional[bool]
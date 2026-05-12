from agents.availability_agent import check_doctor_availability

while True:

    user_input = input("\nAsk: ")

    result = check_doctor_availability(user_input)

    print("\nBot:", result)
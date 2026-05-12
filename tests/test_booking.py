from agents.booking_agent import book_appointment

while True:

    user_input = input("\nAsk: ")

    result = book_appointment(user_input)

    print("\nBot:", result)
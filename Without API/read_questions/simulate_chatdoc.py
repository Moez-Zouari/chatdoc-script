import random

def simulate_chatdoc_response(question):
    """Simulates a ChatDoc response from a question."""
    possible_responses = [
        "This is a simulated response for the question ",
        "I cannot answer that at the moment, but here's a suggestion ",
        "The answer might be related to the following documentation ",
        "I recommend checking the following resources for more information "
    ]
    # Choose a random response
    simulated_response = random.choice(possible_responses)
    return simulated_response

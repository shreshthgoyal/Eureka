def apiMessage(query_type: str, response: str) -> str:
    response_map = {
        "Gym": "You can follow the given link.",
        "Price": "You can follow the given link.",
        "Queries": response,
        "Default": "I can't answer the provided query, for further information you can follow the provided link or contact us.",
        "Greet": response
    }

    if query_type in response_map:
        return response_map[query_type]
    else:
        raise "I can't help you write now"

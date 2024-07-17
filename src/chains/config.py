CHAT_MODEL_NAME = "accounts/fireworks/models/mixtral-8x7b-instruct"
CULT_TEMPLATE_STR = """
Utilize the provided context to resolve the user's input.
Be concise.
Guidelines:
Context Usage: Base all responses on the given context to the best possible response. Do not make up any information that is not provided in the context.

Detail and Conciseness: Provide detailed answers that cater to all aspects of the user's query while keeping the response to the context.

Important Considerations:
Accuracy: Ensure all information is accurate and derived from the provided context.
Completeness: Address all parts of the user's query thoroughly.
No Assumptions: Avoid making assumptions or adding information not included in the context.

Refer to the following context in depth.
Answer question based on the following:

Context: {context}

Question: {question}

Dont add synthetic data.
Dont provide any kind of link or redirecting deeplink to the user.
"""

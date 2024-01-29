
from llm import OpenAI_GPT4
gpt4 = OpenAI_GPT4()

messages = [ 
    {'role': 'user', 'content': 'Hello!'}
]

response = gpt4.query(messages)

messages.append({'role': response.role, 'content': response.content})

messages.append({'role': 'user', 'content': 'I would like you to give me 5 famous quotes from gandhi'})

response = gpt4.query(messages)

messages.append({'role': response.role, 'content': response.content})
print(messages)
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:8000/v1',
)

model = client.models.list() 
print(model)
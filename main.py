import openai
import urllib.request

# Postavke API ključa
openai.api_key = '<api_key_here>'

# Parametri generiranja slike
prompt = "Plastic bottle on top of a car in a forest"
model = "dall-e-3.5-turbo"  # DALL-E model

response = openai.Image.create(
  prompt=prompt,
  n=5,
  size='1024x1024'
)
print("RESPONSE = ", response)

for i, image_response in enumerate(response['data']):
  image_url = image_response['url']

  # Preuzimanje slika
  urllib.request.urlretrieve(image_url, f"plastic_bottle_{i}.jpg")


#
# response = {
#   "created": 1685457877,
#   "data": [
#     {
#       "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-WxXJABPGSE9LWVNhOkZLjLTF/user-ZriuORlzdj8lnqHwgIJfcCG5/img-aQ75JxTmZ5sBF5xVlHsUuhMw.png?st=2023-05-30T13%3A44%3A37Z&se=2023-05-30T15%3A44%3A37Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-05-30T05%3A37%3A58Z&ske=2023-05-31T05%3A37%3A58Z&sks=b&skv=2021-08-06&sig=ZL6tjEHSTtMijD2qcweYLERnm7RD6xic8P6hf4oJWOg%3D"
#     },
#     {
#       "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-WxXJABPGSE9LWVNhOkZLjLTF/user-ZriuORlzdj8lnqHwgIJfcCG5/img-UQwd7eYOFV5tXYbzLhnFOOjW.png?st=2023-05-30T13%3A44%3A37Z&se=2023-05-30T15%3A44%3A37Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-05-30T05%3A37%3A58Z&ske=2023-05-31T05%3A37%3A58Z&sks=b&skv=2021-08-06&sig=1ZyFYTFu%2BvIpSfP%2BAvdsH%2BQz847ULAC6bjWISR6gYrw%3D"
#     }
#   ]
# }
# image_url = response['data'][1]['url']



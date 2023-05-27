import openai

# Postavke API ključa
openai.api_key = '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'

# Parametri generiranja slike
prompt = "Generate an image of a plastic bottle."
model = "dall-e-3.5-turbo"  # DALL-E model

# Generiranje slike
# response = openai.Completion.create(
#     engine=model,
#     prompt=prompt,
#     max_tokens=100,
#     num_completions=1
# )
response = openai.Image.create(
  prompt=prompt,
  n=2,
  size='1024x1024'
)
print("RESPONSE = ", response)

# Dobivanje generirane slike
image_url = response.choices[0].image
# image_url = response['data'][0]['url']

# Preuzimanje slike
import urllib.request

urllib.request.urlretrieve(image_url, "plastic_bottle.jpg")

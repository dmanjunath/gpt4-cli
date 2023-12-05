import sys
from openai import OpenAI
client = OpenAI()

command = " ".join(sys.argv[1:]).strip()

print(f"starting generation for '{command}'")

response = client.images.generate(
  model="dall-e-3",
  prompt=command,
  size="1792x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)
import google.generativeai as genai
genai.configure(api_key="AIzaSyC_FBokV-6OC1cniro2rXtkeRKfVIl8SmA")

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)

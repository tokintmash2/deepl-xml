import deepl

auth_key = "a57ff645-14a2-4baf-9a76-9f2127927223:fx"  # Replace with your key
deepl_client = deepl.DeepLClient(auth_key)

result = deepl_client.translate_text("Hello, world!", target_lang="ET")
print(result.text)  # "Bonjour, le monde !"
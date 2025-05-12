import deepl

auth_key = "a57ff645-14a2-4baf-9a76-9f2127927223:fx"  # Replace with your key

translator = deepl.Translator(auth_key)

text = "Suvaline kartul kasvas põllul ja muutus <i>roheliseks</i>, selle asemel, et olla sinine. Peremees pahandas."

result = translator.translate_text(
    text,
    source_lang="ET",
    target_lang="EN-GB",
    tag_handling="xml",   # specify XML handling
    ignore_tags=["i"]     # optionally, specify tags to ignore during translation
)

print(result.text)

# deepl_client = deepl.DeepLClient(auth_key)

# result = deepl_client.translate_text("Suvaline kartul kasvas põllul ja muutus <i>roheliseks</i>, selle asemel, et olla sinine. Peremees pahandas.", target_lang="EN-GB", source_lang="ET")
# print(result.text)  # "Bonjour, le monde !"
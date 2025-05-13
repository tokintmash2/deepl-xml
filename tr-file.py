import deepl
import xml.etree.ElementTree as ET

f = open("key", "r")  
auth_key = f.read().strip()
f.close()
translator = deepl.Translator(auth_key)

ET.register_namespace('', 'http://docbook.org/ns/docbook')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
ET.register_namespace('xi', 'http://www.w3.org/2001/XInclude')

ns = {'db': 'http://docbook.org/ns/docbook'}

tree = ET.parse("source/input.xml")
root = tree.getroot()

tags_to_translate = ['title', 'para', 'caption', 'medialabel', 'emphasis']

def translate_text_if_needed(text):
    if text and text.strip():
        result = translator.translate_text(
            text.strip(),
            source_lang="EN",
            target_lang="FI",
            tag_handling="xml"
        )
        return result.text
    return text

for elem in root.findall(".//db:*", ns):
    tag_no_ns = elem.tag.split('}')[1]

    if tag_no_ns in tags_to_translate:
        # Translate text before children
        elem.text = translate_text_if_needed(elem.text)

        # Translate tails of child elements
        for child in elem.iter():
            child.tail = translate_text_if_needed(child.tail)
            
root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
root.set("xmlns:xi", "http://www.w3.org/2001/XInclude")

# Save translated file
tree.write("translated.xml", encoding="UTF-8", xml_declaration=True)

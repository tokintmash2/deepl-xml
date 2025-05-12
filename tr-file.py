import deepl
import xml.etree.ElementTree as ET

auth_key = "api_key"  
translator = deepl.Translator(auth_key)

# Define your namespace clearly
ns = {'db': 'http://docbook.org/ns/docbook'}

# Register namespace to preserve prefixes
ET.register_namespace('', 'http://docbook.org/ns/docbook')

# Parse input XML file
tree = ET.parse("source/input.xml")
root = tree.getroot()

# List of tags you want translated
tags_to_translate = ['title', 'para', 'caption', 'tag', 'sect2']

# Translate relevant elements
for elem in root.findall(".//db:*", ns):
    tag_no_ns = elem.tag.split('}')[1]  # Extract local tag name without namespace
    if tag_no_ns in tags_to_translate and elem.text and elem.text.strip():
        # Call DeepL to translate text
        result = translator.translate_text(
            elem.text.strip(),
            source_lang="EN",  # Your original text seems English
            target_lang="ET",
            tag_handling="xml"
        )
        elem.text = result.text

# Write translated XML to output file
tree.write("translated.xml", encoding="UTF-8", xml_declaration=True)

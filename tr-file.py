import deepl
import xml.etree.ElementTree as ET

def translate_xml_file(input_file, output_file, source_lang="EN", target_lang="RU"):
    # Read API key
    with open("key", "r") as f:
        auth_key = f.read().strip()
    
    translator = deepl.Translator(auth_key)
    
    # Read the XML file as text
    with open(input_file, "r", encoding="utf-8") as f:
        xml_content = f.read()
    
    # Tags to ignore (not translate)
    ignore_tags = ["imageobject", "imagedata", "indexterm", "tag", "primary", "secondary"]
    
    # Translate the entire XML content at once
    result = translator.translate_text(
        xml_content,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling="xml",
        ignore_tags=ignore_tags
    )
    
    # Write the translated content to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result.text)
    
    print(f"Translation completed: {input_file} → {output_file}")

if __name__ == "__main__":
    translate_xml_file("source/input.xml", "translated.xml")

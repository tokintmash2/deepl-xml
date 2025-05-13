import deepl
import xml.etree.ElementTree as ET
import os

source_lang="EN"
target_lang="DE"

def get_files_in_directory():
    directory = os.fsencode("source")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xml"):
            input_file = os.path.join("source", filename)
            output_file = os.path.join("target", f"{filename}_{target_lang}.xml")
            translate_xml_file(input_file, output_file)
    

def translate_xml_file(input_file, output_file):
    # key is API key in a separate file
    with open("key", "r") as f:
        auth_key = f.read().strip()
    
    translator = deepl.Translator(auth_key)
    
    # Open XML file
    with open(input_file, "r", encoding="utf-8") as f:
        xml_content = f.read()
    
    # Tags to ignore
    ignore_tags = ["imageobject", "imagedata", "indexterm", "tag", "primary", "secondary"]
    
    # Translate the entire XML content
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
    get_files_in_directory()

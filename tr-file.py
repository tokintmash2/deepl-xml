import deepl
import xml.etree.ElementTree as ET
import os

source_lang = "ET"
target_lang = "RU"
DEEPL_MAX_CHARS = 128000  # DeepL API max request size

def get_files_in_directory():
    directory = os.fsencode("source")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xml"):
            input_file = os.path.join("source", filename)
            output_file = os.path.join("target", f"{filename}_{target_lang}.xml")
            translate_xml_file(input_file, output_file)

def translate_xml_file(input_file, output_file):
    # Read DeepL API key
    with open("key", "r") as f:
        auth_key = f.read().strip()
    
    translator = deepl.Translator(auth_key)  # seconds

    tree = ET.parse(input_file)
    root = tree.getroot()

    # Flatten all translatable text elements
    text_elements = []
    def collect_text_elements(elem):
        if elem.text and elem.text.strip():
            text_elements.append(elem)
        for child in elem:
            collect_text_elements(child)
    collect_text_elements(root)

    # Translate in chunks
    buffer = []
    buffer_chars = 0
    buffer_map = []  # map of (element, original_text)
    for elem in text_elements:
        text = elem.text.strip()
        encoded_size = len(text.encode('utf-8'))
        if buffer_chars + encoded_size > DEEPL_MAX_CHARS or len(buffer) >= 50:
            flush_translation(buffer, buffer_map, translator)
            buffer = []
            buffer_map = []
            buffer_chars = 0
        buffer.append(text)
        buffer_map.append((elem, text))
        buffer_chars += encoded_size


    if buffer:
        flush_translation(buffer, buffer_map, translator)

    # Write modified XML
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Translation completed: {input_file} → {output_file}")

def flush_translation(buffer, buffer_map, translator):
    try:
        result = translator.translate_text(
            buffer,
            source_lang=source_lang,
            target_lang=target_lang
        )
        for (elem, _), translated in zip(buffer_map, result):
            elem.text = translated.text
    except deepl.DeepLException as e:
        print("❌ DeepL API error:", str(e))
    except Exception as e:
        print("❌ Unexpected error:", str(e))


if __name__ == "__main__":
    get_files_in_directory()
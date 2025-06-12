import xml.etree.ElementTree as ET
import os
import math

input_file = "source/split/split-test.xml"

def split_by_level_2(input_file, max_level2_per_chunk=1):
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    print(root)

    # Get all level-2 elements (direct children of root)
    level2_elements = list(root)

    total_chunks = math.ceil(len(level2_elements) / max_level2_per_chunk)
    chunk_files = []

    for i in range(total_chunks):
        chunk_elements = level2_elements[i * max_level2_per_chunk : (i + 1) * max_level2_per_chunk]
        
        # Just write the raw XML content of the elements
        base = os.path.splitext(os.path.basename(input_file))[0]
        chunk_file = os.path.join(os.path.dirname(input_file), f"{base}_chunk{i}.xml")
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            for element in chunk_elements:
                # Write raw XML content without root wrapper
                xml_string = ET.tostring(element, encoding='unicode')
                f.write(xml_string)
        
        chunk_files.append(chunk_file)

    return chunk_files

if __name__ == "__main__":
    split_by_level_2(input_file, 10)

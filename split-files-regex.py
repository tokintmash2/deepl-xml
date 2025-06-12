import os
import math
import re

input_file = "source/split/split-test.xml"

def split_by_level_2(input_file, max_level2_per_chunk=1):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the root element and its content
    root_match = re.search(r'<(\w+)[^>]*>', content)
    if not root_match:
        raise ValueError("Could not find root element")
    
    root_tag = root_match.group(1)
    root_start = root_match.end()
    
    # Find where root element ends
    root_end = content.rfind(f'</{root_tag}>')
    if root_end == -1:
        raise ValueError(f"Could not find closing tag for {root_tag}")
    
    # Extract content between root tags
    inner_content = content[root_start:root_end]
    
    # Find all level-2 elements (direct children of root)
    # This regex finds complete elements with their content
    level2_pattern = rf'<(\w+)(?:[^>]*)>(?:(?!</\1>).)*</\1>'
    level2_elements = re.findall(level2_pattern, inner_content, re.DOTALL)
    
    # Find the actual element strings with their positions
    element_strings = []
    pos = 0
    while pos < len(inner_content):
        match = re.search(rf'<(\w+)(?:[^>]*)>', inner_content[pos:])
        if not match:
            break
        
        tag_name = match.group(1)
        start_pos = pos + match.start()
        
        # Find the matching closing tag
        tag_count = 1
        search_pos = pos + match.end()
        
        while tag_count > 0 and search_pos < len(inner_content):
            next_tag = re.search(rf'</?{tag_name}(?:\s[^>]*)?>', inner_content[search_pos:])
            if not next_tag:
                break
            
            if next_tag.group().startswith(f'</{tag_name}'):
                tag_count -= 1
            else:
                tag_count += 1
            
            search_pos += next_tag.end()
            if tag_count == 0:
                element_strings.append(inner_content[start_pos:search_pos])
                pos = search_pos
                break
        else:
            break
    
    total_chunks = math.ceil(len(element_strings) / max_level2_per_chunk)
    chunk_files = []

    for i in range(total_chunks):
        chunk_elements = element_strings[i * max_level2_per_chunk : (i + 1) * max_level2_per_chunk]
        
        base = os.path.splitext(os.path.basename(input_file))[0]
        chunk_file = os.path.join(os.path.dirname(input_file), f"{base}_chunk{i}.xml")
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            for element in chunk_elements:
                f.write(element)
        
        chunk_files.append(chunk_file)

    return chunk_files

if __name__ == "__main__":
    split_by_level_2(input_file, 2)

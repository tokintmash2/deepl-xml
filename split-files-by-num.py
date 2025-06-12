import os
import re

input_file = "source/split/split-test.xml"

def split_by_character_count(input_file, max_chars_per_chunk=700000):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the root element opening and closing tags
    root_match = re.search(r'<[^>]+>', content)
    if not root_match:
        raise ValueError("Could not find root element")
    
    root_opening = root_match.group()
    root_start = root_match.end()
    
    # Find the last closing tag (root closing)
    root_closing_match = re.search(r'<\/[^>]+>\s*$', content)
    if not root_closing_match:
        raise ValueError("Could not find root closing tag")
    
    root_closing = root_closing_match.group()
    root_end = root_closing_match.start()
    
    # Extract content between root tags
    inner_content = content[root_start:root_end]
    
    chunk_files = []
    chunk_num = 0
    current_pos = 0
    
    while current_pos < len(inner_content):
        # Find the end position for this chunk
        end_pos = min(current_pos + max_chars_per_chunk, len(inner_content))
        
        # If we're not at the very end, find the nearest tag boundary
        if end_pos < len(inner_content):
            # Look for the pattern: "> <" (end of one tag, start of another)
            # Search backwards from end_pos to find a good cut point
            search_start = max(0, end_pos - 1000)  # Search within 1000 chars back
            
            # Find all "> <" patterns in the search area
            tag_boundaries = []
            for match in re.finditer(r'>\s*<', inner_content[search_start:end_pos + 100]):
                actual_pos = search_start + match.start() + 1  # Position after '>'
                tag_boundaries.append(actual_pos)
            
            if tag_boundaries:
                # Choose the boundary closest to our target end_pos
                end_pos = min(tag_boundaries, key=lambda x: abs(x - end_pos))
        
        # Extract chunk content
        chunk_content = inner_content[current_pos:end_pos]
        
        # Write chunk file
        base = os.path.splitext(os.path.basename(input_file))[0]
        chunk_file = os.path.join(os.path.dirname(input_file), f"{base}_chunk{chunk_num}.xml")
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk_content)
        
        chunk_files.append(chunk_file)
        print(f"Created {chunk_file} with {len(chunk_content)} characters")
        
        current_pos = end_pos
        chunk_num += 1
    
    return chunk_files

if __name__ == "__main__":
    split_by_character_count(input_file, 100000)

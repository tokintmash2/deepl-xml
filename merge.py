import os
import glob

def merge_chunks(chunk_pattern, output_file):
    """
    Simple concatenation of chunk files back into one file.
    """
    # Get all chunk files and sort them by chunk number
    chunk_files = glob.glob(chunk_pattern)
    chunk_files.sort(key=lambda x: int(x.split('_chunk')[1].split('.')[0]))
    
    print(f"Merging {len(chunk_files)} chunks...")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for chunk_file in chunk_files:
            print(f"Adding: {chunk_file}")
            with open(chunk_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
    
    print(f"Done! Merged into: {output_file}")

if __name__ == "__main__":
    merge_chunks("target/split-test_chunk*.xml", "target/merged-output.xml")

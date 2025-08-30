import os
import sys
from datetime import datetime

def search_lyrics(directory, query_word):
    """
    Search for a query word in lyrics files and output results to a file.
    """
    # Generate output filename with timestamp and query word
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"query_results_{timestamp}_{query_word}.txt"
    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        # Traverse the lyrics directory
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):  # Assuming lyrics files are .txt
                    file_path = os.path.join(root, file)
                    song_name = os.path.splitext(file)[0]
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as lyric_file:
                            lines = lyric_file.readlines()
                            
                            for i, line in enumerate(lines):
                                if query_word.lower() in line.lower():
                                    # Get context (previous, current, and next lines)
                                    start = max(0, i - 1)
                                    end = min(len(lines), i + 2)
                                    context = lines[start:end]
                                    
                                    # Write results to output file
                                    singer = os.path.basename(os.path.dirname(file_path))
                                    output_file.write(f"==========\nSinger: {singer}\nSong: {song_name}\n")
                                    output_file.write(f"Context:\n")
                                    for ctx_line in context:
                                        output_file.write(f"  - {ctx_line.strip()}\n")
                                    output_file.write("\n")
                                    break  # Avoid duplicate lines in the same song
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}", file=sys.stderr)
    
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python query.py <query_word>")
        sys.exit(1)
    
    lyrics_dir = os.path.join(os.path.dirname(__file__), 'lyrics')
    query_word = sys.argv[1]
    
    search_lyrics(lyrics_dir, query_word)
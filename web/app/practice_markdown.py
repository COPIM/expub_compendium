# @name: practice_markdown.py
# @creation_date: 2024-02-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: functions for retrieving Markdown for practices
# @acknowledgements:

import os
import markdown

# function to get practice from Markdown file
def get_practice_markdown(practice_name, option='html'):
    practice_name = practice_name.replace(" ", "_")
    file_path = f'content/practices/{practice_name}.md'
    
    if not os.path.exists(file_path):
        return ""
    
    try:
        with open(file_path, 'r') as f:
            practice_text = f.read()
            if option == 'html':
                practice_text = markdown.markdown(practice_text)
        return practice_text
    except Exception as e:
        return f"Error: {str(e)}"

# function to write new or edited practice to Markdown file
def write_practice_markdown(practice_name, markdown):
    practice_name = practice_name.replace(" ", "_")
    with open(f'content/practices/{practice_name}.md', 'w+') as f:
        f.write(markdown)

# function to extract only the first paragraph of practice Markdown
def extract_first_paragraph(markdown):
    # Split the text into lines
    lines = markdown.split("\n")
    
    # Initialize a flag to track when we find the first paragraph
    paragraph = []
    
    for line in lines:
        # Ignore headings (lines starting with #)
        if line.startswith("#"):
            continue
        
        # If the line is not empty, it's part of a paragraph
        if line.strip():
            paragraph.append(line.strip())
        elif paragraph:  # Stop once we have collected a paragraph and hit an empty line
            break

    return " ".join(paragraph)
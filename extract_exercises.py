import os
import re
import json

root_dir = 'Natural_Sciences'
output_file = 'assets/json/daily_problems.json'
exercises = []

# Simplified Regex for exercise (captures everything between begin and end)
exercise_pattern = re.compile(r'\\begin{exercise}(.*?)\\end{exercise}', re.DOTALL)
# Regex for solution (to be searched after exercise)
solution_pattern = re.compile(r'^\\s*\\begin{solution}(.*?)\\end{solution}', re.DOTALL)

print("Starting scan...")

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(subdir, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    
                    for match in exercise_pattern.finditer(content):
                        # Extract raw body
                        raw_body = match.group(1).strip()
                        
                        # Manual title extraction
                        title = "Exercise"
                        content_text = raw_body
                        
                        # Check for optional argument [Title]
                        # We handle simple cases where title doesn't contain ]
                        if raw_body.startswith('['):
                            end_bracket = raw_body.find(']')
                            if end_bracket != -1:
                                title = raw_body[1:end_bracket]
                                content_text = raw_body[end_bracket+1:].strip()
                        
                        # Look for solution immediately following this match
                        remaining_content = content[match.end():]
                        solution_match = solution_pattern.match(remaining_content)
                        
                        solution_text = None
                        if solution_match:
                            solution_text = solution_match.group(1).strip()
                        
                        exercises.append({
                            'source': filepath,
                            'title': title,
                            'content': content_text,
                            'solution': solution_text
                        })

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(exercises, f, indent=2)

print(f"Extracted {len(exercises)} exercises to {output_file}")

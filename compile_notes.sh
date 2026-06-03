#!/bin/bash

# Find all paper.tex files
NOTE_FILES=$(find . -name "paper.tex")

echo "Starting compilation of LaTeX notes..."
echo "--------------------------------------"

for file in $NOTE_FILES; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    
    # Get absolute path for reporting
    abs_dir=$(cd "$dir" && pwd)
    rel_path="${file#./}"

    echo "Compiling: $rel_path"
    
    # Run latexmk in the file's directory
    # -pdf: generate pdf
    # -halt-on-error: stop on first error
    # -interaction=nonstopmode: don't wait for user input
    output=$(cd "$dir" && latexmk -pdf -halt-on-error -interaction=nonstopmode "$base" 2>&1)
    status=$?
    
    if [ $status -eq 0 ]; then
        echo "✅ Success: $rel_path"
        # Clean up aux files after success
        (cd "$dir" && latexmk -c "$base" > /dev/null 2>&1)
    else
        echo "❌ Error: $rel_path"
        echo "Relevant log output:"
        # Extract errors and warnings
        echo "$output" | grep -iE "!(.*)|warning|undefined" | grep -v "Read 0 entries" | sed 's/^/  /'
    fi
    echo "--------------------------------------"
done

echo "Compilation process finished."

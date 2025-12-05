import os
import re
import sys
from pathlib import Path

def pause_at_end():
    """Pause so window doesn't close immediately"""
    input("\nPress Enter to exit...")
    sys.exit()

def process_line(line, line_num):
    """Process a single line and return (corrected_line, errors_found)"""
    original = line
    errors = []
    
    # Remove trailing spaces
    if line.rstrip() != line:
        errors.append(f"Line {line_num}: Removed trailing spaces")
        line = line.rstrip()
    
    # Skip empty lines
    if not line:
        return None, errors
    
    # Collapse multiple spaces to single space
    if '  ' in line:
        errors.append(f"Line {line_num}: Collapsed multiple spaces")
        line = re.sub(r' +', ' ', line)
    
    # Check if line ends with __wildcard__ pattern
    ends_with_wildcard = re.search(r'__.*?__$', line)
    
    if ends_with_wildcard:
        # Should NOT have comma
        if line.endswith(',') or line.endswith(', '):
            errors.append(f"Line {line_num}: Removed comma after wildcard")
            line = line.rstrip(',').rstrip()
    else:
        # Should have comma
        if not line.endswith(','):
            errors.append(f"Line {line_num}: Added missing comma")
            line = line + ','
    
    return line, errors

def process_file(filepath):
    """Process a single file and return list of errors"""
    all_errors = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        corrected_lines = []
        
        for i, line in enumerate(lines, 1):
            # Remove newline for processing
            line = line.rstrip('\n\r')
            corrected, errors = process_line(line, i)
            
            if corrected is not None:
                corrected_lines.append(corrected)
            
            all_errors.extend(errors)
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(corrected_lines))
            if corrected_lines:  # Add final newline if file not empty
                f.write('\n')
        
        return all_errors
    
    except Exception as e:
        return [f"ERROR: Could not process file: {str(e)}"]

def main():
    # Get current directory
    start_dir = Path.cwd()
    
    # Find all .txt files, excluding those in 'logic' folders or starting with '!'
    all_txt_files = start_dir.rglob('*.txt')
    txt_files = [
        f for f in all_txt_files 
        if 'logic' not in f.parts and not f.name.startswith('!')
    ]
    
    # Prepare log
    log_lines = []
    log_lines.append("=" * 60)
    log_lines.append("WILDCARD LINTER LOG")
    log_lines.append("=" * 60)
    log_lines.append(f"Starting directory: {start_dir}")
    log_lines.append(f"Files found: {len(txt_files)}")
    log_lines.append("=" * 60)
    
    total_errors = 0
    
    for filepath in txt_files:
        relative_path = filepath.relative_to(start_dir)
        log_lines.append(f"\nProcessing: {relative_path}")
        
        errors = process_file(filepath)
        
        if errors:
            total_errors += len(errors)
            for error in errors:
                log_lines.append(f"  {error}")
        else:
            log_lines.append("  No errors found")
    
    log_lines.append("\n" + "=" * 60)
    log_lines.append(f"SUMMARY: {total_errors} errors corrected across {len(txt_files)} files")
    log_lines.append("=" * 60)
    
    # Write log file
    log_content = '\n'.join(log_lines)
    with open(start_dir / 'log.txt', 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    # Display on screen
    print(log_content)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
    finally:
        pause_at_end()

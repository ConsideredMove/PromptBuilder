import os
from pathlib import Path
from datetime import datetime

def process_file_content(content, filename):
    """
    Replace single underscores with spaces, except when inside:
    - Double underscore wildcards (__...__) 
    - Parentheses (which may contain nested wildcards)
    
    Returns: (processed_content, replacement_count, error_message)
    """
    result = []
    in_wildcard = False
    paren_depth = 0
    replacement_count = 0
    
    i = 0
    while i < len(content):
        char = content[i]
        
        # Check for double underscore
        if i < len(content) - 1 and content[i:i+2] == '__':
            in_wildcard = not in_wildcard
            result.append('__')
            i += 2
            continue
        
        # Track parentheses
        if char == '(':
            paren_depth += 1
            result.append(char)
            i += 1
            continue
        
        if char == ')':
            paren_depth -= 1
            result.append(char)
            i += 1
            continue
        
        # Replace underscore only if not protected
        if char == '_' and not in_wildcard and paren_depth == 0:
            result.append(' ')
            replacement_count += 1
        else:
            result.append(char)
        
        i += 1
    
    # Check for malformed wildcards
    if in_wildcard:
        return None, 0, f"Malformed wildcard: unpaired __ detected"
    
    return ''.join(result), replacement_count, None

def process_directory(start_dir, log_file):
    """
    Process all .txt files in directory and subdirectories
    """
    start_dir = Path(start_dir)
    total_files = 0
    total_replacements = 0
    errors = []
    
    log_file.write(f"Starting wildcard underscore replacement\n")
    log_file.write(f"Directory: {start_dir}\n")
    log_file.write(f"Time: {datetime.now()}\n")
    log_file.write("=" * 60 + "\n\n")
    
    # Walk through all subdirectories
    for txt_file in start_dir.rglob('*.txt'):
        try:
            # Read file
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process content
            processed, count, error = process_file_content(content, txt_file.name)
            
            if error:
                error_msg = f"ERROR in {txt_file.relative_to(start_dir)}: {error}"
                errors.append(error_msg)
                log_file.write(error_msg + "\n")
                print(error_msg)
                continue
            
            # Write back if changes were made
            if count > 0:
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(processed)
                
                msg = f"Processed: {txt_file.relative_to(start_dir)} - {count} replacements"
                log_file.write(msg + "\n")
                print(msg)
                total_replacements += count
            else:
                msg = f"Processed: {txt_file.relative_to(start_dir)} - no changes needed"
                log_file.write(msg + "\n")
                print(msg)
            
            total_files += 1
            
        except Exception as e:
            error_msg = f"ERROR processing {txt_file.relative_to(start_dir)}: {str(e)}"
            errors.append(error_msg)
            log_file.write(error_msg + "\n")
            print(error_msg)
    
    # Summary
    log_file.write("\n" + "=" * 60 + "\n")
    log_file.write(f"SUMMARY\n")
    log_file.write(f"Files processed: {total_files}\n")
    log_file.write(f"Total replacements: {total_replacements}\n")
    log_file.write(f"Errors: {len(errors)}\n")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY")
    print(f"Files processed: {total_files}")
    print(f"Total replacements: {total_replacements}")
    print(f"Errors: {len(errors)}")

if __name__ == "__main__":
    # Get script directory
    script_dir = Path(__file__).parent
    log_path = script_dir / "wildcard_replacer.log"
    
    print(f"Processing directory: {script_dir}")
    print(f"Log file: {log_path}\n")
    
    # Open log file and process
    with open(log_path, 'w', encoding='utf-8') as log:
        process_directory(script_dir, log)
    
    print(f"\nLog written to: {log_path}")
    input("\nPress Enter to close...")

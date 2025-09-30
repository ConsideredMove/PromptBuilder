import re
from pathlib import Path
from collections import defaultdict

def find_all_wildcards():
    """Find all .txt files in current directory and subdirectories."""
    base_path = Path.cwd()
    return list(base_path.rglob("*.txt"))

def find_references(wildcard_name, files):
    """Find all references to a wildcard across all files."""
    # Case-insensitive pattern for __wildcard__
    pattern = re.compile(f"__{re.escape(wildcard_name)}__", re.IGNORECASE)
    
    references = defaultdict(list)
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            matches = pattern.finditer(content)
            
            for match in matches:
                # Find line number and line content
                line_start = content.rfind('\n', 0, match.start()) + 1
                line_end = content.find('\n', match.end())
                if line_end == -1:
                    line_end = len(content)
                
                line_content = content[line_start:line_end].strip()
                line_num = content[:match.start()].count('\n') + 1
                
                references[file_path].append({
                    'line_num': line_num,
                    'line': line_content,
                    'match': match.group()
                })
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    return references

def find_wildcard_file(wildcard_name, files):
    """Find the file corresponding to the wildcard name."""
    for file_path in files:
        if file_path.stem.lower() == wildcard_name.lower():
            return file_path
    return None

def preview_changes(old_name, new_name, wildcard_file, references):
    """Show what will be changed."""
    print("\n" + "="*60)
    print("PREVIEW OF CHANGES")
    print("="*60)
    
    if wildcard_file:
        print(f"\nFile to rename:")
        print(f"  {wildcard_file} -> {wildcard_file.parent / (new_name + '.txt')}")
    else:
        print(f"\nNo file named '{old_name}.txt' found (will only update references)")
    
    if references:
        print(f"\nReferences to update ({sum(len(refs) for refs in references.values())} total):")
        for file_path, refs in references.items():
            print(f"\n  {file_path} ({len(refs)} reference(s)):")
            for ref in refs[:3]:  # Show first 3 references per file
                print(f"    Line {ref['line_num']}: {ref['line']}")
            if len(refs) > 3:
                print(f"    ... and {len(refs) - 3} more")
    else:
        print("\nNo references found in any files.")
    
    print("\n" + "="*60)

def apply_changes(old_name, new_name, wildcard_file, references, files):
    """Apply the renaming changes and return updated file list."""
    pattern = re.compile(f"__{re.escape(old_name)}__", re.IGNORECASE)
    new_reference = f"__{new_name}__"
    
    # Update references in files
    updated_files = 0
    for file_path, refs in references.items():
        try:
            content = file_path.read_text(encoding='utf-8')
            new_content = pattern.sub(new_reference, content)
            file_path.write_text(new_content, encoding='utf-8')
            updated_files += 1
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
    
    # Rename the wildcard file itself
    if wildcard_file:
        try:
            new_path = wildcard_file.parent / (new_name + '.txt')
            wildcard_file.rename(new_path)
            print(f"\n✓ Renamed file: {wildcard_file.name} -> {new_path.name}")
        except Exception as e:
            print(f"Error renaming file: {e}")
    
    print(f"✓ Updated {updated_files} file(s) with references")
    print("\nRefactoring complete!")
    
    # Refresh file list
    return find_all_wildcards()

def main():
    print("Wildcard Refactoring Tool")
    print("="*60)
    
    # Initial scan
    files = find_all_wildcards()
    
    while True:
        print(f"\nCurrent file count: {len(files)}")
        
        # Get wildcard to rename
        old_name = input("\nEnter the wildcard name to rename (without underscores, or 'q' to quit): ").strip()
        if old_name.lower() == 'q':
            print("Exiting.")
            break
        if not old_name:
            print("No name provided.")
            continue
        
        # Find the wildcard file
        wildcard_file = find_wildcard_file(old_name, files)
        
        # Find all references
        print(f"\nSearching for references to '__{old_name}__'...")
        references = find_references(old_name, files)
        
        if not wildcard_file and not references:
            print(f"\nNo file named '{old_name}.txt' and no references found. Nothing to do.")
            continue
        
        # Get new name
        new_name = input("\nEnter the new wildcard name: ").strip()
        if not new_name:
            print("No new name provided.")
            continue
        
        # Preview changes
        preview_changes(old_name, new_name, wildcard_file, references)
        
        # Confirm
        confirm = input("\nProceed with these changes? (y/n): ").strip().lower()
        if confirm == 'y':
            files = apply_changes(old_name, new_name, wildcard_file, references, files)
        else:
            print("\nCancelled. No changes made.")

if __name__ == "__main__":
    main()

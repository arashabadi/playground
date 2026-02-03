import os
import json
import base64
import time
from pathlib import Path

def is_binary(path):
    """Simple check to avoid encoding binary blobs as plain text."""
    try:
        with open(path, 'tr') as f:
            f.read(1024)
            return False
    except:
        return True

def bundle_repo(root_dir, output_file="ai_studio_bundle.json"):
    root = Path(root_dir).resolve()
    
    # Universal ignore patterns for all types of repos
    ignore = {
        '.git', '.svn', '.hg', 'node_modules', '__pycache__', 
        '.venv', 'venv', 'env', '.idea', '.vscode', '.DS_Store',
        'build', 'dist', '.gemini', 'target'
    }

    bundle_files = []
    for path in root.rglob('*'):
        if any(part in ignore for part in path.parts) or path.is_dir():
            continue
            
        try:
            content = path.read_bytes()
            encoded = base64.b64encode(content).decode('utf-8')
            
            file_meta = {
                "name": str(path.relative_to(root)),
                "type": "application/octet-stream" if is_binary(path) else "text/plain",
                "size": len(content),
                "lastModified": int(path.stat().st_mtime * 1000),
                "data": encoded
            }
            # AI Studio expects the file entry itself to be a stringified JSON
            bundle_files.append(json.dumps(file_meta))
        except Exception as e:
            print(f"Skipping {path}: {e}")

    # Build the special nested AI Studio format
    inner_msg = [{
        "id": 1,
        "author": "user",
        "payload": {
            "type": "text",
            "text": f"Universal Bundle of: {root.name}",
            "files": bundle_files
        },
        "createdTimestamp": {"seconds": int(time.time()), "nanos": 0}
    }]

    final_json = {
        "chunkedPrompt": {
            "chunks": [{"role": "user", "text": json.dumps(inner_msg)}]
        }
    }

    with open(output_file, 'w') as f:
        json.dump(final_json, f, indent=2)
    
    print(f"Done! Created {output_file} with {len(bundle_files)} files.")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    bundle_repo(target)

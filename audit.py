import os
import re
from pathlib import Path

def audit_portfolio():
    root = Path(__file__).parent
    modules = ["Module01", "Module02", "Module03", "Module04"]
    
    print("\n" + "="*50)
    print("🚀 SANJAY'S PORTFOLIO AUDITOR")
    print("="*50)

    # 1. Check Reflections
    print("\n📝 Checking Reflections (Rubric Requirement):")
    for i in range(1, 5):
        ref_file = root / "Reflections" / f"ref{i:02d}.md"
        if ref_file.exists():
            print(f"  ✅ Found: {ref_file.name}")
        else:
            print(f"  ❌ MISSING: {ref_file.name}")

    # 2. Check Learning Goal Links in READMEs
    for mod in modules:
        print(f"\n📁 Auditing {mod} Evidence Links:")
        readme = root / mod / "README.md"
        
        if not readme.exists():
            print(f"  ❌ MISSING README: {mod}/README.md")
            continue
            
        content = readme.read_text(encoding="utf-8")
        
        # Regex to find markdown links: [Text](./file.md) or [Text](../file.md)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        local_links = [link for link in links if not link[1].startswith('http')]
        
        if not local_links:
            print("  ⚠️ No local evidence links found in this README.")
            continue
            
        for text, path_str in local_links:
            # Resolve the path relative to the README
            target_file = (readme.parent / path_str).resolve()
            
            if target_file.exists():
                print(f"  ✅ Verified: [{text}] -> {target_file.name}")
            else:
                print(f"  ❌ BROKEN LINK: [{text}] points to {path_str} (File not found!)")

    print("\n" + "="*50)

if __name__ == "__main__":
    audit_portfolio()
    
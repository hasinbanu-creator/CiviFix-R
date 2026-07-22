import re

def fix_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # We need to map img.type or asset.type correctly.
    # We will search for: type: img.type || "image/jpeg"
    # and replace with: type: (img.type === 'image' ? 'image/jpeg' : img.type) || "image/jpeg"
    
    content = re.sub(r'type:\s*(img|asset)\.type\s*\|\|\s*"image/jpeg"', 
                     r"type: (\1.type === 'image' ? 'image/jpeg' : \1.type) || 'image/jpeg'", 
                     content)

    with open(filepath, "w") as f:
        f.write(content)

fix_file("civifix-frontend/src/screens/Complaints/ComplaintPreviewScreen.js")
fix_file("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js")
fix_file("civifix-frontend/src/screens/Complaints/CreateComplaintScreen.js")

print("MIME type mapping applied.")

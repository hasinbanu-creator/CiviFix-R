import re
import glob

files_to_fix = [
    "civifix-frontend/src/screens/Complaints/ComplaintPreviewScreen.js",
    "civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js"
]

for file_path in files_to_fix:
    with open(file_path, "r") as f:
        content = f.read()
    
    # Ensure Platform is imported
    if "import { Platform" not in content and "import {Platform" not in content:
        if "from 'react-native';" in content:
            content = re.sub(r"(import \{[^}]+)\}(\s*from 'react-native';)", r"\1, Platform\2", content)
        else:
            content = "import { Platform } from 'react-native';\n" + content
            
    # Fix the dynamic import logic
    content = content.replace("import('react-native').Platform?.OS === 'android'", "Platform.OS === 'android'")
    
    with open(file_path, "w") as f:
        f.write(content)

with open("civifix-frontend/src/services/authService.js", "r") as f:
    content = f.read()

# Fix transformRequest which shouldn't be overridden if we want default Axios behavior, OR we keep it if we want raw bypass
content = re.sub(r",\s*transformRequest: \(data, headers\) => \{\s*return data;\s*\}", "", content)
content = re.sub(r"headers: \{\s*\},?", "", content)

with open("civifix-frontend/src/services/authService.js", "w") as f:
    f.write(content)

print("Files fixed.")

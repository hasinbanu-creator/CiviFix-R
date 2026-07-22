import re

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "r") as f:
    content = f.read()

# Make sure Platform is imported at the top
if "import { Platform" not in content and "import {Platform" not in content:
    content = "import { Platform } from 'react-native';\n" + content

old_code = """      selectedProofImages.forEach((img, index) => {
        formData.append("images", img);
      });"""

new_code = """      selectedProofImages.forEach((img, index) => {
        let fileUri = img.uri;
        if (Platform.OS === 'android' && !fileUri.startsWith('file://') && !fileUri.startsWith('content://')) {
          fileUri = 'file://' + fileUri;
        }
        formData.append("images", {
          uri: fileUri,
          name: img.name || `proof-${index}.jpg`,
          type: img.type || "image/jpeg"
        });
      });"""

content = content.replace(old_code, new_code)
with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "w") as f:
    f.write(content)

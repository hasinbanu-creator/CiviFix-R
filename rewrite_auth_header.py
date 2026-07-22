import re

with open("civifix-frontend/src/services/authService.js", "r") as f:
    content = f.read()

# Fix createComplaint
content = re.sub(
    r"headers: \{\n\s*'Content-Type': 'multipart/form-data'\n\s*\},",
    "headers: {\n          // Let Axios generate boundary\n        },",
    content
)

with open("civifix-frontend/src/services/authService.js", "w") as f:
    f.write(content)

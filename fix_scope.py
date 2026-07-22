import re

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "r") as f:
    content = f.read()

# Extract the function
func_regex = r"  const getFinalImageUri = \(img\) => \{\n    let finalUri = img;\n    if \(img && typeof img === 'string' && !img.startsWith\('http'\) && !img.startsWith\('data:'\)\) \{\n      const base = API_URL \? API_URL.replace\(/\\\\/api\\\\/v1\\\\/\?\$\/, ''\) : '';\n      finalUri = `\$\{base\}\$\{img.startsWith\('/'\) \? '' : '/'\}\$\{img\}`;\n    \}\n    console.log\(`\[ComplaintDetailScreen\] Image Source: \$\{img\} -> Final URI: \$\{finalUri\}`\);\n    return finalUri;\n  \};\n"

# The original definition has a slightly different indentation or exact matches, let's just use string replace.
original_func = """  const getFinalImageUri = (img) => {
    let finalUri = img;
    if (img && typeof img === 'string' && !img.startsWith('http') && !img.startsWith('data:')) {
      const base = API_URL ? API_URL.replace(/\/api\/v1\/?$/, '') : '';
      finalUri = `${base}${img.startsWith('/') ? '' : '/'}${img}`;
    }
    console.log(`[ComplaintDetailScreen] Image Source: ${img} -> Final URI: ${finalUri}`);
    return finalUri;
  };
"""

# Remove it from the current location
if original_func in content:
    content = content.replace(original_func, "")
else:
    print("Could not find exact function block to remove.")

# Insert it outside the component, right before export const ComplaintDetailScreen = ...
insert_pos = content.find("export const ComplaintDetailScreen =")
if insert_pos != -1:
    content = content[:insert_pos] + original_func.replace("  const", "const") + "\n" + content[insert_pos:]
else:
    print("Could not find component start.")

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "w") as f:
    f.write(content)

print("Scope fixed.")

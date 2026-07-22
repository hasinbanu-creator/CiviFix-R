import re

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "r") as f:
    content = f.read()

helper = """
  const getFinalImageUri = (img) => {
    let finalUri = img;
    if (img && typeof img === 'string' && !img.startsWith('http') && !img.startsWith('data:')) {
      const base = API_URL ? API_URL.replace(/\/api\/v1\/?$/, '') : '';
      finalUri = `${base}${img.startsWith('/') ? '' : '/'}${img}`;
    }
    console.log(`[ComplaintDetailScreen] Image Source: ${img} -> Final URI: ${finalUri}`);
    return finalUri;
  };

  useEffect(() => {
    if (complaintImages.length > 0) {
      console.log("[ComplaintDetailScreen] Loaded complaint images array:", complaintImages);
    }
  }, [complaintImages]);
"""

# Insert the helper inside the component just before `return`
content = content.replace("  return (\n    <View style={styles.flex}>", helper + "\n  return (\n    <View style={styles.flex}>")

# Replace resolveImageUri(img, API_URL) with getFinalImageUri(img)
content = content.replace("resolveImageUri(img, API_URL)", "getFinalImageUri(img)")

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "w") as f:
    f.write(content)

print("ComplaintDetailScreen.js updated.")

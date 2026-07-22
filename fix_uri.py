import re

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "r") as f:
    content = f.read()

# Replace getFinalImageUri definition
old_func = """const getFinalImageUri = (img) => {
    let finalUri = img;
    if (img && typeof img === 'string' && !img.startsWith('http') && !img.startsWith('data:')) {
    const base = API_URL ? API_URL.replace(/\/api\/v1\/?$/, '') : '';
      finalUri = `${base}${img.startsWith('/') ? '' : '/'}${img}`;
    }
    console.log(`[ComplaintDetailScreen] Image Source: ${img} -> Final URI: ${finalUri}`);
    return finalUri;
  };"""

new_func = """const getFinalImageUri = (img) => {
    let finalUri = img;
    if (img && typeof img === 'string' && !img.startsWith('http') && !img.startsWith('data:')) {
      const base = API_URL ? API_URL.replace(/\\/api\\/v1\\/?$/, '') : '';
      // If the backend didn't include 'uploads/', we inject it.
      let path = img.startsWith('/') ? img : '/' + img;
      if (!path.startsWith('/uploads/')) {
        path = '/uploads' + path;
      }
      finalUri = `${base}${path}`;
    }
    console.log(`[ComplaintDetailScreen] Image Source: ${img} -> Final URI: ${finalUri}`);
    return finalUri;
  };"""

content = content.replace(old_func, new_func)

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "w") as f:
    f.write(content)

print("URI mapping fixed.")

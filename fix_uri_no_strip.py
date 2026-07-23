with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "r") as f:
    content = f.read()

old_func = """const getFinalImageUri = (img: string) => {
  let finalUri = img;
  if (img && typeof img === 'string' && !img.startsWith('http') && !img.startsWith('data:')) {
    let base = API_URL ? API_URL.replace(/\\/api\\/v1\\/?$/, '') : '';
    base = base.replace(/\\/$/, '');
    
    let path = img.startsWith('/') ? img : '/' + img;
    if (!path.startsWith('/uploads/')) {
      path = '/uploads' + path;
    }
    path = path.replace(/^\\/+/, '/');
    finalUri = `${base}${path}`;
  }
  return finalUri;
};"""

new_func = """const getFinalImageUri = (img: string) => {
  let finalUri = img;
  if (img && typeof img === 'string' && !img.startsWith('http') && !img.startsWith('data:')) {
    // Keep the /api/v1 prefix because the backend proxy might require it for routing.
    let base = API_URL || '';
    base = base.replace(/\\/$/, '');
    
    let path = img.startsWith('/') ? img : '/' + img;
    if (!path.startsWith('/uploads/')) {
      path = '/uploads' + path;
    }
    path = path.replace(/^\\/+/, '/');
    finalUri = `${base}${path}`;
  }
  return finalUri;
};"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "w") as f:
        f.write(content)
    print("Frontend URL logic updated.")
else:
    print("Old function not found.")

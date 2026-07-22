import re

with open("civifix-frontend/src/services/authService.js", "r") as f:
    content = f.read()

# Replace createComplaint
create_regex = r"  createComplaint: async \(complaintData\) => \{[\s\S]*?catch \(err\) \{\n      console\.error\(\"\[authService\] createComplaint failed:\"\);\n      if \(err\.response\) \{\n        console\.error\(\"HTTP status:\", err\.response\.status\);\n        console\.error\(\"Response body:\", err\.response\.data\);\n      \} else \{\n        console\.error\(err\.message \|\| err\);\n      \}\n      throw err;\n    \}\n  \},"

create_new = """  createComplaint: async (complaintData) => {
    console.log("========== TRACE: createComplaint ==========");
    console.log("1. Entered authService.createComplaint()");
    const url = `${api.defaults.baseURL}${ENDPOINTS.CREATE_COMPLAINT}`;
    console.log("2. URL computed:", url);
    
    const token = await AsyncStorage.getItem("authToken");
    const maskedToken = token ? `${token.substring(0, 4)}...${token.substring(token.length - 4)}` : "null";
    console.log("3. Authorization header: Bearer", maskedToken);
    
    console.log("4. Validating FormData...");
    if (complaintData && complaintData._parts) {
      console.log("   - FormData keys:", complaintData._parts.map(p => p[0]));
      const images = complaintData._parts.filter(p => p[0] === 'images');
      images.forEach((img, i) => {
        console.log(`   - Image ${i + 1} URI:`, img[1]?.uri);
        console.log(`   - Image ${i + 1} MIME type:`, img[1]?.type);
      });
    }

    try {
      console.log("5. Calling fetch()...");
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Accept": "application/json"
          // CRITICAL: Do NOT set Content-Type manually for FormData in React Native fetch!
        },
        body: complaintData
      });
      console.log("6. fetch() completed without crashing!");
      console.log("7. Response status:", response.status);
      
      const responseData = await response.json();
      if (!response.ok) {
        console.error("8. Server returned error:", responseData);
        throw new Error(responseData.message || "Failed to create complaint");
      }
      return responseData;
    } catch (err) {
      console.error("6. fetch() or execution crashed before returning a response!");
      console.error("   -> Error:", err.message);
      console.error("   -> Stack Trace:", err.stack);
      throw err;
    }
  },"""

content = re.sub(create_regex, create_new, content)

# Replace inspectorResolveComplaint
resolve_regex = r"  inspectorResolveComplaint: async \(complaintId, payload\) => \{[\s\S]*?catch \(err\) \{\n      console\.error\(\"\[authService\] inspectorResolveComplaint failed:\"\);\n      if \(err\.response\) \{\n        console\.error\(\"HTTP status:\", err\.response\.status\);\n        console\.error\(\"Response body:\", err\.response\.data\);\n      \} else \{\n        console\.error\(err\.message \|\| err\);\n      \}\n      throw err;\n    \}\n  \},"

resolve_new = """  inspectorResolveComplaint: async (complaintId, payload) => {
    console.log("========== TRACE: inspectorResolveComplaint ==========");
    console.log("1. Entered authService.inspectorResolveComplaint()");
    const url = `${api.defaults.baseURL}/inspector/complaints/${complaintId}/resolve`;
    console.log("2. URL computed:", url);
    
    const token = await AsyncStorage.getItem("authToken");
    const maskedToken = token ? `${token.substring(0, 4)}...${token.substring(token.length - 4)}` : "null";
    console.log("3. Authorization header: Bearer", maskedToken);
    
    console.log("4. Validating FormData...");
    if (payload && payload._parts) {
      console.log("   - FormData keys:", payload._parts.map(p => p[0]));
      const images = payload._parts.filter(p => p[0] === 'images');
      images.forEach((img, i) => {
        console.log(`   - Image ${i + 1} URI:`, img[1]?.uri);
        console.log(`   - Image ${i + 1} MIME type:`, img[1]?.type);
      });
    }

    try {
      console.log("5. Calling fetch()...");
      const response = await fetch(url, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Accept": "application/json"
          // Do NOT set Content-Type manually
        },
        body: payload
      });
      console.log("6. fetch() completed without crashing!");
      console.log("7. Response status:", response.status);
      
      const responseData = await response.json();
      if (!response.ok) {
        console.error("8. Server returned error:", responseData);
        throw new Error(responseData.message || "Failed to resolve complaint");
      }
      return responseData;
    } catch (err) {
      console.error("6. fetch() or execution crashed before returning a response!");
      console.error("   -> Error:", err.message);
      console.error("   -> Stack Trace:", err.stack);
      throw err;
    }
  },"""

content = re.sub(resolve_regex, resolve_new, content)

with open("civifix-frontend/src/services/authService.js", "w") as f:
    f.write(content)

print("Rewritten.")

import re

with open("civifix-frontend/src/services/authService.js", "r") as f:
    content = f.read()

# Fix createComplaint
create_old = """  createComplaint: async (complaintData) => {
    const response = await api.post(ENDPOINTS.CREATE_COMPLAINT, complaintData, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    return unwrapResponse(response);
  },"""

create_new = """  createComplaint: async (complaintData) => {
    console.log("[authService] POST", ENDPOINTS.CREATE_COMPLAINT, complaintData);
    // Explicitly removing manual Content-Type header so axios can auto-generate the boundary
    const response = await api.post(ENDPOINTS.CREATE_COMPLAINT, complaintData);
    return unwrapResponse(response);
  },"""

content = content.replace(create_old, create_new)

# Fix inspectorResolveComplaint
resolve_old = """  inspectorResolveComplaint: async (complaintId, payload) => {
    const res = await api.put(`/inspector/complaints/${complaintId}/resolve`, payload, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    return unwrapResponse(res);
  },"""

resolve_new = """  inspectorResolveComplaint: async (complaintId, payload) => {
    console.log("[authService] PUT /inspector/complaints/" + complaintId + "/resolve", payload);
    // Explicitly removing manual Content-Type header so axios can auto-generate the boundary
    const res = await api.put(`/inspector/complaints/${complaintId}/resolve`, payload);
    return unwrapResponse(res);
  },"""

content = content.replace(resolve_old, resolve_new)

with open("civifix-frontend/src/services/authService.js", "w") as f:
    f.write(content)


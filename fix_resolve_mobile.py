import re

with open("civifix-frontend/src/services/authService.js", "r") as f:
    content = f.read()

resolve_old = """  inspectorResolveComplaint: async (complaintId, payload = {}) => {
    const res = await api.put(`/inspector/complaints/${complaintId}/resolve`, {
      proof_images: payload.proof_images || [],
      note: payload.note || undefined,
    });
    return unwrapResponse(res);
  },"""

resolve_new = """  inspectorResolveComplaint: async (complaintId, payload) => {
    const res = await api.put(`/inspector/complaints/${complaintId}/resolve`, payload, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    return unwrapResponse(res);
  },"""

content = content.replace(resolve_old, resolve_new)

with open("civifix-frontend/src/services/authService.js", "w") as f:
    f.write(content)


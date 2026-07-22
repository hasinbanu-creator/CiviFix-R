import re

with open("civifix-frontend/src/services/authService.js", "r") as f:
    content = f.read()

create_complaint_old = """  createComplaint: async (complaintData) => {
    const response = await api.post(ENDPOINTS.CREATE_COMPLAINT, complaintData);
    return unwrapResponse(response);
  },"""

create_complaint_new = """  createComplaint: async (complaintData) => {
    const response = await api.post(ENDPOINTS.CREATE_COMPLAINT, complaintData, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    return unwrapResponse(response);
  },"""

content = content.replace(create_complaint_old, create_complaint_new)

with open("civifix-frontend/src/services/authService.js", "w") as f:
    f.write(content)


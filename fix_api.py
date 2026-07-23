with open("civifix-web/src/services/api.ts", "r") as f:
    content = f.read()

if "submitFeedback" not in content:
    new_methods = """
  submitFeedback: async (id: string, data: any) => {
    const response = await api.put(ENDPOINTS.SUBMIT_FEEDBACK(id), null, { params: data });
    return response.data;
  },

  reopenComplaint: async (id: string, reason: string) => {
    const response = await api.put(ENDPOINTS.REOPEN_COMPLAINT(id), null, { params: { reason } });
    return response.data;
  },
"""
    content = content.replace(
        "resolveComplaintWithImages: async (id: string, formData: FormData) => {",
        new_methods + "\n  resolveComplaintWithImages: async (id: string, formData: FormData) => {"
    )
    with open("civifix-web/src/services/api.ts", "w") as f:
        f.write(content)
    print("Added methods to api.ts")

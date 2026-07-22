import re

with open("civifix-web/src/app/(dashboard)/complaints/create/page.tsx", "r") as f:
    content = f.read()

submit_old = """      const formData = new FormData();
      Object.entries(form).forEach(([key, value]) => {
        formData.append(key, value);
      });
      
      selectedImages.forEach((file) => {
        formData.append("images", file);
      });"""

submit_new = """      const formData = new FormData();
      formData.append("ward_id", form.ward_id);
      formData.append("complaint_type", form.complaint_type);
      formData.append("description", form.description);
      formData.append("priority", form.priority);
      formData.append("latitude", form.latitude);
      formData.append("longitude", form.longitude);
      if (form.address) formData.append("address", form.address);
      if (form.citizen_note) formData.append("citizen_note", form.citizen_note.trim());
      
      selectedImages.forEach((file) => {
        formData.append("images", file);
      });"""

content = content.replace(submit_old, submit_new)

with open("civifix-web/src/app/(dashboard)/complaints/create/page.tsx", "w") as f:
    f.write(content)


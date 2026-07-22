import re

with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "r") as f:
    content = f.read()

# Make proof images required in UI
content = content.replace(
    "Proof Images (Optional)",
    "Proof Images (Required)"
)

# Update resolveStatus logic
resolve_old = """  const resolveStatus = async () => {
    try {
      setUpdating(true);
      
      if (selectedProofImages.length > 0) {
        const formData = new FormData();
        selectedProofImages.forEach(img => {
          formData.append("images", img);
        });
        await complaintsApi.resolveComplaintWithImages(id, formData);
      } else {
        await authService.inspectorResolveComplaint(id);
      }
      
      setShowResolveModal(false);"""

resolve_new = """  const resolveStatus = async () => {
    if (selectedProofImages.length === 0) {
      alert("Please upload at least one proof image to resolve this complaint.");
      return;
    }
    try {
      setUpdating(true);
      
      const formData = new FormData();
      selectedProofImages.forEach(img => {
        formData.append("images", img);
      });
      await complaintsApi.resolveComplaintWithImages(id, formData);
      
      setShowResolveModal(false);"""

content = content.replace(resolve_old, resolve_new)

# Make sure submit button is disabled if no images
button_old = """<button
                  onClick={resolveStatus}
                  disabled={updating}
                  className="flex-1 py-4 px-6 bg-success hover:bg-success/90 text-success-foreground rounded-2xl font-black text-sm tracking-wide disabled:opacity-70 flex items-center justify-center gap-2"
                >"""

button_new = """<button
                  onClick={resolveStatus}
                  disabled={updating || selectedProofImages.length === 0}
                  className="flex-1 py-4 px-6 bg-success hover:bg-success/90 text-success-foreground rounded-2xl font-black text-sm tracking-wide disabled:opacity-70 flex items-center justify-center gap-2"
                >"""

content = content.replace(button_old, button_new)

with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "w") as f:
    f.write(content)


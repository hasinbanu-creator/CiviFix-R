import re

with open("civifix-frontend/src/screens/Complaints/CreateComplaintScreen.js", "r") as f:
    content = f.read()

# Remove the uploadImagesToServer call and just pass selectedImages in form
submit_old = """  const submit = async () => {
    if (!validate()) return;

    try {
      setLoading(true);
      const uploadedImageUrls = await uploadImagesToServer();
      const nextForm = { ...form, image_urls: uploadedImageUrls };

      navigation.navigate("ComplaintPreview", {
        form: nextForm,
        ward: wardItems.find((w) => w.value === form.ward_id),
        selectedType,
        selectedPri,
      });
    } catch {
      setServerError("Unable to upload photos. Please try again.");
    } finally {
      setLoading(false);
    }
  };"""

submit_new = """  const submit = async () => {
    if (!validate()) return;

    try {
      setLoading(true);
      // Removed pre-upload. We pass raw images to preview screen.
      const nextForm = { ...form, images: selectedImages };

      navigation.navigate("ComplaintPreview", {
        form: nextForm,
        ward: wardItems.find((w) => w.value === form.ward_id),
        selectedType,
        selectedPri,
      });
    } catch {
      setServerError("Unable to proceed. Please try again.");
    } finally {
      setLoading(false);
    }
  };"""

content = content.replace(submit_old, submit_new)

with open("civifix-frontend/src/screens/Complaints/CreateComplaintScreen.js", "w") as f:
    f.write(content)


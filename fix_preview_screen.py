import re

with open("civifix-frontend/src/screens/Complaints/ComplaintPreviewScreen.js", "r") as f:
    content = f.read()

handleSubmit_old = """  const handleSubmit = async () => {
    try {
      setSubmitting(true);

      const payload = {
        ward_id: form.ward_id,
        complaint_type: form.complaint_type,
        description: form.description,
        priority: form.priority,
        latitude: parseFloat(form.latitude),
        longitude: parseFloat(form.longitude),
        address: form.address,
        citizen_note: form.citizen_note ? form.citizen_note.trim() : undefined,
        image_urls: Array.isArray(form.image_urls) ? form.image_urls : [],
      };

      const created = await authService.createComplaint(payload);
      
      // Navigate to Success Screen
      navigation.replace("ComplaintSuccess", { complaint: created });
    } catch (err) {
      alert(getErrorMessage(err, "Unable to submit complaint."));
    } finally {
      setSubmitting(false);
    }
  };"""

handleSubmit_new = """  const handleSubmit = async () => {
    try {
      setSubmitting(true);

      const formData = new FormData();
      formData.append("ward_id", form.ward_id);
      formData.append("complaint_type", form.complaint_type);
      formData.append("description", form.description);
      formData.append("priority", form.priority);
      formData.append("latitude", form.latitude.toString());
      formData.append("longitude", form.longitude.toString());
      if (form.address) formData.append("address", form.address);
      if (form.citizen_note) formData.append("citizen_note", form.citizen_note.trim());
      
      if (Array.isArray(form.images)) {
        form.images.forEach((img, index) => {
          formData.append("images", {
            uri: img.uri,
            name: img.name || `photo-${index}.jpg`,
            type: img.type || "image/jpeg"
          });
        });
      }

      const created = await authService.createComplaint(formData);
      
      navigation.replace("ComplaintSuccess", { complaint: created });
    } catch (err) {
      alert(getErrorMessage(err, "Unable to submit complaint."));
    } finally {
      setSubmitting(false);
    }
  };"""

content = content.replace(handleSubmit_old, handleSubmit_new)

# Also fix the image previews to read from local URI since they are not uploaded yet
preview_images_old = """        {/* Uploaded Photos */}
        {Array.isArray(form.image_urls) && form.image_urls.length > 0 ? (
          <View style={styles.card}>
            <View style={styles.row}>
              <Icon name="image-multiple-outline" size={20} color={COLORS.primary} />
              <Text style={styles.sectionTitle}>Attached Photos</Text>
            </View>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.imageScroll}>
              {form.image_urls.map((img, idx) => {
                const resolvedUri = resolveImageUri(img, API_URL);
                return <Image key={`${img}-${idx}`} source={{ uri: resolvedUri }} style={styles.previewImage} />;
              })}
            </ScrollView>
          </View>
        ) : null}"""

preview_images_new = """        {/* Uploaded Photos */}
        {Array.isArray(form.images) && form.images.length > 0 ? (
          <View style={styles.card}>
            <View style={styles.row}>
              <Icon name="image-multiple-outline" size={20} color={COLORS.primary} />
              <Text style={styles.sectionTitle}>Attached Photos</Text>
            </View>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.imageScroll}>
              {form.images.map((img, idx) => (
                <Image key={`img-${idx}`} source={{ uri: img.uri }} style={styles.previewImage} />
              ))}
            </ScrollView>
          </View>
        ) : null}"""

content = content.replace(preview_images_old, preview_images_new)

with open("civifix-frontend/src/screens/Complaints/ComplaintPreviewScreen.js", "w") as f:
    f.write(content)


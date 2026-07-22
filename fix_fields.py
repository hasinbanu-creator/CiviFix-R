import re

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "r") as f:
    content = f.read()

# I will add the requested logs inside the component body, inside useEffect
new_log = """
  useEffect(() => {
    console.log("--- IMAGE LOGS ---");
    console.log("complaint.images:", complaint?.images);
    console.log("complaint.image_urls:", complaint?.image_urls);
    console.log("complaint.proof_images:", complaint?.proof_images);
  }, [complaint]);
"""

# Replace the existing useEffect logging if it exists, or just add it
old_log = """  useEffect(() => {
    if (complaintImages.length > 0) {
      console.log("[ComplaintDetailScreen] Loaded complaint images array:", complaintImages);
    }
  }, [complaintImages]);"""

if old_log in content:
    content = content.replace(old_log, new_log)

# Fix the complaintImages declaration to use the correct fields
# It seems the backend probably returns `images` instead of `image_urls` or `proof_images`
old_array = """  const complaintImages = Array.isArray(complaint?.image_urls) && complaint.image_urls.length > 0
    ? complaint.image_urls
    : Array.isArray(complaint?.proof_images) && complaint.proof_images.length > 0
      ? complaint.proof_images
      : [];"""

new_array = """  // Extract citizen uploaded images or proof images
  let complaintImages = [];
  if (Array.isArray(complaint?.images) && complaint.images.length > 0) {
    complaintImages = complaint.images;
  } else if (Array.isArray(complaint?.image_urls) && complaint.image_urls.length > 0) {
    complaintImages = complaint.image_urls;
  } else if (Array.isArray(complaint?.proof_images) && complaint.proof_images.length > 0) {
    complaintImages = complaint.proof_images;
  }"""

content = content.replace(old_array, new_array)

with open("civifix-frontend/src/screens/Complaints/ComplaintDetailScreen.js", "w") as f:
    f.write(content)

print("Updated DetailScreen.")

import re

with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "r") as f:
    content = f.read()

log_effect = """
  useEffect(() => {
    if (complaint) {
      console.log("--- DEBUG LOGS ---");
      console.log("Complaint Response:", complaint);
      console.log("complaint.images:", complaint.images);
      console.log("complaint.image_urls:", complaint.image_urls);
      console.log("complaint.proof_images:", complaint.proof_images);
    }
  }, [complaint]);
"""

# Insert at the top of the component, just after the first few hooks.
# Let's find: const queryClient = useQueryClient();
insert_marker = "const queryClient = useQueryClient();"
if insert_marker in content and "console.log(\"--- DEBUG LOGS ---\");" not in content:
    content = content.replace(insert_marker, insert_marker + "\n" + log_effect)
    with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "w") as f:
        f.write(content)
    print("Added logs at the top.")
else:
    print("Could not find insert marker or already exists.")

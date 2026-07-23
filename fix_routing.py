import os

files = [
    "civifix-web/src/app/(dashboard)/dashboard/page.tsx",
    "civifix-web/src/app/(dashboard)/complaints/page.tsx"
]

for file in files:
    with open(file, "r") as f:
        content = f.read()

    # We want to replace `complaint._id || complaint.complaint_id` with `complaint.id || complaint._id || complaint.complaint_id`
    # Also `c._id || c.complaint_id` with `c.id || c._id || c.complaint_id`
    
    content = content.replace("complaint._id || complaint.complaint_id", "complaint.id || complaint._id || complaint.complaint_id")
    content = content.replace("c._id || c.complaint_id", "c.id || c._id || c.complaint_id")

    # In complaints/page.tsx, there's also an onClick that uses window.location.href. We should update that too.
    content = content.replace("window.location.href=`/complaints/${complaint._id || complaint.complaint_id}`", "window.location.href=`/complaints/${complaint.id || complaint._id || complaint.complaint_id}`")
    
    with open(file, "w") as f:
        f.write(content)

print("Routing fixed.")

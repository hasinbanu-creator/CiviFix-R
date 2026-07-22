import re

with open("civifix-frontend/src/screens/Complaints/ComplaintsListScreen.js", "r") as f:
    content = f.read()

# Replace any keyExtractor logic to guarantee uniqueness
content = re.sub(
    r"keyExtractor=\{\(item,\s*index\)\s*=>\s*.*\}",
    'keyExtractor={(item, index) => `${item?._id || item?.complaint_id || "c"}-${index}`}',
    content
)

with open("civifix-frontend/src/screens/Complaints/ComplaintsListScreen.js", "w") as f:
    f.write(content)


with open("civifix-frontend/src/screens/Admin/ComplaintMonitoringScreen.js", "r") as f:
    content = f.read()

content = re.sub(
    r"keyExtractor=\{\(item\)\s*=>\s*item\._id\}",
    'keyExtractor={(item, index) => `${item?._id || "a"}-${index}`}',
    content
)

with open("civifix-frontend/src/screens/Admin/ComplaintMonitoringScreen.js", "w") as f:
    f.write(content)


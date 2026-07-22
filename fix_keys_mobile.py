import re
import glob

# 1. Fix ComplaintsListScreen.js
with open("civifix-frontend/src/screens/Complaints/ComplaintsListScreen.js", "r") as f:
    content = f.read()

# Make sure we don't duplicate items when appending in loadComplaints
load_old = """      if (pageNum === 1) {
        setComplaints(data);
      } else {
        setComplaints(prev => [...prev, ...data]);
      }"""

load_new = """      if (pageNum === 1) {
        setComplaints(data);
      } else {
        setComplaints(prev => {
          const newItems = data.filter(d => !prev.some(p => p._id === d._id));
          return [...prev, ...newItems];
        });
      }"""

content = content.replace(load_old, load_new)

with open("civifix-frontend/src/screens/Complaints/ComplaintsListScreen.js", "w") as f:
    f.write(content)

# 2. Fix ComplaintMonitoringScreen.js
with open("civifix-frontend/src/screens/Admin/ComplaintMonitoringScreen.js", "r") as f:
    content = f.read()

load_old2 = """      if (pageNum === 1) {
        setComplaints(data);
      } else {
        setComplaints(prev => [...prev, ...data]);
      }"""

load_new2 = """      if (pageNum === 1) {
        setComplaints(data);
      } else {
        setComplaints(prev => {
          const newItems = data.filter(d => !prev.some(p => p._id === d._id));
          return [...prev, ...newItems];
        });
      }"""

content = content.replace(load_old2, load_new2)

with open("civifix-frontend/src/screens/Admin/ComplaintMonitoringScreen.js", "w") as f:
    f.write(content)


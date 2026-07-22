import re

with open("civifix-frontend/src/screens/Dashboard/DashboardScreen.js", "r") as f:
    content = f.read()

# Add statusFilter state
state_old = """  const [selectedWardId, setSelectedWardId] = useState("");
  const [complaints, setComplaints]     = useState([]);
  const [stats, setStats]               = useState({ total: 0, pending: 0, in_progress: 0, resolved: 0, rejected: 0 });"""

state_new = """  const [selectedWardId, setSelectedWardId] = useState("");
  const [complaints, setComplaints]     = useState([]);
  const [statusFilter, setStatusFilter] = useState("All");
  const [stats, setStats]               = useState({ total: 0, pending: 0, in_progress: 0, resolved: 0, rejected: 0 });"""

content = content.replace(state_old, state_new)

# Add useMemo for filteredComplaints
filtered_complaints_old = """      {/* ── Complaints List ───────────────────────────────────────────── */}
      <SectionTitle
        left={`Complaints in Ward${selectedWard ? ` #${selectedWard.ward_number}` : ""}`}
        rightComponent={
          <View style={{ flexDirection: "row", gap: 12 }}>
            <TouchableOpacity onPress={() => selectedWardId && loadComplaints(selectedWardId)}>
              <Icon name="refresh" size={20} color={COLORS.primary} />
            </TouchableOpacity>
            <TouchableOpacity onPress={() => {/* Search */}}>
              <Icon name="magnify" size={20} color={COLORS.primary} />
            </TouchableOpacity>
            <TouchableOpacity onPress={() => {/* Filter */}}>
              <Icon name="filter-variant" size={20} color={COLORS.primary} />
            </TouchableOpacity>
          </View>
        }
      />

      <ListCard
        empty={!loadingComplaints && complaints.length === 0}
        emptyLabel={selectedWardId
          ? "No complaints available for this ward."
          : "Select a ward to view complaints."
        }
      >
        {loadingComplaints
          ? <View style={{ padding: SPACING.xl }}><ActivityIndicator color={COLORS.primary} /></View>
          : complaints.map((c, i, arr) => (
              <InspectorComplaintItem"""

filtered_complaints_new = """      {/* ── Status Chips ───────────────────────────────────────────── */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: SPACING.md, marginBottom: SPACING.sm }}>
        {["All", "Pending", "In Progress", "Resolved", "Rejected"].map(status => {
          const isSelected = statusFilter === status;
          return (
            <TouchableOpacity
              key={status}
              onPress={() => setStatusFilter(status)}
              style={{
                paddingHorizontal: 16,
                paddingVertical: 8,
                borderRadius: 20,
                backgroundColor: isSelected ? COLORS.primary : COLORS.card,
                borderWidth: 1,
                borderColor: isSelected ? COLORS.primary : COLORS.border,
                marginRight: 8,
                ...SHADOWS.sm,
              }}
            >
              <Text style={{
                color: isSelected ? "#fff" : COLORS.textDark,
                fontWeight: isSelected ? "700" : "500",
                fontSize: FONT_SIZES.sm
              }}>
                {status}
              </Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>

      {/* ── Complaints List ───────────────────────────────────────────── */}
      <SectionTitle
        left={`Complaints in Ward${selectedWard ? ` #${selectedWard.ward_number}` : ""}`}
        rightComponent={
          <View style={{ flexDirection: "row", gap: 12 }}>
            <TouchableOpacity onPress={() => selectedWardId && loadComplaints(selectedWardId)}>
              <Icon name="refresh" size={20} color={COLORS.primary} />
            </TouchableOpacity>
          </View>
        }
      />

      <ListCard
        empty={!loadingComplaints && complaints.filter(c => {
          if (statusFilter === "All") return true;
          if (statusFilter === "Pending") return ["OPEN", "PENDING"].includes(c.status);
          if (statusFilter === "In Progress") return ["IN_PROGRESS", "WORKING", "ACCEPTED", "FIELD_VISIT", "APPROVAL"].includes(c.status);
          if (statusFilter === "Resolved") return ["RESOLVED", "CLOSED"].includes(c.status);
          if (statusFilter === "Rejected") return c.status === "REJECTED";
          return true;
        }).length === 0}
        emptyLabel={selectedWardId
          ? `No ${statusFilter === "All" ? "" : statusFilter.toLowerCase()} complaints available for this ward.`
          : "Select a ward to view complaints."
        }
      >
        {loadingComplaints
          ? <View style={{ padding: SPACING.xl }}><ActivityIndicator color={COLORS.primary} /></View>
          : complaints.filter(c => {
              if (statusFilter === "All") return true;
              if (statusFilter === "Pending") return ["OPEN", "PENDING"].includes(c.status);
              if (statusFilter === "In Progress") return ["IN_PROGRESS", "WORKING", "ACCEPTED", "FIELD_VISIT", "APPROVAL"].includes(c.status);
              if (statusFilter === "Resolved") return ["RESOLVED", "CLOSED"].includes(c.status);
              if (statusFilter === "Rejected") return c.status === "REJECTED";
              return true;
            }).map((c, i, arr) => (
              <InspectorComplaintItem"""

content = content.replace(filtered_complaints_old, filtered_complaints_new)

with open("civifix-frontend/src/screens/Dashboard/DashboardScreen.js", "w") as f:
    f.write(content)


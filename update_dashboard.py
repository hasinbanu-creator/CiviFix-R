import re

with open("civifix-web/src/app/(dashboard)/dashboard/page.tsx", "r") as f:
    content = f.read()

# First replace ROLE_META.INSPECTOR
role_meta_old = 'INSPECTOR:      { label: "Inspector",      color: "text-secondary", bg: "bg-secondary/20", gradient: "from-secondary to-slate-800" },'
role_meta_new = 'INSPECTOR:      { label: "Inspector",      color: "text-teal-100", bg: "bg-teal-800/40", gradient: "from-teal-800 to-teal-600" },'
content = content.replace(role_meta_old, role_meta_new)

# Now replace InspectorDashboard component
# from function InspectorDashboard() { ... down to } right before function AdminDashboard()

inspector_dashboard_new = """function InspectorDashboard() {
  const { user } = useAuth();
  const [wards, setWards] = useState<any[]>([]);
  const [selectedWardId, setSelectedWardId] = useState<string>("all");
  const [complaints, setComplaints] = useState<any[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [stats, setStats] = useState<any>({ total: 0, pending: 0, in_progress: 0, resolved: 0, rejected: 0 });
  const [isLoadingWards, setIsLoadingWards] = useState<boolean>(true);
  const [isLoadingComplaints, setIsLoadingComplaints] = useState<boolean>(false);
  
  const [statusFilter, setStatusFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");

  const refreshData = async (wardId: string) => {
    setIsLoadingComplaints(true);
    try {
      const res = await authService.getWardComplaints({
        ward_id: wardId === "all" ? "" : wardId,
        limit: 100,
      });
      const complaintsList = res?.complaints || res?.data || (Array.isArray(res) ? res : []);
      setComplaints(complaintsList);
      if (res?.stats) {
        setStats(res.stats);
      } else {
        const total = complaintsList.length;
        const pending = complaintsList.filter((c: any) => ["OPEN", "PENDING"].includes(c.status)).length;
        const in_progress = complaintsList.filter((c: any) => ["IN_PROGRESS", "WORKING", "ACCEPTED", "FIELD_VISIT", "APPROVAL"].includes(c.status)).length;
        const resolved = complaintsList.filter((c: any) => ["RESOLVED", "CLOSED"].includes(c.status)).length;
        const rejected = complaintsList.filter((c: any) => c.status === "REJECTED").length;
        setStats({ total, pending, in_progress, resolved, rejected });
      }
    } catch (error: any) {
      console.error(error);
      setComplaints([]);
    } finally {
      setIsLoadingComplaints(false);
    }
  };

  useEffect(() => {
    async function loadWards() {
      setIsLoadingWards(true);
      try {
        const res = await authService.getAllWards({ limit: 100 });
        let wardsList: any[] = [];
        if (Array.isArray(res)) wardsList = res;
        else if (Array.isArray(res?.data)) wardsList = res.data;
        else if (Array.isArray(res?.wards)) wardsList = res.wards;
        setWards(wardsList);
      } catch (error: any) {
        setLoadError("Failed to load wards.");
      } finally {
        setIsLoadingWards(false);
      }
    }
    loadWards();
  }, []);

  useEffect(() => {
    refreshData(selectedWardId);
  }, [selectedWardId]);

  const filteredComplaints = useMemo(() => {
    return complaints.filter(c => {
      if (statusFilter !== "All") {
        if (statusFilter === "Pending" && !["OPEN", "PENDING"].includes(c.status)) return false;
        if (statusFilter === "In Progress" && !["IN_PROGRESS", "WORKING", "ACCEPTED", "FIELD_VISIT", "APPROVAL"].includes(c.status)) return false;
        if (statusFilter === "Resolved" && !["RESOLVED", "CLOSED"].includes(c.status)) return false;
        if (statusFilter === "Rejected" && c.status !== "REJECTED") return false;
      }
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        const idMatch = (c.complaint_id || "").toLowerCase().includes(q);
        const typeMatch = (c.complaint_type || "").toLowerCase().includes(q);
        const locMatch = (c.address || "").toLowerCase().includes(q);
        const nameMatch = (c.citizen?.name || "").toLowerCase().includes(q);
        if (!idMatch && !typeMatch && !locMatch && !nameMatch) return false;
      }
      return true;
    });
  }, [complaints, statusFilter, searchQuery]);

  if (isLoadingWards) {
    return (
      <div className="p-10 flex flex-col items-center gap-3">
        <div className="w-10 h-10 border-4 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium text-slate-500">Loading wards…</p>
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="p-10 text-center flex flex-col items-center">
        <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
          <AlertCircle className="w-8 h-8 text-red-500" />
        </div>
        <p className="text-base font-bold text-slate-800">Ward Load Error</p>
        <p className="text-sm font-medium text-slate-500 mt-1">{loadError}</p>
        <button onClick={() => window.location.reload()} className="mt-4 px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-sm font-bold transition-colors">Retry</button>
      </div>
    );
  }

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Profile Stats Row (Teal Theme) */}
      <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 mb-8 mt-[-3rem] relative z-10 mx-4 md:mx-0 flex flex-wrap items-center justify-between">
        {[
          { label: "Total", value: stats.total || 0, filter: "All", color: "text-slate-800" },
          { label: "Pending", value: stats.pending || 0, filter: "Pending", color: "text-teal-600" },
          { label: "In Progress", value: stats.in_progress || 0, filter: "In Progress", color: "text-teal-500" },
          { label: "Resolved", value: stats.resolved || 0, filter: "Resolved", color: "text-teal-400" },
          { label: "Rejected", value: stats.rejected || 0, filter: "Rejected", color: "text-red-500" },
        ].map((s, idx) => (
          <button 
            key={s.label} 
            onClick={() => setStatusFilter(s.filter)}
            className={`flex-1 text-center py-2 px-2 hover:bg-slate-50 rounded-xl transition-colors ${idx !== 4 ? 'border-r border-slate-100' : ''} ${statusFilter === s.filter ? 'ring-2 ring-teal-100 bg-teal-50/50' : ''}`}
          >
            <p className={`text-3xl font-black ${s.color}`}>{s.value}</p>
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">{s.label}</p>
          </button>
        ))}
      </div>

      <div className="px-4 md:px-0">
        {/* Ward selection and Search */}
        <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex flex-col gap-1">
            <h3 className="text-lg font-bold text-slate-800">Select Ward</h3>
            <select
              value={selectedWardId}
              onChange={(e) => setSelectedWardId(e.target.value)}
              className="bg-white text-slate-700 font-semibold text-sm px-4 py-3 rounded-2xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-teal-500 min-w-[200px] shadow-sm cursor-pointer"
            >
              <option value="all">All Wards</option>
              {wards.map((ward) => (
                <option key={ward._id || ward.id} value={ward._id || ward.id}>
                  {ward.ward_name} (Ward #{ward.ward_number})
                </option>
              ))}
            </select>
          </div>
          
          <div className="relative flex-1 max-w-md mt-6 md:mt-0">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search ID, type, location or name..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-2xl pl-12 pr-4 py-3 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-teal-500 shadow-sm"
            />
          </div>
        </div>

        {/* Filter Chips */}
        <div className="flex flex-wrap gap-2 mb-8">
          {["All", "Pending", "In Progress", "Resolved", "Rejected"].map(filter => (
            <button
              key={filter}
              onClick={() => setStatusFilter(filter)}
              className={`px-4 py-2 rounded-full text-sm font-bold transition-all shadow-sm flex items-center ${
                statusFilter === filter 
                  ? "bg-teal-600 text-white shadow-teal-500/30 ring-2 ring-teal-200 ring-offset-1" 
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
              }`}
            >
              {filter} 
              <span className={`ml-2 px-2 py-0.5 rounded-full text-xs font-black ${statusFilter === filter ? 'bg-teal-700 text-teal-100' : 'bg-slate-100 text-slate-500'}`}>
                {filter === "All" ? stats.total : filter === "Pending" ? stats.pending : filter === "In Progress" ? stats.in_progress : filter === "Resolved" ? stats.resolved : stats.rejected}
              </span>
            </button>
          ))}
        </div>

        {/* Table */}
        <div className="bg-white border border-slate-200 rounded-3xl shadow-sm overflow-hidden mb-8">
          <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
             <h3 className="text-lg font-bold text-slate-800">
               {selectedWardId === "all" ? "All Complaints" : `Complaints in ${wards.find(w => (w._id||w.id) === selectedWardId)?.ward_name || "Selected Ward"}`}
             </h3>
             <button onClick={() => refreshData(selectedWardId)} className="text-teal-600 hover:text-teal-700 text-sm font-bold flex items-center gap-2 transition-colors">
               Refresh <Activity className="w-4 h-4" />
             </button>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse whitespace-nowrap">
              <thead>
                <tr className="border-b border-slate-100 text-xs font-black text-slate-500 uppercase tracking-widest bg-slate-50/50">
                  <th className="p-5">Complaint ID</th>
                  <th className="p-5">Type</th>
                  <th className="p-5">Location</th>
                  <th className="p-5">Date</th>
                  <th className="p-5">Status</th>
                  <th className="p-5">Priority</th>
                  <th className="p-5 text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {isLoadingComplaints ? (
                  <tr>
                    <td colSpan={7} className="p-10 text-center">
                      <div className="w-8 h-8 border-4 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
                    </td>
                  </tr>
                ) : filteredComplaints.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="p-10 text-center">
                      <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <ClipboardList className="w-8 h-8 text-slate-400" />
                      </div>
                      <p className="text-base font-bold text-slate-700">No complaints found</p>
                      <p className="text-sm font-medium text-slate-500 mt-1">Try adjusting your filters or search query.</p>
                    </td>
                  </tr>
                ) : (
                  filteredComplaints.map((c: any) => {
                    const statusStyles = STATUS_STYLES[c.status as ComplaintStatus] || STATUS_STYLES.OPEN;
                    const typeMeta = TYPE_META[(c.complaint_type as ComplaintType)] || TYPE_META.OTHER;
                    
                    return (
                      <tr key={c._id || c.complaint_id} className="border-b border-slate-50 hover:bg-slate-50/50 transition-colors group">
                        <td className="p-5">
                          <p className="text-sm font-black text-slate-700">{c.complaint_id || "#CIV-NEW"}</p>
                          <p className="text-xs font-medium text-slate-500 mt-0.5">{c.citizen?.name || "Citizen"}</p>
                        </td>
                        <td className="p-5">
                          <div className="flex items-center gap-3">
                            <div className={`w-8 h-8 rounded-lg ${typeMeta.bg} flex items-center justify-center shrink-0`}>
                              <typeMeta.icon className={`w-4 h-4 ${typeMeta.color}`} />
                            </div>
                            <span className="text-sm font-bold text-slate-700">{typeMeta.title}</span>
                          </div>
                        </td>
                        <td className="p-5">
                          <p className="text-sm font-medium text-slate-600 max-w-[200px] truncate" title={c.address}>{c.address || "No address provided"}</p>
                        </td>
                        <td className="p-5">
                          <p className="text-sm font-medium text-slate-600">
                            {c.created_at ? new Date(c.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) : "N/A"}
                          </p>
                        </td>
                        <td className="p-5">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${statusStyles.bg} ${statusStyles.color}`}>
                            {statusStyles.label}
                          </span>
                        </td>
                        <td className="p-5">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${c.priority === 'HIGH' ? 'bg-red-100 text-red-600' : 'bg-slate-100 text-slate-600'}`}>
                            {c.priority || "MEDIUM"}
                          </span>
                        </td>
                        <td className="p-5 text-right">
                          <Link href={`/complaints/${c._id || c.complaint_id}`} className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-slate-100 text-slate-600 hover:bg-teal-100 hover:text-teal-700 transition-colors">
                            <ChevronRight className="w-5 h-5" />
                          </Link>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}"""

pattern = re.compile(r"function InspectorDashboard\(\) \{.*?\n\}\n\nfunction AdminDashboard\(\) \{", re.DOTALL)
content = pattern.sub(inspector_dashboard_new + "\n\nfunction AdminDashboard() {", content)

with open("civifix-web/src/app/(dashboard)/dashboard/page.tsx", "w") as f:
    f.write(content)


import re

with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "r") as f:
    content = f.read()

# 1. Update the Header background
header_old = 'className="bg-primary pt-10 pb-16 px-6 md:px-12 md:rounded-b-[60px] rounded-b-[40px] shadow-lg flex items-start justify-between"'
header_new = 'className={`${isInspectorOrWorker ? "bg-gradient-to-br from-teal-800 to-teal-600" : "bg-primary"} pt-10 pb-16 px-6 md:px-12 md:rounded-b-[60px] rounded-b-[40px] shadow-lg flex items-start justify-between`}'
content = content.replace(header_old, header_new)

# 2. Update Inspector Actions
actions_old = """        {/* Inspector Actions — simplified workflow */}
        {user?.role === "INSPECTOR" && (
          <>
            {/* OPEN: Start Work + Reject */}
            {complaint.status === "OPEN" && (
              <div className="bg-card rounded-[2rem] p-6 shadow-sm border border-border mb-6">
                <div className="flex items-center gap-3 mb-6 pb-4 border-b border-border/50">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                    <MoreVertical className="w-5 h-5 text-primary" />
                  </div>
                  <h3 className="text-lg font-black text-foreground">Complaint Actions</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    disabled={updating}
                    onClick={handleStartWork}
                    className="flex items-center justify-center gap-2 bg-primary hover:bg-primary/90 text-primary-foreground rounded-2xl py-4 text-sm font-bold shadow-md shadow-primary/20 disabled:opacity-50 transition-all hover:-translate-y-0.5"
                  >
                    <Play className="w-5 h-5" /> Start Work
                  </button>
                  <button
                    disabled={updating}
                    onClick={() => setShowRejectModal(true)}
                    className="flex items-center justify-center gap-2 bg-destructive hover:bg-destructive/90 text-destructive-foreground rounded-2xl py-4 text-sm font-bold shadow-md shadow-destructive/20 disabled:opacity-50 transition-all hover:-translate-y-0.5"
                  >
                    <X className="w-5 h-5" /> Reject
                  </button>
                </div>
              </div>
            )}

            {/* IN_PROGRESS: Resolve */}
            {complaint.status === "IN_PROGRESS" && (
              <div className="bg-card rounded-[2rem] p-6 shadow-sm border border-border mb-6">
                <div className="flex items-center gap-3 mb-6 pb-4 border-b border-border/50">
                  <div className="w-10 h-10 rounded-xl bg-success/10 flex items-center justify-center">
                    <CheckCircle2 className="w-5 h-5 text-success" />
                  </div>
                  <h3 className="text-lg font-black text-foreground">Complaint Actions</h3>
                </div>
                <button
                  disabled={updating}
                  onClick={() => setShowResolveModal(true)}
                  className="w-full flex items-center justify-center gap-2 bg-success hover:bg-success/90 text-success-foreground rounded-2xl py-4 text-sm font-bold shadow-md shadow-success/20 disabled:opacity-50 transition-all hover:-translate-y-0.5"
                >
                  <Check className="w-5 h-5" /> Resolve Complaint
                </button>
              </div>
            )}
          </>
        )}"""

actions_new = """        {/* Inspector Actions — simplified workflow */}
        {user?.role === "INSPECTOR" && (
          <>
            {/* OPEN: Start Work + Reject */}
            {complaint.status === "OPEN" && (
              <div className="bg-white rounded-[2rem] p-6 shadow-sm border border-slate-200 mb-6">
                <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
                  <div className="w-10 h-10 rounded-xl bg-teal-50 flex items-center justify-center">
                    <MoreVertical className="w-5 h-5 text-teal-600" />
                  </div>
                  <h3 className="text-lg font-black text-slate-800">Complaint Actions</h3>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    disabled={updating}
                    onClick={handleStartWork}
                    className="flex items-center justify-center gap-2 bg-teal-600 hover:bg-teal-700 text-white rounded-2xl py-4 text-sm font-bold shadow-md shadow-teal-600/20 disabled:opacity-50 transition-all hover:-translate-y-0.5"
                  >
                    <Play className="w-5 h-5" /> Start Work
                  </button>
                  <button
                    disabled={updating}
                    onClick={() => setShowRejectModal(true)}
                    className="flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white rounded-2xl py-4 text-sm font-bold shadow-md shadow-red-500/20 disabled:opacity-50 transition-all hover:-translate-y-0.5"
                  >
                    <X className="w-5 h-5" /> Reject
                  </button>
                </div>
              </div>
            )}

            {/* IN_PROGRESS: Resolve */}
            {complaint.status === "IN_PROGRESS" && (
              <div className="bg-white rounded-[2rem] p-6 shadow-sm border border-slate-200 mb-6">
                <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-100">
                  <div className="w-10 h-10 rounded-xl bg-teal-50 flex items-center justify-center">
                    <CheckCircle2 className="w-5 h-5 text-teal-600" />
                  </div>
                  <h3 className="text-lg font-black text-slate-800">Complaint Actions</h3>
                </div>
                <button
                  disabled={updating}
                  onClick={() => setShowResolveModal(true)}
                  className="w-full flex items-center justify-center gap-2 bg-teal-600 hover:bg-teal-700 text-white rounded-2xl py-4 text-sm font-bold shadow-md shadow-teal-600/20 disabled:opacity-50 transition-all hover:-translate-y-0.5"
                >
                  <Check className="w-5 h-5" /> Resolve Complaint
                </button>
              </div>
            )}
          </>
        )}"""

content = content.replace(actions_old, actions_new)

# 3. Update Modals (Resolve Confirmation) if it's the inspector resolving
resolve_modal_old = 'className="flex-1 bg-success hover:bg-success/90 text-success-foreground font-bold py-3.5 rounded-2xl shadow-md shadow-success/20 disabled:opacity-50 transition-colors"'
resolve_modal_new = 'className="flex-1 bg-teal-600 hover:bg-teal-700 text-white font-bold py-3.5 rounded-2xl shadow-md shadow-teal-600/20 disabled:opacity-50 transition-colors"'
content = content.replace(resolve_modal_old, resolve_modal_new)

reject_modal_old = 'className="flex-1 bg-destructive hover:bg-destructive/90 text-destructive-foreground font-bold py-3.5 rounded-2xl shadow-md shadow-destructive/20 disabled:opacity-50 transition-colors"'
reject_modal_new = 'className="flex-1 bg-red-500 hover:bg-red-600 text-white font-bold py-3.5 rounded-2xl shadow-md shadow-red-500/20 disabled:opacity-50 transition-colors"'
content = content.replace(reject_modal_old, reject_modal_new)

with open("civifix-web/src/app/(dashboard)/complaints/[id]/page.tsx", "w") as f:
    f.write(content)


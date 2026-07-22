"use client";

import React, { useState, useEffect } from "react";
import { useAuth } from "@/context/auth-context";
import { User, Phone, Save, Loader2, CheckCircle2 } from "lucide-react";
import authService from "@/services/auth";

export default function SettingsPage() {
  const { user, setUser } = useAuth();
  
  const [formData, setFormData] = useState({
    name: "",
    mobile_number: "",
  });
  
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || user.full_name || "",
        mobile_number: user.mobile_number || "",
      });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMsg("");
    setErrorMsg("");

    try {
      const updatedUser = await authService.updateProfile(formData);
      setUser({ ...user, ...updatedUser });
      setSuccessMsg("Profile updated successfully!");
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 bg-background min-h-screen pb-20 md:pb-8">
      {/* Header */}
      <div className="bg-primary pt-12 pb-16 px-6 md:px-12 md:rounded-b-[60px] rounded-b-[40px] shadow-lg flex items-center justify-between sticky top-0 z-20 md:static">
        <div className="max-w-3xl mx-auto w-full flex items-center justify-between">
           <div>
             <h1 className="text-3xl font-black text-white tracking-tight">Settings</h1>
             <p className="text-white/80 font-semibold mt-2">Manage your personal information</p>
           </div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto w-full -mt-8 relative z-10 px-4 sm:px-6 lg:px-8">
        <div className="bg-card rounded-[2rem] p-6 sm:p-8 shadow-sm border border-border">
          
          {successMsg && (
            <div className="mb-6 p-4 bg-success/10 border border-success/30 rounded-2xl flex items-center gap-3 text-success">
              <CheckCircle2 className="w-5 h-5" />
              <p className="font-semibold text-sm">{successMsg}</p>
            </div>
          )}

          {errorMsg && (
            <div className="mb-6 p-4 bg-destructive/10 border border-destructive/30 rounded-2xl flex items-center gap-3 text-destructive">
              <p className="font-semibold text-sm">{errorMsg}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-foreground mb-2">Full Name</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <User className="w-5 h-5 text-muted-foreground" />
                </div>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-4 bg-background border border-border rounded-2xl text-foreground font-semibold focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all placeholder:font-medium placeholder:text-muted-foreground"
                  placeholder="Enter your full name"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-foreground mb-2">Mobile Number</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Phone className="w-5 h-5 text-muted-foreground" />
                </div>
                <input
                  type="tel"
                  name="mobile_number"
                  value={formData.mobile_number}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-4 bg-background border border-border rounded-2xl text-foreground font-semibold focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all placeholder:font-medium placeholder:text-muted-foreground"
                  placeholder="Enter your mobile number"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 bg-primary hover:bg-primary/90 text-primary-foreground py-4 px-6 rounded-2xl font-bold transition-all disabled:opacity-50 hover:shadow-md hover:shadow-primary/20"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  Save Changes
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

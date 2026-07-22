"use client";

import React, { useState, useEffect } from "react";
import { notificationsApi } from "@/services/api";
import { Bell, Check, Trash2, CheckCircle2 } from "lucide-react";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchNotifications = async () => {
    try {
      const res: any = await notificationsApi.getNotifications(1, 50);
      setNotifications(res.data?.notifications || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const handleMarkAsRead = async (id: string) => {
    try {
      await notificationsApi.markAsRead(id);
      setNotifications(notifications.map(n => n._id === id ? { ...n, is_read: true } : n));
    } catch (e) {
      console.error(e);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationsApi.markAllAsRead();
      setNotifications(notifications.map(n => ({ ...n, is_read: true })));
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 bg-background min-h-screen pb-20 md:pb-8">
      {/* Header */}
      <div className="bg-primary pt-12 pb-16 px-6 md:px-12 md:rounded-b-[60px] rounded-b-[40px] shadow-lg flex items-center justify-between sticky top-0 z-20 md:static">
        <div className="max-w-3xl mx-auto w-full flex items-center justify-between">
           <div>
             <h1 className="text-3xl font-black text-white tracking-tight">Notifications</h1>
             <p className="text-white/80 font-semibold mt-2">Stay updated on your civic issues</p>
           </div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto w-full -mt-8 relative z-10 px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-4 px-2">
          <p className="text-sm font-bold text-muted-foreground">{notifications.filter(n => !n.is_read).length} unread</p>
          <button onClick={handleMarkAllAsRead} className="text-sm font-bold text-primary hover:underline flex items-center gap-1">
            <CheckCircle2 className="w-4 h-4" /> Mark all read
          </button>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 col-span-full">
            <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm font-bold text-muted-foreground mt-4">Loading notifications...</p>
          </div>
        ) : notifications.length === 0 ? (
          <div className="bg-card rounded-[2rem] p-8 text-center shadow-sm border border-border">
            <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
              <Bell className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-black text-foreground mb-2">No notifications yet</h3>
            <p className="text-sm font-semibold text-muted-foreground">You will receive alerts here when your complaints are updated.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {notifications.map((notif: any) => (
              <div 
                key={notif._id} 
                className={`bg-card rounded-[2rem] p-6 shadow-sm hover:shadow-md transition-all duration-300 border ${notif.is_read ? 'border-border' : 'border-primary/50'}`}
              >
                <div className="flex gap-4">
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 ${notif.is_read ? 'bg-muted' : 'bg-primary/10'}`}>
                    <Bell className={`w-6 h-6 ${notif.is_read ? 'text-muted-foreground' : 'text-primary'}`} />
                  </div>
                  <div className="flex-1">
                    <h4 className="text-base font-black text-foreground">{notif.title}</h4>
                    <p className="text-sm font-medium text-muted-foreground mt-1">{notif.message}</p>
                    <p className="text-xs font-bold text-muted-foreground/70 mt-3">{new Date(notif.created_at).toLocaleString()}</p>
                  </div>
                  {!notif.is_read && (
                    <button 
                      onClick={() => handleMarkAsRead(notif._id)}
                      className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center hover:bg-primary/20 transition-colors shrink-0"
                    >
                      <Check className="w-4 h-4 text-primary" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

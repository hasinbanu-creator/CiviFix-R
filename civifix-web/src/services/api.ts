import api, { unwrapResponse } from "@/lib/api";

export const complaintsApi = {
  updateStatus: async (id: string, status: string) => {
    const res = await api.put(`/complaints/${id}/status`, { status });
    return unwrapResponse(res);
  },
  
  addNote: async (id: string, payload: { text: string }) => {
    const res = await api.put(`/complaints/${id}/note`, payload);
    return unwrapResponse(res);
  },

  resolveComplaintWithImages: async (id: string, formData: FormData) => {
    const res = await api.put(`/inspector/complaints/${id}/resolve`, formData);
    return unwrapResponse(res);
  }
};

export const notificationsApi = {
  getNotifications: async (page = 1, limit = 20) => {
    const res = await api.get(`/notifications`, { params: { page, limit } });
    return unwrapResponse(res);
  },
  
  markAsRead: async (id: string) => {
    const res = await api.put(`/notifications/${id}/read`);
    return unwrapResponse(res);
  },

  markAllAsRead: async () => {
    const res = await api.put(`/notifications/read-all`);
    return unwrapResponse(res);
  }
};

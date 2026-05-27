import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const fetchCurrentUser = async () => {
  const res = await api.post("/auth/me");
  return res.data;
};

export const fetchCampaigns = async () => {
  const res = await api.get("/campaigns");
  return res.data;
};

export const createCampaign = async (name: string, description: string) => {
  const res = await api.post("/campaigns", { name, description });
  return res.data;
};

export const joinCampaign = async (id: number, inviteCode: string) => {
  const res = await api.post(`/campaigns/${id}/join`, { invite_code: inviteCode });
  return res.data;
};

export const fetchCampaign = async (id: number) => {
  const res = await api.get(`/campaigns/${id}`);
  return res.data;
};

export const fetchMembers = async (id: number) => {
  const res = await api.get(`/campaigns/${id}/members`);
  return res.data;
};

export const removeMember = async (campaignId: number, userId: number) => {
  const res = await api.delete(`/campaigns/${campaignId}/members/${userId}`);
  return res.data;
};

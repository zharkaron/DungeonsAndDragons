import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { joinCampaign } from "../services/api";

export default function JoinCampaignPage() {
  const [inviteCode, setInviteCode] = useState("");
  const [campaignId, setCampaignId] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!campaignId.trim() || !inviteCode.trim()) {
      setError("Both campaign ID and invite code are required");
      return;
    }

    try {
      await joinCampaign(parseInt(campaignId), inviteCode);
      navigate("/my-campaigns");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to join campaign");
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center mb-4">
                Join Campaign
              </h2>
              {error && (
                <div className="alert alert-danger">{error}</div>
              )}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="campaignId" className="form-label">
                    Campaign ID
                  </label>
                  <input
                    type="number"
                    className="form-control"
                    id="campaignId"
                    value={campaignId}
                    onChange={(e) => setCampaignId(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="inviteCode" className="form-label">
                    Invite Code
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="inviteCode"
                    value={inviteCode}
                    onChange={(e) => setInviteCode(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100 mb-3">
                  Join Campaign
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

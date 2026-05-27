import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { fetchCampaigns } from "../services/api";

interface Campaign {
  id: number;
  name: string;
  description: string | null;
  inviteCode: string;
}

export default function MyCampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCampaigns()
      .then((data) => {
        setCampaigns(data as Campaign[]);
        setLoading(false);
      })
      .catch((err: any) => {
        setError(err.response?.data?.detail || "Failed to fetch campaigns");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="d-flex justify-content-center">
          <div className="spinner-border text-primary"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>My Campaigns</h2>
        <Link to="/campaigns/create" className="btn btn-primary">
          Create Campaign
        </Link>
      </div>
      {error && (
        <div className="alert alert-danger">{error}</div>
      )}
      {campaigns.length === 0 ? (
        <div className="alert alert-info">
          You haven't joined any campaigns yet.
        </div>
      ) : (
        <div className="row">
          {campaigns.map((campaign) => (
            <div key={campaign.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{campaign.name}</h5>
                  {campaign.description && (
                    <p className="card-text">{campaign.description}</p>
                  )}
                  <div className="mb-2">
                    <span className="badge bg-secondary">
                      Invite Code: {campaign.inviteCode}
                    </span>
                  </div>
                </div>
                <div className="card-footer bg-transparent">
                  <Link
                    to={`/campaigns/${campaign.id}/detail`}
                    className="btn btn-outline-primary w-100"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchCampaign, fetchMembers } from "../services/api";

interface Member {
  id: number;
  userId: number;
  username: string;
  role: string;
  joinedAt: string;
}

interface Campaign {
  id: number;
  name: string;
  description: string | null;
  dmId: number;
  inviteCode: string;
  createdAt: string;
}

export default function CampaignDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;

    Promise.all([
      fetchCampaign(parseInt(id)).catch((err) => {
        setError(
          err.response?.data?.detail || "Failed to fetch campaign details",
        );
        return null;
      }),
      fetchMembers(parseInt(id)).catch(() => []),
    ]).then(([data, membersData]) => {
      if (data) setCampaign(data);
      setMembers(membersData as Member[]);
      setLoading(false);
    });
  }, [id]);

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
      <Link to="/my-campaigns" className="btn btn-outline-secondary mb-3">
        ← Back to My Campaigns
      </Link>
      {error && (
        <div className="alert alert-danger">{error}</div>
      )}
      {campaign ? (
        <>
          <h2 className="mb-3">{campaign.name}</h2>
          {campaign.description && (
            <p className="lead">{campaign.description}</p>
          )}
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Campaign Info</h5>
              <p>
                <strong>DM ID:</strong> {campaign.dmId}
              </p>
              <p>
                <strong>Invite Code:</strong> {campaign.inviteCode}
              </p>
              <p>
                <strong>Created:</strong>{" "}
                {new Date(campaign.createdAt).toLocaleDateString()}
              </p>
            </div>
          </div>
        </>
      ) : (
        <div className="alert alert-danger">Campaign not found</div>
      )}
      <h3 className="mt-4">Members</h3>
      {members.length === 0 ? (
        <div className="alert alert-info">No members yet.</div>
      ) : (
        <div className="row">
          {members.map((member) => (
            <div key={member.id} className="col-md-6 col-lg-4 mb-3">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{member.username}</h5>
                  <span className={`badge bg-${member.role === "dm" ? "danger" : "primary"}`}>
                    {member.role}
                  </span>
                  <p className="card-text">
                    Joined:{" "}
                    {new Date(member.joinedAt).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCampaign } from "../services/api";

export default function CreateCampaignPage() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!name.trim()) {
      setError("Campaign name is required");
      return;
    }

    try {
      await createCampaign(name, description);
      navigate("/my-campaigns");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to create campaign");
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-4">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center mb-4">
                Create Campaign
              </h2>
              {error && (
                <div className="alert alert-danger">{error}</div>
              )}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="name" className="form-label">
                    Campaign Name
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    maxLength={100}
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="description" className="form-label">
                    Description
                  </label>
                  <textarea
                    className="form-control"
                    id="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    maxLength={1000}
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100 mb-3">
                  Create Campaign
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

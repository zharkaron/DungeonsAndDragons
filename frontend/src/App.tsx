import { useContext } from "react";
import {
  Routes,
  Route,
  Link,
  Navigate,
  Outlet,
} from "react-router-dom";
import { AuthContext } from "./context/AuthContext";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import MyCampaignsPage from "./pages/MyCampaignsPage";
import CreateCampaignPage from "./pages/CreateCampaignPage";
import CampaignDetailPage from "./pages/CampaignDetailPage";
import JoinCampaignPage from "./pages/JoinCampaignPage";

function ProtectedRoute() {
  const auth = useContext(AuthContext);
  if (!auth?.isAuthenticated) {
    return <Navigate to="/login" />;
  }
  return <Outlet />;
}

function Layout() {
  const auth = useContext(AuthContext);
  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div className="container">
          <Link className="navbar-brand" to="/login">
            🐉 D&D Campaign Manager
          </Link>
          {auth?.isAuthenticated && (
            <div className="d-flex align-items-center">
              <Link to="/my-campaigns" className="nav-link">
                My Campaigns
              </Link>
              <Link to="/campaigns/join" className="nav-link">
                Join Campaign
              </Link>
              <button
                className="btn btn-outline-light ms-2"
                onClick={auth.logout}
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/my-campaigns" element={<MyCampaignsPage />} />
          <Route path="/campaigns/create" element={<CreateCampaignPage />} />
          <Route
            path="/campaigns/:id/detail"
            element={<CampaignDetailPage />}
          />
          <Route path="/campaigns/join" element={<JoinCampaignPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </>
  );
}

function App() {
  return <Layout />;
}

export default App;

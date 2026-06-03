import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import SearchTrains from "./pages/SearchTrains";

function App() {
  return (
    <div>
      <header className="header">
        <Link to="/" className="brand">
          <span className="logo">RG</span>
          <div>
            <h1>RailGuard</h1>
            <p>AI Railway Delay Prediction</p>
          </div>
        </Link>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/search" className="nav-btn">Search Trains</Link>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<SearchTrains />} />
      </Routes>

      <footer className="footer">
        <strong>RailGuard</strong>
        <span>AI-powered railway delay intelligence platform</span>
        <span>Emergency Railway Helpline: 139</span>
      </footer>
    </div>
  );
}

export default App;

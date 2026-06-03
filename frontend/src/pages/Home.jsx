import { Link } from "react-router-dom";
import { ShieldCheck, Clock, Route } from "lucide-react";

function Home() {
  return (
    <main>
      <section className="hero">
        <div className="hero-text">
          <span className="tag">Indian Railway Delay Intelligence</span>
          <h2>Check trains and predict delay risk before you travel.</h2>
          <p>
            RailGuard uses machine learning and railway route data to show expected delay,
            delay probability, and a simple delay score out of 10.
          </p>
          <div className="actions">
            <Link to="/search" className="primary">Search Trains</Link>
          </div>
          <div className="mini-stats">
            <div><strong>1-10</strong><span>Delay Score</span></div>
            <div><strong>AI</strong><span>Prediction</span></div>
            <div><strong>Route</strong><span>Analytics</span></div>
          </div>
        </div>

        <div className="hero-image-card">
          <img src="/images/train.jpg" alt="Indian railway train" />
          <div className="alert-card">
            <strong>Live Route Risk</strong>
            <span>Weather, congestion and train type based scoring</span>
          </div>
        </div>
      </section>

      <section className="features">
        <div className="feature-card"><Clock /><h3>Expected Delay</h3><p>View predicted delay in minutes for each train.</p></div>
        <div className="feature-card"><ShieldCheck /><h3>Delay Score</h3><p>Simple 1/10 to 10/10 risk score for quick decisions.</p></div>
        <div className="feature-card"><Route /><h3>Route Search</h3><p>Find trains between source and destination station codes.</p></div>
      </section>
    </main>
  );
}
export default Home;

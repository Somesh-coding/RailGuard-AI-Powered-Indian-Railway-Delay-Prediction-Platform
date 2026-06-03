import { useState } from "react";
import API from "../api";

function SearchTrains() {
  const [form, setForm] = useState({
    source: "",
    destination: "",
    weather: "Rainy",
    dayOfWeek: "Tuesday",
    timeOfDay: "Afternoon",
    routeCongestion: "Medium"
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const searchTrains = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await API.post("/trains/search", form);
      setResult(res.data);
    } catch (err) {
      setError("Backend or ML service is not running");
    }
    setLoading(false);
  };

  return (
    <main className="search-page">
      <section className="search-panel">
        <div>
          <span className="tag">Train Search</span>
          <h2>Find trains and delay score</h2>
          <p>Use station codes like NGP, PUNE, BD, NK.</p>
        </div>

        <form className="search-box" onSubmit={searchTrains}>
          <input required placeholder="Source e.g. NGP" value={form.source} onChange={(e)=>setForm({...form, source:e.target.value.toUpperCase()})}/>
          <input required placeholder="Destination e.g. PUNE" value={form.destination} onChange={(e)=>setForm({...form, destination:e.target.value.toUpperCase()})}/>
          <select value={form.weather} onChange={(e)=>setForm({...form, weather:e.target.value})}><option>Clear</option><option>Rainy</option><option>Foggy</option><option>Stormy</option></select>
          <select value={form.dayOfWeek} onChange={(e)=>setForm({...form, dayOfWeek:e.target.value})}><option>Monday</option><option>Tuesday</option><option>Wednesday</option><option>Thursday</option><option>Friday</option><option>Saturday</option><option>Sunday</option></select>
          <select value={form.timeOfDay} onChange={(e)=>setForm({...form, timeOfDay:e.target.value})}><option>Morning</option><option>Afternoon</option><option>Evening</option><option>Night</option></select>
          <select value={form.routeCongestion} onChange={(e)=>setForm({...form, routeCongestion:e.target.value})}><option>Low</option><option>Medium</option><option>High</option></select>
          <button disabled={loading}>{loading ? "Searching..." : "Search Trains"}</button>
        </form>
      </section>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="results-section">
          <h2>{result.totalTrains} trains found from {result.source} to {result.destination}</h2>
          <div className="train-list">
            {result.trains?.map((train, index) => (
              <div className="train-card" key={index}>
                <div className="train-info">
                  <h3>{train.trainName}</h3>
                  <p>Train No: {train.trainNumber}</p>
                  <p>{train.sourceStation} → {train.destinationStation}</p>
                  <p>Departure: {train.departureTime} | Arrival: {train.arrivalTime}</p>
                  <p>Distance: {train.distance} km | Type: {train.trainType}</p>
                </div>
                <div className="score-box">
                  <span>{train.delayScore}/10</span>
                  <p>Delay Score</p>
                  <strong>{train.delayProbability}%</strong>
                  <small>{train.expectedDelay} min expected</small>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}

export default SearchTrains;

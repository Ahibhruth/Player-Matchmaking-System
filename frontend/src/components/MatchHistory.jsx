import React, { useEffect, useState } from "react";

const MatchHistory = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/match_history")
      .then((res) => res.json())
      .then((data) => setHistory(data.history || []))
      .catch((err) => console.error("Failed to fetch match history", err));
  }, []);

  return (
    <div style={{ maxWidth: "100%", overflowX: "auto", marginTop: "20px" }}>
      <h2>📜 Match History</h2>
      {history.length === 0 ? (
        <p>No match history yet.</p>
      ) : (
        <table style={{ width: "100%", minWidth: "400px", borderCollapse: "collapse", color: "#fff" }}>
          <thead>
            <tr>
              <th>Winner</th>
              <th>Loser</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {history.map((match, index) => (
              <tr key={index}>
                <td>{match.winner}</td>
                <td>{match.loser}</td>
                <td>{new Date(match.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default MatchHistory;

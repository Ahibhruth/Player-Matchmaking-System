import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const PlayerProfile = () => {
  const { name } = useParams();
  const [player, setPlayer] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/api/player_stats/${name}`)
      .then(res => res.json())
      .then(data => setPlayer(data))
      .catch(console.error);
  }, [name]);

  if (!player) return <p>Loading...</p>;
  if (player.error) return <p>{player.error}</p>;

  return (
    <div style={{ color: "#fff", padding: "1rem" }}>
      <h1>{player.name}'s Profile</h1>
      <p><strong>Rank:</strong> {player.rank}</p>
      <p><strong>Playstyle:</strong> {player.playstyle}</p>
      <p><strong>Wins:</strong> {player.wins}</p>
      <p><strong>Losses:</strong> {player.losses}</p>
      <p><strong>Win Rate:</strong> {player.win_rate}%</p>

      <h2>Match History</h2>
      <table style={{ width: "100%", border: "1px solid white" }}>
        <thead>
          <tr>
            <th>Winner</th>
            <th>Loser</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {player.match_history.map((match, i) => (
            <tr key={i}>
              <td>{match.winner}</td>
              <td>{match.loser}</td>
              <td>{new Date(match.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PlayerProfile;

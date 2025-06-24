import React, { useState, useEffect } from "react";
import "./MatchmakingForm.css";

const PlayerProfileModal = ({ player, onClose, onRefresh, isLoading }) => {
  if (!player) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{player.name}'s Profile</h2>
          <div className="modal-actions">
            <button 
              onClick={(e) => { e.stopPropagation(); onRefresh(); }} 
              className="refresh-button"
              disabled={isLoading}
            >
              {isLoading ? 'Refreshing...' : '⟳ Refresh'}
            </button>
            <button className="close-button" onClick={onClose}>×</button>
          </div>
        </div>
        <div className="player-details">
          <p><strong>Rank:</strong> {player.rank}</p>
          <p><strong>Playstyle:</strong> {player.playstyle}</p>
          <p><strong>Wins:</strong> {player.wins || 0}</p>
          <p><strong>Losses:</strong> {player.losses || 0}</p>
          <p><strong>Total Matches:</strong> {player.total_matches || 0}</p>
          <p><strong>Win Rate:</strong> {player.win_rate || 0}%</p>
          
          {player.match_history && player.match_history.length > 0 && (
            <div className="match-history">
              <h3>Match History</h3>
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Winner</th>
                    <th>Loser</th>
                  </tr>
                </thead>
                <tbody>
                  {player.match_history.map((match, index) => (
                    <tr key={index} className={match.winner === player.name ? 'won' : 'lost'}>
                      <td>{new Date(match.timestamp).toLocaleString()}</td>
                      <td>{match.winner}</td>
                      <td>{match.loser}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};


const MatchmakingForm = () => {
  const [players, setPlayers] = useState([]);
  const [form, setForm] = useState({ id: "", name: "", rank: "", playstyle: "aggressive", available: "true", avoid: "" });
  const [matchResult, setMatchResult] = useState("");
  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [lastMatchedPlayers, setLastMatchedPlayers] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [isLoadingProfile, setIsLoadingProfile] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/players")
      .then(res => res.json())
      .then(data => setPlayers(data.players));
  }, []);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const registerPlayer = () => {
    const avoidList = form.avoid.split(",").map(s => s.trim()).filter(Boolean);
    fetch("http://127.0.0.1:5000/api/register_player", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: parseInt(form.id),
        name: form.name,
        rank: parseInt(form.rank),
        playstyle: form.playstyle,
        available: form.available === "true",
        avoid: avoidList
      })
    })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        if (data.message === "Player registered successfully!") {
          setForm({ id: "", name: "", rank: "", playstyle: "aggressive", available: "true", avoid: "" });
          fetch("http://127.0.0.1:5000/api/players")
            .then(res => res.json())
            .then(data => setPlayers(data.players));
        }
      });
  };

  const fetchPlayerProfile = async (playerName) => {
    if (!playerName) return;
    
    setIsLoadingProfile(true);
    try {
      const response = await fetch(`http://localhost:5000/api/player_stats/${encodeURIComponent(playerName)}`);
      const data = await response.json();
      
      if (response.ok) {
        setSelectedProfile(data);
      } else {
        console.error('Error fetching profile:', data.error);
        alert(data.error || 'Failed to load player profile');
      }
    } catch (err) {
      console.error('Error fetching player profile:', err);
      alert('Error loading player profile');
    } finally {
      setIsLoadingProfile(false);
    }
  };
  
  const viewPlayerProfile = (playerName) => {
    setSelectedProfile({ name: playerName }); // Set basic info immediately
    fetchPlayerProfile(playerName);
  };
  
  const handleProfileRefresh = () => {
    if (selectedProfile?.name) {
      fetchPlayerProfile(selectedProfile.name);
    }
  };

  const findMatch = () => {
    if (!selectedPlayer) return alert("Select a player first");
    setLastMatchedPlayers([]);
    fetch(`http://127.0.0.1:5000/api/match/${selectedPlayer}`)
      .then(res => res.json())
      .then(data => {
        if (data.matches) {
          const matchedPlayer = data.matches[0];
          setLastMatchedPlayers([matchedPlayer]);
          setMatchResult(
            <>
              Matched Player: <strong>{matchedPlayer}</strong> —{" "}
              <button 
                onClick={() => viewPlayerProfile(matchedPlayer)}
                style={{ 
                  background: 'none',
                  border: 'none',
                  color: '#88f',
                  textDecoration: 'underline',
                  cursor: 'pointer',
                  padding: 0,
                  font: 'inherit'
                }}
              >
                View Profile
              </button>
            </>
          );
        } else {
          setMatchResult(data.error);
        }
      })
      .catch(err => {
        console.error('Error finding match:', err);
        setMatchResult('Error finding match');
      });
  };

  const matchAgain = () => {
    if (!selectedPlayer || lastMatchedPlayers.length === 0) {
      alert("Find a match first");
      return;
    }
    const excludeParams = lastMatchedPlayers.map(p => `exclude=${encodeURIComponent(p)}`).join("&");
    fetch(`http://127.0.0.1:5000/api/match/${selectedPlayer}?${excludeParams}`)
      .then(res => res.json())
      .then(data => {
        if (data.matches) {
          const newMatchedPlayer = data.matches[0];
          setLastMatchedPlayers(prev => [...prev, newMatchedPlayer]);
          setMatchResult(
            <>
              Matched Player: <strong>{newMatchedPlayer}</strong> —{" "}
              <button 
                onClick={() => viewPlayerProfile(newMatchedPlayer)}
                style={{ 
                  background: 'none',
                  border: 'none',
                  color: '#88f',
                  textDecoration: 'underline',
                  cursor: 'pointer',
                  padding: 0,
                  font: 'inherit'
                }}
              >
                View Profile
              </button>
            </>
          );
        } else {
          setMatchResult(data.error);
        }
      })
      .catch(err => {
        console.error('Error finding another match:', err);
        setMatchResult('Error finding another match');
      });
  };

  return (
    <div className="container">
      {selectedProfile && (
        <PlayerProfileModal 
          player={selectedProfile} 
          onClose={() => setSelectedProfile(null)}
          onRefresh={handleProfileRefresh}
          isLoading={isLoadingProfile}
        />
      )}

      <section className="section">
        <h2 className="section-title">REGISTER PLAYER</h2>
        <input className="input" name="id" value={form.id} placeholder="Player ID" onChange={handleChange} />
        <input className="input" name="name" value={form.name} placeholder="Player Name" onChange={handleChange} />
        <input className="input" name="rank" type="number" value={form.rank} placeholder="Rank" onChange={handleChange} />
        <select className="select" name="playstyle" value={form.playstyle} onChange={handleChange}>
          <option value="aggressive">Aggressive</option>
          <option value="defensive">Defensive</option>
          <option value="balanced">Balanced</option>
        </select>
        <select className="select" name="available" value={form.available} onChange={handleChange}>
          <option value="true">Available</option>
          <option value="false">Not Available</option>
        </select>
        <input className="input" name="avoid" value={form.avoid} placeholder="Avoid playstyles (comma separated)" onChange={handleChange} />
        <button className="button" onClick={registerPlayer}>REGISTER</button>
      </section>

      <section className="section">
        <h2 className="section-title">FIND MATCH</h2>
        <select className="select" value={selectedPlayer} onChange={e => setSelectedPlayer(e.target.value)}>
          <option value="">Select Player</option>
          {players.map(name => (
            <option key={name} value={name}>{name}</option>
          ))}
        </select>
        <button className="button" onClick={findMatch}>FIND MATCH</button>
        <button className="button" onClick={matchAgain}>MATCH AGAIN</button>
        <div className="result-box">{matchResult}</div>
      </section>
    </div>
  );
};

export default MatchmakingForm;

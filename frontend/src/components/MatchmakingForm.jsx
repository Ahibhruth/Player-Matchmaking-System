import React, { useState, useEffect } from "react";
import "./MatchmakingForm.css";

const MatchmakingForm = () => {
  const [players, setPlayers] = useState([]);
  const [form, setForm] = useState({ id: "", name: "", rank: "", playstyle: "aggressive", available: "true", avoid: "" });
  const [matchResult, setMatchResult] = useState("");
  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [lastMatchedPlayers, setLastMatchedPlayers] = useState([]);

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

  const findMatch = () => {
    if (!selectedPlayer) return alert("Select a player first");
    setLastMatchedPlayers([]);
    fetch(`http://127.0.0.1:5000/api/match/${selectedPlayer}`)
      .then(res => res.json())
      .then(data => {
        if (data.matches) {
          setLastMatchedPlayers([data.matches[0]]);
          setMatchResult(
            <>
              Matched Player: <strong>{data.matches[0]}</strong> —{" "}
              <a href={`/player/${data.matches[0]}`} style={{ color: "#88f" }}>View Profile</a>
            </>
          );
        } else setMatchResult(data.error);
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
          setLastMatchedPlayers(prev => [...prev, data.matches[0]]);
          setMatchResult(
            <>
              Matched Player: <strong>{data.matches[0]}</strong> —{" "}
              <a href={`/player/${data.matches[0]}`} style={{ color: "#88f" }}>View Profile</a>
            </>
          );
        } else setMatchResult(data.error);
      });
  };

  return (
    <div className="container">

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

function startGame() {
  document.getElementById("welcome-screen").classList.add("hidden");
  document.getElementById("game-ui").classList.remove("hidden");
}

function registerPlayer() {
  const name = document.getElementById("regName").value;
  const rank = parseInt(document.getElementById("regRank").value);
  const playstyle = document.getElementById("regStyle").value;

  fetch('/api/register_player', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, rank, playstyle })
  })
  .then(res => res.json())
  .then(data => document.getElementById("result").innerText = data.message)
  .catch(err => console.error(err));
}

function findMatch() {
  const name = document.getElementById("matchName").value;

  fetch(`/match/${name}`)
    .then(res => res.json())
    .then(data => {
      if (data.matches) {
        document.getElementById("result").innerText = "Matched with: " + data.matches.join(', ');
      } else {
        document.getElementById("result").innerText = data.error;
      }
    })
    .catch(() => {
      document.getElementById("result").innerText = "Failed to fetch match!";
    });
}

function deletePlayer() {
  const name = document.getElementById("deleteName").value;
  if (!confirm(`Are you sure you want to delete player '${name}'?`)) return;

  fetch(`/api/delete_player/${name}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => document.getElementById("result").innerText = data.message)
    .catch(() => {
      document.getElementById("result").innerText = "Error deleting player.";
    });
}

// Function to start the game and display the game panel
function startGame() {
  document.querySelector(".welcome-screen").style.display = "none";
  document.getElementById("game-panel").style.display = "block";
}

// Function to register a new player
function registerPlayer() {
  let name = document.getElementById("regName").value;
  let rank = document.getElementById("regRank").value;
  let playstyle = document.getElementById("regStyle").value;

  if (name && rank) {
    fetch("http://127.0.0.1:5000/api/register_player", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        rank: parseInt(rank),
        playstyle: playstyle,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        if (data.message === "Player registered successfully!") {
          document.getElementById("regName").value = "";
          document.getElementById("regRank").value = "";
        }
      });
  } else {
    alert("Please fill in all fields!");
  }
}

// Function to find a match for a player
function findMatch() {
  let name = document.getElementById("matchName").value;

  if (name) {
    fetch(`http://127.0.0.1:5000/match/${name}`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.matches) {
          document.getElementById("result").innerHTML =
            "<h3>Matching Players: </h3>" + data.matches.join(", ");
        } else {
          document.getElementById("result").innerHTML =
            "<h3>" + data.error + "</h3>";
        }
      });
  } else {
    alert("Please enter a player name!");
  }
}

// Function to delete a player
function deletePlayer() {
  let name = document.getElementById("deleteName").value;

  if (name) {
    if (confirm(`Are you sure you want to delete ${name}?`)) {
      fetch("http://127.0.0.1:5000/delete_player", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: name }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          if (data.message === "Player deleted successfully!") {
            document.getElementById("deleteName").value = "";
          }
        });
    }
  } else {
    alert("Please enter a player name to delete!");
  }
}

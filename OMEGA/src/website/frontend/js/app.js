document.getElementById('racePredictionForm').addEventListener('submit', function(e) {
  e.preventDefault();

  // Show loader
  document.getElementById('loader').style.display = 'block';

  // Get form values
  const stSpeed = document.getElementById('st_speed').value;
  const compound = document.getElementById('compound').value;
  const airTemp = document.getElementById('air_temp').value;
  const rainfall = document.getElementById('rainfall').value;
  const windDirection = document.getElementById('wind_direction').value;
  const windSpeed = document.getElementById('wind_speed').value;

  // Create data object for API
  const data = {
    st_speed: stSpeed,
    compound: compound,
    air_temperature: airTemp,
    rainfall: rainfall,
    wind_direction: windDirection,
    wind_speed: windSpeed
  };

  // Make actual API call to backend
  fetch('http://127.0.0.1:5000/api/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok: ' + response.statusText);
    }
    return response.json();
  })
  .then(responseData => {
    // Hide loader
    document.getElementById('loader').style.display = 'none';

    // Display results
    displayTeamPerformance(responseData);
  })
  .catch(error => {
    console.error('Error:', error);
    document.getElementById('loader').style.display = 'none';

    // Add more user-friendly error message
    const resultContent = document.getElementById('resultContent');
    resultContent.innerHTML = `
      <div class="alert alert-danger">
        <h4>Error Occurred</h4>
        <p>There was a problem processing your request: ${error.message}</p>
        <p>Please try again or check if the backend server is running.</p>
      </div>
    `;
  });
});

// Display team performance in the UI
function displayTeamPerformance(data) {
  const resultContent = document.getElementById('resultContent');

  // Clear previous results
  resultContent.innerHTML = '';

  // Create race conditions summary
  const conditionsHTML = `
    <div class="race-stats">
      <h4>Car tier list - Race Conditions</h4>
      <div class="row">
        <div class="col-6">
          <p><strong>Track Temp:</strong> ${data.raceConditions.trackTemp}°C</p>
          <p><strong>Air Temp:</strong> ${data.raceConditions.airTemp}°C</p>
          <p><strong>Humidity:</strong> ${data.raceConditions.humidity}%</p>
          ${data.raceConditions.predictedLapTime ? `<p><strong>Base Lap Time:</strong> ${data.raceConditions.predictedLapTime}s</p>` : ''}
        </div>
        <div class="col-6">
          <p><strong>Wind:</strong> ${data.raceConditions.windSpeed} km/h (${data.raceConditions.windDirection}°)</p>
          <p><strong>Rainfall:</strong> ${data.raceConditions.rainfall} mm</p>
          <p><strong>Compound:</strong> ${data.raceConditions.compound}</p>
        </div>
      </div>
    </div>
  `;

  // Create team performance table
  let teamsHTML = `
    <table class="table standings-table">
      <thead>
        <tr>
          <th>Rank</th>
          <th>Team</th>
          <th>Car Performance</th>
          <th>Advantage</th>
        </tr>
      </thead>
      <tbody>
  `;

  data.teams.forEach((team, index) => {
    teamsHTML += `
      <tr class="position-${index < 3 ? (index + 1) : ''}">
        <td>${index + 1}</td>
        <td>
          <img src="${team.logo}" class="team-logo" alt="${team.name}">
          ${team.name}
        </td>
        <td>${team.finalPerformance}%</td>
        <td>${team.advantage}</td>
      </tr>
    `;
  });

  teamsHTML += `
      </tbody>
    </table>
  `;

  // Only show the conditions and team table (removed performance metrics cards)
  resultContent.innerHTML = conditionsHTML + teamsHTML;
}

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

  // Simulate API call
  setTimeout(() => {
    mockApiCall(data)
      .then(response => {
        // Hide loader
        document.getElementById('loader').style.display = 'none';

        // Display results
        displayTeamPerformance(response);
      })
      .catch(error => {
        console.error('Error:', error);
        document.getElementById('loader').style.display = 'none';
        alert('An error occurred while processing your request. Please try again.');
      });
  }, 1000); // Simulated delay
});

// Mock API call function (replace with actual API call)
function mockApiCall(data) {
  return new Promise((resolve) => {
    // Define F1 teams with their base stats
    const teams = [
      {
        id: 1,
        name: "Red Bull Racing",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/red-bull-racing-logo.png.transform/2col/image.png",
        basePerformance: 98.5,
        aerodynamics: 97,
        power: 95,
        chassis: 98,
        reliability: 94,
        tireManagement: 96
      },
      {
        id: 2,
        name: "Ferrari",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/ferrari-logo.png.transform/2col/image.png",
        basePerformance: 97.8,
        aerodynamics: 94,
        power: 98,
        chassis: 93,
        reliability: 88,
        tireManagement: 89
      },
      {
        id: 3,
        name: "Mercedes",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/mercedes-logo.png.transform/2col/image.png",
        basePerformance: 97.5,
        aerodynamics: 92,
        power: 96,
        chassis: 95,
        reliability: 96,
        tireManagement: 93
      },
      {
        id: 4,
        name: "McLaren",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/mclaren-logo.png.transform/2col/image.png",
        basePerformance: 97.2,
        aerodynamics: 93,
        power: 94,
        chassis: 94,
        reliability: 91,
        tireManagement: 94
      },
      {
        id: 5,
        name: "Aston Martin",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/aston-martin-logo.png.transform/2col/image.png",
        basePerformance: 96.8,
        aerodynamics: 91,
        power: 92,
        chassis: 90,
        reliability: 93,
        tireManagement: 90
      },
      {
        id: 6,
        name: "Alpine F1 Team",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/alpine-logo.png.transform/2col/image.png",
        basePerformance: 96.0,
        aerodynamics: 88,
        power: 90,
        chassis: 89,
        reliability: 85,
        tireManagement: 87
      },
      {
        id: 7,
        name: "Williams",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/williams-logo.png.transform/2col/image.png",
        basePerformance: 95.2,
        aerodynamics: 86,
        power: 91,
        chassis: 85,
        reliability: 88,
        tireManagement: 83
      },
      {
        id: 8,
        name: "AlphaTauri",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/alphatauri-logo.png.transform/2col/image.png",
        basePerformance: 95.0,
        aerodynamics: 85,
        power: 95,
        chassis: 83,
        reliability: 89,
        tireManagement: 85
      },
      {
        id: 9,
        name: "Alfa Romeo",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/alfa-romeo-logo.png.transform/2col/image.png",
        basePerformance: 94.5,
        aerodynamics: 82,
        power: 88,
        chassis: 86,
        reliability: 82,
        tireManagement: 84
      },
      {
        id: 10,
        name: "Haas F1 Team",
        logo: "https://www.formula1.com/content/dam/fom-website/teams/2023/haas-f1-team-logo.png.transform/2col/image.png",
        basePerformance: 94.0,
        aerodynamics: 80,
        power: 87,
        chassis: 84,
        reliability: 81,
        tireManagement: 82
      }
    ];

    // Apply modifiers based on conditions
    const modifiedTeams = teams.map(team => {
      let performanceAdjustment = 0;
      let aeroAdjustment = 0;
      let powerAdjustment = 0;
      let chassisAdjustment = 0;
      let tireAdjustment = 0;

      // Tire compound effects
      if (data.compound === "Soft") {
        // Ferrari and McLaren better on softs
        if (team.name === "Ferrari" || team.name === "McLaren") {
          tireAdjustment += 2.5;
          performanceAdjustment += 0.4;
        }
      } else if (data.compound === "Hard") {
        // Red Bull and Mercedes better on hards
        if (team.name === "Red Bull Racing" || team.name === "Mercedes") {
          tireAdjustment += 2.0;
          performanceAdjustment += 0.3;
        }
      } else if (data.compound === "Wet" || data.compound === "Intermediate") {
        // Red Bull better in wet conditions
        if (team.name === "Red Bull Racing") {
          performanceAdjustment += 0.5;
          aeroAdjustment += 3.0;
        }
      }

      // Temperature effects
      if (parseFloat(data.air_temperature) > 30) {
        // Ferrari engines perform better in heat
        if (team.name === "Ferrari" || team.name === "Alfa Romeo" || team.name === "Haas F1 Team") {
          powerAdjustment += 2.0;
          performanceAdjustment += 0.2;
        } else {
          // Others might struggle
          powerAdjustment -= 1.0;
        }
      } else if (parseFloat(data.air_temperature) < 15) {
        // Mercedes performs better in cooler temps
        if (team.name === "Mercedes" || team.name === "Aston Martin" || team.name === "Williams") {
          performanceAdjustment += 0.3;
        }
      }

      // Rain effects
      if (parseFloat(data.rainfall) > 5) {
        // Some teams are better in the wet
        if (team.name === "Red Bull Racing" || team.name === "Mercedes") {
          aeroAdjustment += 3.0;
          chassisAdjustment += 2.0;
          performanceAdjustment += 0.4;
        } else if (team.name === "Ferrari") {
          // Ferrari struggles in wet
          performanceAdjustment -= 0.3;
        }
      }

      // Straight line speed effects
      if (parseFloat(data.st_speed) > 330) {
        // Teams with better aero
        if (team.aerodynamics > 95) {
          performanceAdjustment += 0.2;
        }
      }

      // Calculate final performance
      const finalPerformance = (
        team.basePerformance +
        performanceAdjustment
      ).toFixed(1);

      return {
        ...team,
        finalPerformance: parseFloat(finalPerformance),
        aerodynamics: team.aerodynamics + aeroAdjustment,
        power: team.power + powerAdjustment,
        chassis: team.chassis + chassisAdjustment,
        tireManagement: team.tireManagement + tireAdjustment
      };
    });

    // Sort teams by performance
    modifiedTeams.sort((a, b) => b.finalPerformance - a.finalPerformance);

    // Calculate advantage relative to top team
    const topPerformance = modifiedTeams[0].finalPerformance;
    modifiedTeams.forEach(team => {
      team.advantage = team.finalPerformance === topPerformance ?
        "BASELINE" :
        ((team.finalPerformance - topPerformance).toFixed(1) + "%");
    });

    // Race conditions summary
    const raceConditions = {
      trackTemp: (parseFloat(data.air_temperature) + 10).toFixed(1),
      airTemp: data.air_temperature,
      humidity: (50 + Math.random() * 30).toFixed(1),
      windSpeed: data.wind_speed,
      windDirection: data.wind_direction,
      rainfall: data.rainfall,
      compound: data.compound
    };

    resolve({
      teams: modifiedTeams,
      raceConditions: raceConditions,
      trackName: "Test Grand Prix"
    });
  });
}

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

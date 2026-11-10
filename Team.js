function selectTeam(teamCode)
{
    document.querySelector('.team-grid').style.display = 'none';
    document.getElementById('dashboard-view').style.display = 'block';

    fetch(`http://127.0.0.1:5002/api/scores/${teamCode}`)
        .then(r => r.json())
        .then(data => {
            const weeks = data.map(g => 'Wk' + g.week + ' ' + g.opponent);
            const teamScores = data.map(g => g.team_score);
            const oppScores = data.map(g => g.opp_score);
            const wins = data.filter(g => g.result === 'W').length;
            const losses = data.filter(g => g.result === 'L').length;
            document.getElementById('record-text').innerText = wins + ' - ' + losses;
            const avgScored = (data.reduce((sum, g) => sum + g.team_score, 0) / data.length).toFixed(1);
            const avgallowed = (data.reduce((sum, g) => sum + g.opp_score, 0) / data.length).toFixed(1);
            const winPct = ((wins / data.length) * 100).toFixed(1) + '%';
            document.getElementById('avg-scored').innerText = avgScored
            document.getElementById('avg-allowed').innerText = avgallowed
            document.getElementById('win-pct').innerText = winPct
            new Chart(document.getElementById("winLossChart"), {
                type: 'doughnut',
                data: {
                    labels: ['Wins', 'Losses'],
                    datasets: [{
                        data: [wins, losses],
                        backgroundColor: ['#00b140', '#a5acaf']
                        }]
                    }
                });
            new Chart(document.getElementById('scoresChart'), {
                type: 'bar',
                data: {
                    labels: weeks,
                    datasets: [
                        { label: teamCode, data: teamScores, backgroundColor: '#00b140'}, 
                        { label: 'Opponent', data: oppScores, backgroundColor: '#a5acaf'}
                        ]
                    }
                });
            });
            fetch(`http://127.0.0.1:5002/api/home_away/${teamCode}`)
            .then(r => r.json())
            .then(data => {
                new Chart(document.getElementById('homeAwayChart'), 
                {type: 'bar', 
                data: {labels: ['Wins', 'Losses', 'Avg Scored', 'Avg Allowed'], 
                datasets: [ 
                    {
                        label: 'Home', data: [data.home.wins, data.home.losses, data.home.avg_scored, data.home.avg_allowed],
                        backgroundColor: '#00b140'
                    },
                    {
                        label: 'Away', data: [data.away.wins, data.away.losses, data.away.avg_scored, data.away.avg_allowed],
                        backgroundColor: '#a5acaf'
                    }
                ]
            }
        });

    });
}
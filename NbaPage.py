from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
from datetime import datetime, timedelta
import pytz  
from IPython.core.display import display, HTML

# Definir fusos horários
et_tz = pytz.timezone('US/Eastern')  
brt_tz = pytz.timezone('America/Sao_Paulo')  

# Buscar jogos do próximo dia
future_date = datetime.today() + timedelta(days=1)
future_date_str = future_date.strftime('%m/%d/%Y')  

# Buscar os jogos do dia futuro
scoreboard = scoreboardv2.ScoreboardV2(game_date=future_date_str)
games = scoreboard.get_dict()

# Mapeando os IDs das equipes para os nomes
team_dict = {team['id']: team['full_name'] for team in teams.get_teams()}

# Criando HTML dinâmico
html_output = """
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f7fc;
        color: #333;
        margin: 0;
        padding: 20px;
    }

    .game-card {
        display: flex;
        flex-direction: column;
        justify-content: flex-start; /* Ajuste: mantém a ordem e evita distâncias grandes */
        align-items: center;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease-in-out;
    }

    .game-card:hover {
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        transform: translateY(-5px);
    }

    /* Alinhamento horizontal para os times e logos */
    .teams-container {
        display: flex;
        justify-content: space-between;
        width: 100%;
        align-items: center;
    }

    .team {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .team img {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 2px solid #ddd;
        padding: 5px;
        transition: transform 0.2s ease-in-out;
    }

    .team img:hover {
        transform: scale(1.1);
    }

    .vs {
        font-weight: bold;
        font-size: 24px;
        color: #333;
    }

    .date-time {
        margin-top: 10px; /* Ajuste da distância entre times e data/hora */
        text-align: center;
        width: 100%;
    }

    .date {
        font-size: 16px;
        color: #777;
    }

    .time {
        font-size: 18px;
        color: #007bff;
    }

    .header {
        text-align: center;
        margin-bottom: 30px;
    }

    h1 {
        font-size: 30px;
        color: #333;
    }

    .game-card .team-name {
        font-size: 18px;
        color: #444;
        font-weight: bold;
    }
</style>

<div class="header">
    <h1>Próximos Jogos da NBA</h1>
</div>
"""

# Gerando os cards dos jogos
for game in games['resultSets'][0]['rowSet']:
    home_team_id = game[6]  # ID do time da casa
    away_team_id = game[7]  # ID do time visitante
    home_team = team_dict.get(home_team_id, 'Desconhecido')
    away_team = team_dict.get(away_team_id, 'Desconhecido')
    game_time_str = game[4]  
    game_date_str = game[0]  # Data no formato ISO (yyyy-mm-ddThh:mm:ss)

    # URLs dos logos
    home_logo_url = f"https://cdn.nba.com/logos/nba/{home_team_id}/primary/L/logo.svg"
    away_logo_url = f"https://cdn.nba.com/logos/nba/{away_team_id}/primary/L/logo.svg"

    # Corrigir e converter o horário para Brasília
    try:
        # Obtendo a data em formato completo
        game_date_obj = datetime.strptime(game_date_str, '%Y-%m-%dT%H:%M:%S')
        
        # Localizando para Eastern Time e convertendo para BRT
        game_date_et = et_tz.localize(game_date_obj)
        game_date_brt = game_date_et.astimezone(brt_tz)

        game_time_brt_str = game_date_brt.strftime('%H:%M')  # Hora no formato HH:MM
        game_date_brt_str = game_date_brt.strftime('%d/%m/%Y')  # Data no formato dd/mm/yyyy
    except ValueError:
        game_time_brt_str = 'Horário desconhecido'
        game_date_brt_str = 'Data desconhecida'

    # Criando o card HTML
    html_output += f"""
    <div class="game-card">
        <div class="teams-container">
            <div class="team">
                <img src="{home_logo_url}" alt="{home_team} Logo">
                <div class="team-name">{home_team}</div>
            </div>
            <div class="vs">🆚</div>
            <div class="team">
                <div class="team-name">{away_team}</div>
                <img src="{away_logo_url}" alt="{away_team} Logo">
            </div>
        </div>
        <div class="date-time">
            <div class="date">📅 {game_date_brt_str}</div>
            <div class="time">🕒 {game_time_brt_str} (BRT)</div>
        </div>
    </div>
    """

# Exibir na tela
display(HTML(html_output))

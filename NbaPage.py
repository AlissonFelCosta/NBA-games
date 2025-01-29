from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
from datetime import datetime, timedelta
import pytz  
from IPython.core.display import display, HTML

# Definir fusos horários
et_tz = pytz.timezone('US/Eastern')  
brt_tz = pytz.timezone('America/Sao_Paulo')  

# Buscar jogos do próximo dia
future_date = datetime.today() + timedelta(days=2)
future_date_str = future_date.strftime('%m/%d/%Y')  

# Buscar os jogos do dia futuro
scoreboard = scoreboardv2.ScoreboardV2(game_date=future_date_str)
games = scoreboard.get_dict()

# Mapeando os IDs das equipes para os nomes
team_dict = {team['id']: team['full_name'] for team in teams.get_teams()}

# Criando HTML dinâmico
html_output = """
<style>
    .game-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }
    .team {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .team img {
        width: 50px;
        height: 50px;
    }
    .vs {
        font-weight: bold;
        font-size: 20px;
        color: #444;
    }
    .time {
        font-size: 16px;
        color: #007bff;
    }
</style>
"""

# Gerando os cards dos jogos
for game in games['resultSets'][0]['rowSet']:
    home_team_id = game[6]  # ID do time da casa
    away_team_id = game[7]  # ID do time visitante
    home_team = team_dict.get(home_team_id, 'Desconhecido')
    away_team = team_dict.get(away_team_id, 'Desconhecido')
    game_time_str = game[4]  

    # URLs dos logos
    home_logo_url = f"https://cdn.nba.com/logos/nba/{home_team_id}/primary/L/logo.svg"
    away_logo_url = f"https://cdn.nba.com/logos/nba/{away_team_id}/primary/L/logo.svg"

    # Converter horário para Brasília
    try:
        game_time_et = datetime.strptime(game_time_str, '%I:%M %p ET')  
        game_time_et = et_tz.localize(game_time_et)  
        game_time_brt = game_time_et.astimezone(brt_tz)  
        game_time_brt_str = game_time_brt.strftime('%H:%M')  
    except ValueError:
        game_time_brt_str = 'Horário desconhecido'  

    # Criando o card HTML
    html_output += f"""
    <div class="game-card">
        <div class="team">
            <img src="{home_logo_url}" alt="{home_team} Logo">
            <span>{home_team}</span>
        </div>
        <div class="vs">🆚</div>
        <div class="team">
            <span>{away_team}</span>
            <img src="{away_logo_url}" alt="{away_team} Logo">
        </div>
        <div class="time">🕒 {game_time_brt_str} (BRT)</div>
    </div>
    """

# Exibir na tela
display(HTML(html_output))

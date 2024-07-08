import random
import time
from collections import defaultdict

teams = [
    "Benfica", "Porto", "Sporting", "Braga", "Vitoria SC",
    "Boavista", "Nacional", "Estrela Da Amadora", "Gil Vicente",
    "Santa Clara", "Rio Ave", "AVS", "Estoril", "Arouca",
    "Famalicao", "Casa Pia", "Moreirense", "Farense"
]



def generate_round_robin_schedule(teams):
    if len(teams) % 2 != 0:
        teams.append(None)
    
    schedule = []
    num_teams = len(teams)
    rounds = num_teams - 1
    
    for round_num in range(rounds):
        round_matches = []
        for i in range(num_teams // 2):
            team1 = teams[i]
            team2 = teams[num_teams - 1 - i]
            if team1 is not None and team2 is not None:
                if round_num % 2 == 0:
                    round_matches.append((team1, team2))
                else:
                    round_matches.append((team2, team1))
        teams.insert(1, teams.pop())  # Gira a lista de times
        schedule.append(round_matches)
    
    return schedule


def double_round_robin_schedule(teams):
    first_half = generate_round_robin_schedule(teams)
    second_half = [(away, home) for home, away in sum(first_half, [])]
    second_half = [second_half[i:i + len(teams) // 2] for i in range(0, len(second_half), len(teams) // 2)]
    return first_half + second_half


def simulate_match(team1, team2):
    score1 = random.randint(0, 3)
    score2 = random.randint(0, 3)
    return (team1, score1, team2, score2)


def calculate_standings(results):
    standings = defaultdict(lambda: {'Pontos': 0, 'Golos Marcados': 0, 'Golos Sofridos': 0, 'Diferença de Golos': 0})

    for team1, score1, team2, score2 in results:
        standings[team1]['Golos Marcados'] += score1
        standings[team1]['Golos Sofridos'] += score2
        standings[team1]['Diferença de Golos'] += (score1 - score2)

        standings[team2]['Golos Marcados'] += score2
        standings[team2]['Golos Sofridos'] += score1
        standings[team2]['Diferença de Golos'] += (score2 - score1)

        if score1 > score2:
            standings[team1]['Pontos'] += 3
        elif score1 < score2:
            standings[team2]['Pontos'] += 3
        else:
            standings[team1]['Pontos'] += 1
            standings[team2]['Pontos'] += 1

    return standings


def print_standings(standings):
    sorted_standings = sorted(standings.items(), key=lambda x: (-x[1]['Pontos'], -x[1]['Golos Marcados']))
    print("\nClassificação Atual:")
    for position, (team, stats) in enumerate(sorted_standings, start=1):
        print(f"{position}. {team} - {stats['Pontos']} pts, DG: {stats['Diferença de Golos']}, GM: {stats['Golos Marcados']}, GS: {stats['Golos Sofridos']}")


random.shuffle(teams)
schedule = double_round_robin_schedule(teams)


standings = defaultdict(lambda: {'Pontos': 0, 'Golos Marcados': 0, 'Golos Sofridos': 0, 'Diferença de Golos': 0})
all_results = []


with open("calendario_jogos.txt", "w") as cal_file, open("resultados_jogos.txt", "w") as res_file:
    for round_num, round_matches in enumerate(schedule, start=1):
        cal_file.write(f"Jornada {round_num}:\n")
        res_file.write(f"Jornada {round_num}:\n")
        print(f"\nJornada {round_num}:")

        for match in round_matches:
            cal_file.write(f"  {match[0]} vs {match[1]}\n")


            team1, score1, team2, score2 = simulate_match(match[0], match[1])
            all_results.append((team1, score1, team2, score2))


            standings[team1]['Golos Marcados'] += score1
            standings[team1]['Golos Sofridos'] += score2
            standings[team1]['Diferença de Golos'] += (score1 - score2)

            standings[team2]['Golos Marcados'] += score2
            standings[team2]['Golos Sofridos'] += score1
            standings[team2]['Diferença de Golos'] += (score2 - score1)

            if score1 > score2:
                standings[team1]['Pontos'] += 3
            elif score1 < score2:
                standings[team2]['Pontos'] += 3
            else:
                standings[team1]['Pontos'] += 1
                standings[team2]['Pontos'] += 1

            res_file.write(f"  {team1} {score1} - {score2} {team2}\n")
            print(f"  {team1} {score1} - {score2} {team2}")

        res_file.write("\n")
        print_standings(standings)
        time.sleep(5)


sorted_standings = sorted(standings.items(), key=lambda x: (-x[1]['Pontos'], -x[1]['Golos Marcados']))


with open("tabela_campeonato.txt", "w") as file:
    file.write("Classificaçao Final:\n")
    for position, (team, stats) in enumerate(sorted_standings, start=1):
        file.write(f"{position}. {team} - {stats['Pontos']} pts, DG: {stats['Diferença de Golos']}, GM: {stats['Golos Marcados']}, GS: {stats['Golos Sofridos']}\n")


print("\nClassificação Final:")
for position, (team, stats) in enumerate(sorted_standings, start=1):
    print(f"{position}. {team} - {stats['Pontos']} pts, DG: {stats['Diferença de Golos']}, GM: {stats['Golos Marcados']}, GS: {stats['Golos Sofridos']}")

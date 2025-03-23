from django.shortcuts import render
from .models import Team, Match, MatchResult
from django.db.models import Sum, Max, Min

def home(request):
    teams = Team.objects.all()
    matches = Match.objects.all()
    team_stats = []

    for team in teams:
        results = MatchResult.objects.filter(team=team)
        
        if results.exists():
            # Aggregate points and stats
            total_points = results.aggregate(Sum('points'))['points__sum'] or 0
            highest_point = results.aggregate(Max('points'))['points__max'] or 0
            lowest_point = results.aggregate(Min('points'))['points__min'] or 0
            matches_attended = results.count()  # Total matches attended by the team

            # Count finishes from 1st to 11th
            position_counts = {str(i): 0 for i in range(1, 12)}
            for match in matches:
                match_results = MatchResult.objects.filter(match=match).order_by('-points')
                
                for position, result in enumerate(match_results, start=1):
                    if result.team == team:
                        position_counts[str(position)] += 1
                        break

            team_stats.append({
                'team': team,
                'total_points': total_points,
                'highest_point': highest_point,
                'lowest_point': lowest_point,
                'matches_attended': matches_attended,
                'position_counts': position_counts,
                'total_firsts': position_counts['1']
            })

    # Sorting by the number of 1st place finishes, then by total points
    team_stats = sorted(team_stats, key=lambda x: (x['total_firsts'], x['total_points']), reverse=True)
    
    # Adding position numbers based on sorting
    for index, team in enumerate(team_stats):
        team['position'] = index + 1

    context = {'team_stats': team_stats}
    return render(request, 'home.html', context)

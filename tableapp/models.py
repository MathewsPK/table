from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    match_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.match_name


class MatchResult(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField()
    series_form = models.CharField(max_length=1, choices=[('W', 'Win'), ('L', 'Lose')], default='L')

    def __str__(self):
        return f"{self.team.name} - {self.match.match_name}"

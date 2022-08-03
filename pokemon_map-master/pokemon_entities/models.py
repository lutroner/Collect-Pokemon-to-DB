import datetime

from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='')
    title_jp = models.CharField(max_length=200, default='')
    image = models.ImageField(blank=True)
    description = models.TextField(default='')
    evolved_from = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Из кого эволюционирует',
                                     related_name='next_evolution')

    # evolved_to = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
    #                                verbose_name='В кого эволюционирует')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(default=datetime.datetime.now)
    disappeared_at = models.DateTimeField(default=datetime.datetime.now)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)

    def __str__(self):
        return self.pokemon.title + ' Entity'

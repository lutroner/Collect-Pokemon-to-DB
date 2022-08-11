import datetime

from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField('Имя', max_length=200)
    title_en = models.CharField('Имя(англ)', max_length=200, blank=True)
    title_jp = models.CharField('Имя(япон)', max_length=200, blank=True)
    image = models.ImageField('Изображение', blank=True)
    description = models.TextField('Описание')
    evolved_from = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Из кого эволюционирует',
                                     related_name='next_evolution')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Объект покемона"""
    lon = models.FloatField('Долгота')
    lat = models.FloatField('Широта')
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    appeared_at = models.DateTimeField('Появился', default=datetime.datetime.now)
    disappeared_at = models.DateTimeField('Исчез', default=datetime.datetime.now)
    level = models.IntegerField('Уровень', blank=True)
    health = models.IntegerField('Здоровье', blank=True)
    strength = models.IntegerField('Сила', blank=True)
    defence = models.IntegerField('Защита', blank=True)
    stamina = models.IntegerField('Выносливость', blank=True)

    def __str__(self):
        return 'Объект ' + self.pokemon.title

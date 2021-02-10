from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.functions import datetime

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50,
                            blank=False,
                            unique=True,
                            verbose_name='Категория'
                            )
    slug = models.SlugField(max_length=50, blank=False,
                            null=True, unique=True
                            )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50,
                            blank=False,
                            unique=True,
                            verbose_name='Жанр'
                            )
    slug = models.SlugField(max_length=50, blank=False,
                            null=True, unique=True
                            )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        default=datetime.datetime.now().year,
        validators=[
            MaxValueValidator(datetime.datetime.today().year)
        ]
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Рейтинг не может быть выше 10'),
        ],
        null=True,
        verbose_name="Рейтинг",
    )
    description = models.TextField(
        max_length=1000,
        verbose_name='Краткое описание',
    )
    genre = models.ManyToManyField(Genre, related_name='title')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )
    slug = models.SlugField(max_length=40)


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Оценка не может превышать 10'),
        ],
        verbose_name='Оценка',
    )

    class Meta:
        ordering = (
            '-pub_date',
        )


class Comments(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Комментарий',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления комментария",
        auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = (
            '-pub_date',
        )


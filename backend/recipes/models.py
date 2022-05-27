# import base64
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    # MEASUREMENT_CHOISES = (
    #     ('kg', 'kg'),
    #     ('g', 'g'),
    #     ('slices', 'slices'),
    #     ('tablespoon', 'tablespoon'),
    #     ('teaspoon', 'teaspoon'),
    #     ('glass', 'glass'),
    #     ('pinch', 'pinch'),
    #     ('pieces', 'pieces'),
    #     ('ml', 'ml'),
    #     ('l', 'l'),
    #     ('to taste', 'to taste'),
    # )
    name = models.CharField(
        max_length=200,
        verbose_name='Название продуктов',
        help_text='Введите название продуктов')
    measurement_unit = models.CharField(
        max_length=200,
        # choices=MEASUREMENT_CHOISES,
        default='g',
        verbose_name='Единицы измерения',
        help_text='Выберете единицы измерения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Укажите название тега')
    color = ColorField(
        format='hex',
        verbose_name='Цвет',
        help_text='Введите цвет тега')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Идентификатор тега',
        help_text='Введите текстовый идентификатор тега')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(upload_to='image/', verbose_name='Изображение')
    # image = models.ImageField(
    #     verbose_name='Изображение',
    #     upload_to='recipes/image/',
    #     help_text='Выберите изображение рецепта'

    # )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Добавьте описание рецепта')
    cooking_time = models.IntegerField(
        validators=(MinValueValidator(
            1,
            message='Минимальное время приготовления - одна минута',
        ),),
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Тег рецепта',
        help_text='Выберите тег рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Продукты в рецепте',
        help_text='Выберите продукты рецепта')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Добавить дату создания')

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепты',
        help_text='Выберите рецепты для добавления в корзину'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                       name='unique_cart')]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор для подписки'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(fields=['user', 'following'],
                       name='unique_subscribe')]

    def __str__(self):
        return f'{self.user} {self.following}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Ингредиенты рецепта',
        help_text='Добавить ингредиенты в корзину')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipes',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество продукта',
        help_text='Укажите количество продукта'
    )

    class Meta:
        verbose_name = 'Продукты в рецепте'
        constraints = [models.UniqueConstraint(fields=['ingredient', 'recipe'],
                       name='unique_ingredientrecipe')]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги',
        help_text='Выберите теги для рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт')

    class Meta:
        verbose_name = 'Теги рецепта'
        constraints = [models.UniqueConstraint(fields=['tag', 'recipe'],
                       name='unique_tagrecipe')]

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                       name='unique_favorite')]

    def __str__(self):
        return f'{self.recipe} {self.user}'

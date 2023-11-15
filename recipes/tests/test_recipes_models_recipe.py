from django.core.exceptions import ValidationError
from .test_recipes_base import RecipeTestBase, Recipe
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='test default category'),
            author=self.make_author(username='newuser'),
            title='Recipe title',
            description='Recipe descripition',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe preparation steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_html_false_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation steps is html is not false',
        )

    def test_recipe_is_published_false_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not false',
        )

from django.urls import reverse, resolve
from recipes import views
from .test_recipes_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipes_home_view_function_correct(self):
        view = resolve(reverse('recipes-home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_returns_status_code_200(self):
        response = self.client.get(reverse('recipes-home'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes-home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_templates_shows_no_recipe_found(self):
        response = self.client.get(reverse('recipes-home'))
        self.assertIn('No recipe found', response.content.decode('utf-8'))

    def test_recipes_home_templates_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes-home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipes_home_templates_dont_loads_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes-home'))
        self.assertIn('No recipe found', response.content.decode('utf-8'))

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes-category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipes_category_view_returns_404(self):
        response = self.client.get(
            reverse('recipes-category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_templates_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes-category', args=(1,)))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipes_category_templates_dont_loads_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes-recipe', kwargs={'id': recipe.category.id})
            )
        self.assertEqual(response.status_code, 404)

    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes-recipe', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipes_detail_view_returns_404(self):
        response = self.client.get(
            reverse('recipes-recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipes_detail_templates_loads_correct_recipes(self):
        needed_title = 'This is a detail page test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes-recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipes_detail_templates_dont_loads_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes-recipe', kwargs={'id': recipe.id})
            )
        self.assertEqual(response.status_code, 404)

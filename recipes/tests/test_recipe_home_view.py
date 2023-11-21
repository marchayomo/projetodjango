from django.urls import reverse, resolve
from recipes import views
from .test_recipes_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
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
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()
        response = self.client.get(reverse('recipes-home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipes_home_templates_dont_loads_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes-home'))
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

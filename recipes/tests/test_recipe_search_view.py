from django.urls import reverse, resolve
from recipes import views
from .test_recipes_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipes_search_uses_correct_view(self):
        resolved = resolve(reverse('recipes-search'))
        self.assertIs(resolved.func, views.search)

    def test_recipes_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes-search')+ '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipes_search_raises_404_if_no_search(self):
        url = reverse('recipes-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes-search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

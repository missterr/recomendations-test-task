from django.shortcuts import reverse
from django.test import TransactionTestCase

from users.helpers import add_recommendations
from users.models import User

HTTP_200_OK = 200


class RecommendationTestCase(TransactionTestCase):
    fixtures = ['genres.json', 'users.json', 'movies.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='user1@test.com')
        self.client.force_login(self.user)

    def test_add_recommendations(self):
        self.assertEqual(self.user.recommendation_set.count(), 0)
        add_recommendations(self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.recommendation_set.count(), 10)

    def test_get_recommendation(self):
        url = reverse('recommendation')
        already_recommended = []
        add_recommendations(self.user)

        for _ in range(3):
            response = self.client.get(url)
            recommendations = response.json()['recommendations']

            self.assertEqual(response.status_code, HTTP_200_OK)
            self.assertEqual(len(recommendations), 3)
            for movie_id in recommendations:
                self.assertNotIn(movie_id, already_recommended)
                already_recommended.append(movie_id)

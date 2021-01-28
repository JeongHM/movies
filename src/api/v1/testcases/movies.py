import json
import string
import requests
import unittest

from datetime import date
from random import choice, randrange

from src.api.common.constants import CONSTANTS


class MoviesControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setting initial variable
        :return: None
        """
        self._host = "http://localhost:5050"
        self._headers = {"Content-Type": "application/json"}
        self._movie_data = {
            "name": "".join([choice(string.ascii_letters) for i in range(10)]),
            "genre": choice(["Action", "Romance", "Horror", "Thriller"]),
            "grade": choice([7, 12, 15, 19]),
            "release_at": date(year=randrange(1980, 2021),
                               month=randrange(1, 12),
                               day=randrange(1, 27)).strftime("%Y-%m-%d"),
            "views": randrange(1, 10000000)
        }

    def request_get(self, path: str = None):
        """
        [GET] Request function
        :param path: uri ( ex. /api/v1/movies )
        :return:
        """
        url = self._host if not path else self._host + path
        req = requests.get(url=url)

        return req

    def request_post(self, data: dict, path: str = None):
        url = self._host if not path else self._host + path
        req = requests.post(url=url,
                            data=json.dumps(data),
                            headers=self._headers)

        return req

    def request_put(self):
        pass

    def request_delete(self, path: str = None):
        """
        [DELETE] Request function
        :param path: uri ( ex. /api/v1/movies )
        :return:
        """
        url = self._host if not path else self._host + path
        req = requests.delete(url=url)

        return req

    def test_get_movies_with_success(self):
        """
        Test Movies Controller 200 Response
            [GET] http://127.0.0.1:5050/api/v1/movies
        :return:
        """
        # delete all movies data
        delete_req = self.request_delete(path=CONSTANTS["V1_MOVIE_API"])
        status_code = delete_req.status_code

        self.assertEqual(200, status_code)

        # create movie data
        self.request_post(data=self._movie_data, path=CONSTANTS["V1_MOVIE_API"])

        # get movie all data
        req = self.request_get(path=CONSTANTS["V1_MOVIE_API"])
        resp = req.json()
        status_code = req.status_code

        self.assertEqual(200, status_code)
        self.assertEqual(1, len(resp["result"]["movies"]))

    def test_get_movies_with_no_content(self):
        """
        Test Movies Controller 204 Response
            [GET] http://127.0.0.1:5050/api/v1/movies
        :return:
        """
        delete_req = self.request_delete(path=CONSTANTS["V1_MOVIE_API"])
        status_code = delete_req.status_code

        self.assertEqual(200, status_code)

        get_req = self.request_get(path=CONSTANTS["V1_MOVIE_API"])
        status_code = get_req.status_code

        self.assertEqual(204, status_code)

    def test_post_movies_success(self):
        """
        Test Movies Controller 200 Response
            [POST] http://127.0.0.1:5050/api/v1/movies
        :return:
        """

        post_req = self.request_post(data=self._movie_data,
                                     path=CONSTANTS["V1_MOVIE_API"])
        post_status_code = post_req.status_code

        self.assertEqual(200, post_status_code)

        req = self.request_get(path=CONSTANTS["V1_MOVIE_API"])
        resp = req.json()

        last_movie = resp["result"]["movies"][-1]
        del last_movie["id"]
        del last_movie["created_at"]

        self.assertEqual(self._movie_data, last_movie)

    def test_post_movies_bad_request(self):
        """
        Test Movies Controller 400 Response
            [POST] http://127.0.0.1:5050/api/v1/movies
        :return:
        """
        pass

    def test_post_movies_conflict(self):
        """
        Test Movies Controller 409 Response
            [POST] http://127.0.0.1:5050/api/v1/movies
        :return:
        """
        data = self._movie_data
        data["name"] = "new world"

        self.request_post(data=data, path=CONSTANTS["V1_MOVIE_API"])

        post_req = self.request_post(data=data,
                                     path=CONSTANTS["V1_MOVIE_API"])

        post_status_code = post_req.status_code
        self.assertEqual(409, post_status_code)

    def test_put_movies_success(self):
        """
        Test Movies Controller 200 Response
            [PUT] http://127.0.0.1:5050/api/v1/movies
        :return:
        """
        pass

    def test_delete_movies_success(self):
        """
        Test Movies Controller 200 Response
            [DELETE] http://127.0.0.1:5050/api/v1/movies
        :return:
        """
        delete_req = self.request_delete(path=CONSTANTS["V1_MOVIE_API"])
        status_code = delete_req.status_code

        self.assertEqual(200, status_code)

        get_req = self.request_get(path=CONSTANTS["V1_MOVIE_API"])
        status_code = get_req.status_code

        self.assertEqual(204, status_code)

    def test_get_specific_movies_success(self):
        """
        Test Movies Controller 200 Response
            [DELETE] http://127.0.0.1:5050/api/v1/movies/{movie_id}
        :return:
        """
        get_req = self.request_get(path=CONSTANTS["V1_MOVIE_API"])
        resp = get_req.json()

        movie_ids = [str(movie.get("id")) for movie in resp["result"]["movies"]]
        movie_id = choice(movie_ids)

        req = self.request_get(path=CONSTANTS["V1_MOVIE_API"] + "/" + movie_id)
        status_code = req.status_code

        self.assertEqual(200, status_code)

    def test_get_specific_movies_no_content(self):
        """
        Test Movies Controller 204 Response
            [DELETE] http://127.0.0.1:5050/api/v1/movies/{movie_id}
        :return:
        """
        get_req = self.request_get(path=CONSTANTS["V1_MOVIE_API"])
        resp = get_req.json()

        movie_ids = [
            str(movie.get("id")) + "123" for movie in resp["result"]["movies"]
        ]

        movie_id = choice(movie_ids)
        req = self.request_get(path=CONSTANTS["V1_MOVIE_API"] + "/" + movie_id)
        status_code = req.status_code

        self.assertEqual(204, status_code)

if __name__ == '__main__':
    unittest.main()
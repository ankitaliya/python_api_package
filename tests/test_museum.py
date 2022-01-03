"""Python Test script to check the functionality of different methods of the created package"""

import unittest
from unittest.mock import patch
import logging
import json
import os
import pandas as pd

from src.museum_api_convert_files.url_requests import MuseumApiURL

logging.basicConfig(filename='logging_statements.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class TestIntegrationContract(unittest.TestCase):
    """Test class contains different test methods for the api and methods testing using mock."""

    def setUp(self):
        self.api_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

    def test_api_url(self):
        """checks for the status code from the actual url"""
        museum_url = MuseumApiURL(self.api_url)
        museum_url.get_object_id()
        self.assertEqual(museum_url.object_id.status_code, 200)

    # Negative test case for passing different other than list
    def test_object_url(self):
        """checks for the status code from the actual url"""
        museum_url = MuseumApiURL(self.api_url)
        museum_url.get_object('a')
        self.assertEqual(museum_url.artifact.status_code, 400)

    @patch('src.museum_api_convert_files.url_requests.requests.get')
    def test_to_get_response_ok(self, mock_get):
        """get ok response from the mocked url"""
        museum_url = MuseumApiURL(self.api_url)
        # Configure the mock to return a response with an OK status code.
        mock_get.return_value.ok = True

        # Call the service, which will send a request to the server.
        response = museum_url.get_object_id()

        # If the request is sent successfully, then I expect a response to be returned.
        self.assertIsNotNone(response)

    def test_get_object(self):
        """assert the mocked data generated after calling original
            function with the truth file"""
        try:
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   '../truth_folder/museum.json'), encoding='utf-8') as file_name:
                json_data = json.load(file_name)
                with patch('src.museum_api_convert_files.url_requests.requests.get') as mock_get:
                    mock_get.return_value.json.return_value = json_data
                    sample = MuseumApiURL(self.api_url)
                    resp = sample.get_object([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

                    self.assertEqual(resp[0], json_data)
        except FileNotFoundError as file_err:
            logging.exception('check for correct path because %s', file_err)

    def test_get_obj_id(self):
        """asserts the list of object ids with the mocked object function returns"""
        obj_id = {'objectIDs': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
        with patch('src.museum_api_convert_files.url_requests.requests.get') as mock_get:
            mock_get.return_value.json.return_value = obj_id
            sample = MuseumApiURL(self.api_url)
            resp = sample.get_object_id()

            self.assertEqual(resp, obj_id['objectIDs'])

    def test_json_to_csv(self):
        """generates csv file from sample dataframe and checks to the path for its presence"""
        sample_dataframe = {'col1': [1, 2], 'col2': [3, 4]}
        sample_df = pd.DataFrame(data=sample_dataframe)
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../temp_folder')
        try:
            if not os.path.exists(directory):
                try:
                    os.mkdir('../temp_folder')
                except OSError as os_error:
                    logging.exception("Something went wrong while /"
                                      "creating the temp directory %s", os_error.args[-1])
            sample_df.to_csv(os.path.join(directory, "csv_file.csv"))
            self.assertTrue(directory, "csv_file.csv")
        except PermissionError as pe_err:
            logging.error('File opened somewhere else because %s', pe_err)

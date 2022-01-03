"""Python Test script to check the functionality of different methods of the created package"""

import unittest
from unittest.mock import patch
import logging
import json
import os
import pandas as pd
from src.museum_api_convert_files.url_requests import MuseumApiURL
from src.museum_api_convert_files.csv_to_diff_form import Converter

temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), './temp_folder')
temp_dir_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../temp_folder')

logging.basicConfig(filename='test_logging.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class TestConvertCSV(unittest.TestCase):
    """Test class that have different test_methods to check for the different formats"""

    def setUp(self):
        self.api_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        try:
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   '../truth_folder/museum.json'), encoding='utf-8') as file_name:
                self.json_data = json.load(file_name)
        except FileNotFoundError as file_err:
            logging.exception("Check the file path %s", file_err)

        self.d_frame = self.generate_dataframe()
        self.csv_convert = Converter(temp_dir, self.d_frame)

    def generate_dataframe(self):
        """generates the dataframe from the mocked json response"""
        with patch('src.museum_api_convert_files.url_requests.requests.get') as mock_get:
            mock_get.return_value.json.return_value = self.json_data
            sample = MuseumApiURL(self.api_url)
            resp = sample.get_object([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

            data_frame = pd.DataFrame(resp[0])
            # normalizing the columns that having nested json structure
            for x_column in ['constituents', 'measurements', 'tags']:
                data_frame = data_frame.explode(x_column)
            df_main = pd.json_normalize(json.loads(data_frame.to_json(orient='records')))
            df_main.drop(columns=['constituents', 'measurements', 'tags'], inplace=True)
            df_main.fillna(0, inplace=True)

        return df_main

    def test_csv_generate_from_df(self):
        """generates csv file from mocked dataframe and checks to the path for its presence"""
        self.csv_convert.json_to_csv('test_csv.csv')
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'test_csv.csv')))

    def test_compare_generated_csv_with_truth(self):
        """compares csv file generated after test to the actual csv file"""
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               '../truth_folder/csv_file.csv'), encoding='utf-8') as csv_file:
            original_csv = csv_file.read()
        with open(os.path.join(temp_dir, 'test_csv.csv'), encoding='utf-8') as generated_file:
            generated_csv_file = generated_file.read()
        self.assertEqual(original_csv, generated_csv_file)

    def test_excel_generate_from_df(self):
        """generates excel file from mocked dataframe and checks to the path for its presence"""
        self.csv_convert.dataframe_to_excel('test_excel.xlsx')
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'test_excel.xlsx')))

    def test_compare_generated_excel_with_truth(self):
        """compares excel file generated after test to the actual excel file"""
        original_excel_df = pd.read_excel(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                       '../truth_folder/excel_file.xlsx'))
        generated_excel_df = pd.read_excel(os.path.join(temp_dir, 'test_excel.xlsx'))

        generated_excel_df.compare(original_excel_df)

    def test_xml_generate_from_df(self):
        """generates xml file from mocked dataframe and checks to the path for its presence"""
        self.csv_convert.dataframe_to_xml('test_xml.xml')
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'test_xml.xml')))

    def test_compare_generated_xml_with_truth(self):
        """compares xml file generated after test to the actual xml file"""
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               '../truth_folder/xml_file.xml'), encoding='utf-8') as xml_file:
            original_xml = xml_file.read()
        with open(os.path.join(temp_dir, 'test_xml.xml'), encoding='utf-8') as generated_file:
            generated_xml_file = generated_file.read()
        self.assertEqual(original_xml, generated_xml_file)

    def test_html_generate_from_df(self):
        """generates html file from mocked dataframe and checks to the path for its presence"""
        self.csv_convert.dataframe_to_html('test_html.html')
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'test_html.html')))

    def test_compare_generated_html_with_truth(self):
        """compares html file generated after test to the actual html file"""
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               '../truth_folder/html_file.html'), encoding='utf-8') as html_file:
            original_html = html_file.read()
        with open(os.path.join(temp_dir, 'test_html.html'), encoding='utf-8') as generated_file:
            generated_html_file = generated_file.read()
        self.assertEqual(original_html, generated_html_file)

    def test_pdf_generate_from_df(self):
        """generates pdf file from passed html file generated from test and
            checks to the path for its presence"""
        self.csv_convert.html_to_pdf('test_pdf.pdf', 'test_html.html')
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'test_pdf.pdf')))

    def test_directory_for_create_file_exists_or_not(self):
        """Raises error for wrong directory path"""
        with self.assertRaises(expected_exception=FileNotFoundError):
            with open(os.path.join(temp_dir_f, 'test_html.html'),
                      encoding='utf-8') as generated_file:
                generated_file.read()

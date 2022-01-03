import pdfkit
import logging
import os


"""
    The script contains a class that contains different methods to convert the 
    input files to different formats.
"""

logging.basicConfig(filename='logging_statements.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class Converter:
    """
    A class for generating excel file from the csv file inputted.

    Attributes: file - csv file that need to convert
    constructor: __init__() to initializes the parameters of the instance created.
        A constructor is always called by default when object is created.
    Methods:
        json_to_csv() - converts that json data to csv file.
        :returns - csv file
        csv_to_excel() - converts that csv file to excel file.
        :returns - excel file
        csv_to_html() - converts that csv file to html file.
        :returns - html file
        csv_to_xml() - converts that csv file to xml file.
        :returns - xml file
        html_to_pdf() - converts that html file to pdf file.
        :returns - pdf file
    """

    # parameterized constructor
    def __init__(self, directory, df):
        self.directory = directory
        self.df = df

    def json_to_csv(self, filename):
        try:
            if not os.path.exists(self.directory):
                try:
                    os.mkdir('./temp_folder')
                except OSError as ae:
                    logging.exception(
                        "Something went wrong while creating the temp_folder directory: {}".format(ae.args[-1]))
            self.df.to_csv(os.path.join(self.directory, filename))
        except PermissionError as pe:
            logging.error('from csv_to_excel function : ' + str(pe))

    def dataframe_to_excel(self, filename):
        try:
            if not os.path.exists(self.directory):
                try:
                    os.mkdir('./temp_folder')
                except OSError as ae:
                    logging.exception(
                        "Something went wrong while creating the temp_folder directory: {}".format(ae.args[-1]))
            self.df.to_excel(os.path.join(self.directory, filename))
        except PermissionError as pe:
            logging.error('from csv_to_excel function : ' + str(pe))

    def dataframe_to_html(self, filename):
        try:
            if not os.path.exists(self.directory):
                try:
                    os.mkdir('./temp_folder')
                except OSError as ae:
                    logging.exception(
                        "Something went wrong while creating the temp_folder directory: {}".format(ae.args[-1]))
            self.df.to_html(os.path.join(self.directory, filename))
        except PermissionError as pe:
            logging.error('from csv_to_html function : ' + str(pe))

    def dataframe_to_xml(self, filename):
        try:
            if not os.path.exists(self.directory):
                try:
                    os.mkdir('./temp_folder')
                except OSError as ae:
                    logging.exception(
                        "Something went wrong while creating the temp_folder directory: {}".format(ae.args[-1]))
            self.df.to_xml(os.path.join(self.directory, filename))
        except PermissionError as pe:
            logging.error('from csv_to_xml function : ' + str(pe))

    def html_to_pdf(self, filename, html_file):
        try:
            if not os.path.exists(os.path.join(self.directory, 'html_file.html')):
                logging.exception(f'FileNotFoundError: HTML report doesnt exist')
            path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdfkit.from_file(os.path.join(self.directory, html_file), os.path.join(self.directory, filename),
                             configuration=config, options={'page-height': '2500', 'page-width': '1270', 'encoding': "UTF-8"})
        except PermissionError as pe:
            logging.error('from html_to_pdf function : ' + str(pe))
        except FileNotFoundError as fe:
            logging.error('from html_to_pdf function : ' + str(fe))

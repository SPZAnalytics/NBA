try:
    import cPickle as pickle
except ImportError:
    import pickle

import csv
import json
import logging
import os


class NBAAgent(object):
    '''
    Base class for agents, such as NBAComAgent
    '''

    def __init__(self, scraper, parser, pipeline, db):
        self.scraper = scraper
        self.parser = parser
        self.pipeline = pipeline
        self.db = db

    def csv_to_dict (self, fn):
        '''
        Takes csv filename and returns dicts

        Arguments:
            fn: string - name of file to read/parse

        Returns:
            List of dicts
        '''
        with open(fn, "rb") as infile:
            for row in csv.DictReader(infile, skipinitialspace=True, delimiter=','):
                yield {k: v for k, v in row.items()}

    def json_to_dict (self, json_fname):
        '''
        Takes json file and returns data structure

        Arguments:
            json_fname: name of file to read/parse

        Returns:
            parsed json into dict
        '''
        if os.path.exists(json_fname):
            with open(json_fname, 'r') as infile:
                return json.load(infile)
        else:
            raise ValueError('{0} does not exist'.format(json_fname))

    def read_pickle (self, pkl_fname):
        '''
        Takes pickle file and returns data structure

        Arguments:
            pkl_fname: name of file to read/parse

        Returns:
            parsed json
        '''
        if os.path.exists(pkl_fname):
            with open(pkl_fname, 'rb') as infile:
                return pickle.load(infile)
        else:
            raise ValueError('{0} does not exist'.format(pkl_fname))

    def file_to_ds(self, fname):
        '''
        Pass filename, it returns data structure. Decides based on file extension.
        '''
        ext = os.path.splitext(fname)[1]
        if ext == '.csv':
            return self.csv_to_dict(fname)
        elif ext == '.json':
            return self.json_to_dict(fname)
        elif ext == 'pkl':
            return self.read_pickle(fname)
        else:
            raise ValueError('{0} is not a supported file extension'.format(ext))

    def save_csv (self, data, csv_fname, fieldnames, sep=';'):
        '''
        Takes datastructure and saves as csv file

        Arguments:
            data: python data structure
            csv_fname: name of file to save
            fieldnames: list of fields
        '''
        try:
            with open(csv_fname, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except:
            logging.exception('could not save csv file')

    def save_json (self, data, json_fname):
        '''
        Takes data and saves to json file

        Arguments:
            data: python data structure
            json_fname: name of file to save
        '''
        try:
            with open(json_fname, 'wb') as outfile:
                json.dump(data, outfile)
        except:
            logging.exception('{0} does not exist'.format(json_fname))
       
    def save_pickle (self, data, pkl_fname):
        '''
        Saves data structure to pickle file

        Arguments:
            data: python data structure
            pkl_fname: name of file to save
        '''
        try:
            with open(pkl_fname, 'wb') as outfile:
                pickle.dump(data, outfile)
        except:
            logging.exception('{0} does not exist'.format(pkl_fname))

    def save_file(self, data, fname):
        '''
        Pass filename, it returns datastructure. Decides based on file extension.
        '''
        ext = os.path.splitext(fname)[1]
        if ext == '.csv':
            self.save_csv(data=data, csv_fname=fname, fieldnames=data[0])
        elif ext == '.json':
            self.save_json(data, fname)
        elif ext == 'pkl':
            self.save_pickle(data, fname)
        else:
            raise ValueError('{0} is not a supported file extension'.format(ext))

if __name__ == '__main__':
    pass
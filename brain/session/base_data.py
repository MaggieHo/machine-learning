#!/usr/bin/python

'''@base_data

This file serves as the superclass for 'data_xx.py' files.

Note: the term 'dataset' used throughout various comments in this file,
      synonymously implies the user supplied 'file upload(s)', and XML url
      references.

'''

from brain.session.data.save_feature_count import feature_count
from brain.session.data.validate_file_extension import reduce_dataset
from brain.session.data.save_entity import entity
from brain.session.data.save_dataset import dataset
from brain.session.data.save_observation_label import observation_label
from brain.converter.convert_dataset import Convert_Dataset


class Base_Data(object):
    '''@Base_Data

    This class provides an interface to save, and validate the provided
    dataset, into logical ordering within the sql database.

    @self.uid, the logged-in user (i.e. userid).

    Note: this class is invoked within 'data_xx.py'.

    Note: this class explicitly inherits the 'new-style' class.

    '''

    def __init__(self, premodel_data):
        '''@__init__

        This constructor is responsible for defining class variables.

        '''

        self.observation_labels = []
        self.list_error = []
        self.uid = 1

    def save_feature_count(self):
        '''@save_feature_count

        This method saves the number of features that can be expected in a
        given observation with respect to 'id_entity'.

        Note: this method needs to execute after 'dataset_to_dict'

        '''

        # svm feature count
        response = feature_count(self.dataset[0])
        if response['error']:
            self.list_error.append(response['error'])

    def validate_file_extension(self):
        '''@validate_file_extension

        This method validates the file extension for each uploaded dataset,
        and returns the unique (non-duplicate) dataset.

        @self.session_type, defined from 'base.py' superclass.

        '''

        # validate and reduce dataset
        response = reduce_dataset(self.premodel_data, self.session_type)
        if response['error']:
            self.list_error.append(response['error'])
        else:
            self.upload = response['dataset']

    def validate_id(self, session_id):
        '''@validate_id

        This method validates if the session id, is a positive integer.

        '''

        error = '\'session_id\' ' + str(session_id) + ' not a positive integer'

        try:
            if not int(session_id) > 0:
                self.list_error.append(error)
        except Exception, error:
            self.list_error.append(str(error))

    def save_entity(self, session_type):
        '''@save_entity

        This method saves the current entity into the database, then returns
        the corresponding entity id.

        '''

        # save svm entity
        response = entity(self.premodel_data, session_type)

        # return result
        if response['error']:
            self.list_error.append(response['error'])
            return {'status': False, 'id': None, 'error': response['error']}
        else:
            return {'status': True, 'id': response['id'], 'error': None}

    def save_premodel_dataset(self):
        '''@save_premodel_dataset

        This method saves each dataset element (independent variable value)
        into the sql database.

        @self.dataset, defined from the 'dataset_to_dict' method.

        '''

        response = dataset(self.dataset)
        if response['error']:
            self.list_error.append(response['error'])

    def save_observation_label(self, session_type, session_id):
        '''save_observation_label

        This method saves the list of unique independent variable labels,
        which can be expected in any given observation, into the sql
        database. This list of labels, is predicated on a supplied session
        id (entity id).

        @self.observation_labels, list of features (independent variables),
            defined after invoking the 'dataset_to_dict' method.

        @session_id, the corresponding returned session id from invoking the
            'save_entity' method.

        '''

        response = observation_label(
            session_type,
            session_id,
            self.observation_labels
        )

        if response['error']:
            self.list_error.append(db_return['error'])

    def dataset_to_dict(self, id_entity):
        '''@dataset_to_dict

        This method converts the supplied csv, or xml file upload(s) to a
            uniform dict object.

        @flag_append, when false, indicates the neccessary 'self.dataset' was
            not properly defined, causing this method to 'return', which
            essentially stops the execution of the current session.

        '''

        flag_append = True
        self.dataset = []

        try:
            # web-interface: define flag to convert to dataset to json
            if self.upload['dataset']['file_upload']:
                for val in self.upload['dataset']['file_upload']:
                    # reset file-pointer
                    val['file'].seek(0)

                    # csv to dict
                    if val['type'] == 'csv':
                        try:
                            # conversion
                            converter = Convert_Dataset(val['file'])
                            converted = converter.csv_to_dict()
                            count_features = converter.get_feature_count()
                            labels = converter.get_observation_labels()

                            # assign observation labels
                            self.observation_labels.append(labels)

                            # build new (relevant) dataset
                            self.dataset.append({
                                'id_entity': id_entity,
                                'premodel_dataset': converted,
                                'count_features': count_features
                            })
                        except Exception as error:
                            self.list_error.append(error)
                            flag_append = False

                    # json to dict
                    elif val['type'] == 'json':
                        try:
                            # conversion
                            converter = Convert_Dataset(val['file'])
                            converted = converter.json_to_dict()
                            count_features = converter.get_feature_count()
                            labels = converter.get_observation_labels()

                            # assign observation labels
                            self.observation_labels.append(labels)

                        # build new (relevant) dataset
                            self.dataset.append({
                                'id_entity': id_entity,
                                'premodel_dataset': converted,
                                'count_features': count_features
                            })
                        except Exception as error:
                            self.list_error.append(error)
                            flag_append = False

                    # xml to dict
                    elif val['type'] == 'xml':
                        try:
                            # conversion
                            converter = Convert_Dataset(val['file'])
                            converted = converter.xml_to_dict()
                            count_features = converter.get_feature_count()
                            labels = converter.get_observation_labels()

                            # assign observation labels
                            self.observation_labels.append(labels)

                            # build new (relevant) dataset
                            self.dataset.append({
                                'id_entity': id_entity,
                                'premodel_dataset': converted,
                                'count_features': count_features
                            })
                        except Exception as error:
                            self.list_error.append(error)
                            flag_append = False

                if not flag_append:
                    return False

            # programmatic-interface
            elif self.upload['dataset']['json_string']:
                # conversion
                dataset_json = self.upload['dataset']['json_string']
                converter = Convert_Dataset(dataset_json, True)
                converted = converter.json_to_dict()
                count_features = converter.get_feature_count()

                self.observation_labels.append(dataset_json.keys())

                # build dataset
                self.dataset.append({
                    'id_entity': id_entity,
                    'premodel_dataset': converted,
                    'count_features': count_features
                })

        except Exception as error:
            self.list_error.append(error)
            print error
            return False

    def get_errors(self):
        '''get_errors

        This method gets all current errors. associated with this class
        instance.

        '''

        if len(self.list_error) > 0:
            return self.list_error
        else:
            return None

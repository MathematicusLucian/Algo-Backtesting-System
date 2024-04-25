# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from flask import jsonify

class BaseService(object):
    __model__ = None
    __metaclass__ = ABCMeta

    def __init__(self, api_key, base_currency):
        self.api_key = api_key
        self.base_currency = base_currency

    def _isinstance(self, obj, raise_error=True):
        rv = isinstance(obj, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (obj, self.__model__))
        return rv

    @abstractmethod
    def set_base_currency(self, obj):
        pass

    @abstractmethod
    def historic_values(self, obj):
        pass

    @abstractmethod
    def latest_values(self, obj):
        pass
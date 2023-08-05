"""
Elipse Plant Manager - EPM Web API
Copyright (C) 2018 Elipse Software.
Distributed under the MIT License.
(See accompanying file LICENSE.txt or copy at http://opensource.org/licenses/MIT)
"""

from .datavaluejson import DataValueJSON
from .statuscodes import StatusCodes
import numpy

class EpmUtils:
    @staticmethod
    def translateQuality(dataValues):
        if isinstance(dataValues, DataValueJSON):
            statusCode = dataValues.statusCode
            opcUa = EpmUtils._statusCodeToOpcUa(statusCode)
            dataValue = DataValueJSON(dataValues.value, opcUa, dataValues.timestamp)
            return dataValue
        elif isinstance(dataValues, dict):
            for numpyArray in dataValues.values():
                for num in numpyArray:
                    statusCode = num['Quality']
                    opcUa = EpmUtils._statusCodeToOpcUa(statusCode)
                    num['Quality'] = opcUa
            return dataValues
        elif isinstance(dataValues, numpy.ndarray):
            for num in dataValues:
                statusCode = num['Quality']
                opcUa = EpmUtils._statusCodeToOpcUa(statusCode)
                num['Quality'] = opcUa
            return dataValues
        else:
            raise Exception('Invalid dataValues parameter')

    @staticmethod
    def _statusCodeToOpcUa(statusCode):
        for code in StatusCodes:
            if statusCode == code.value:
                return code.name
        return statusCode

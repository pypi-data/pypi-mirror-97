import requests
import json
import base64
import os
import configparser


# check for api key set as an environment variable
if os.getenv('RAMCO_API_KEY') is not None:

    # use value if found
    api_key = os.environ['RAMCO_API_KEY']

# check for api key in file 'pyramco_config.ini'
elif configparser.ConfigParser().read('pyramco_config.ini'):

    # use value if found
    api_key = configparser.ConfigParser().get('pyramco_config', 'RAMCO_API_KEY')

else:
    api_key = None

    raise Exception(
        'No RAMCO API key was found. Please set your key as an environment variable or use a config file.')


# RAMCO API URL is always the same
url = 'https://api.ramcoams.com/api/v2/'


# response code/error handling

code_200 = {
    'DescriptionShort': 'OK',
    'DescriptionVerbose': 'The request was successfully processed and data is included in the response.'
}

code_204 = {
    'DescriptionShort': 'OK - No Data',
    'DescriptionVerbose': 'The request was successfully processed but no data is included in the response.'
}

code_206 = {
    'DescriptionShort': 'OK - Partial Data',
    'DescriptionVerbose': 'The request was successfully processed and partial data is included in the response. A StreamToken will be returned to fetch the remaining data.'
}

code_400 = {
    'DescriptionShort': 'Bad Request',
    'DescriptionVerbose': 'The request was not understood. See the response text for more information.'
}

code_401 = {
    'DescriptionShort': 'Unauthorized',
    'DescriptionVerbose': 'The request was understood but it will not be fulfilled due to a lack of user permissions. See the response text for more information.'
}

code_404 = {
    'DescriptionShort': 'Not Found',
    'DescriptionVerbose': 'The request is understood but no matching data is found to return.'
}

code_422 = {
    'DescriptionShort': 'Invalid User',
    'DescriptionVerbose': 'No user exists with provided username and password combination. This error is specific to the AuthenticateUser request.'
}

code_500 = {
    'DescriptionShort': 'Server Error',
    'DescriptionVerbose': 'Something is not working correctly server-side. This is not an issue that can be resolved by modifying query syntax.'
}

no_api_key = {
    'ResponseCode': 900,
    'DescriptionShort': 'No API Key',
    'DescriptionVerbose': 'No RAMCO API key was found. Please set your key as an environment variable, use a config file, or pass the key to the function as a string: api_key'
}

code_unknown = {
    'ResponseCode': 999,
    'DescriptionShort': 'Unknown Request Error',
    'DescriptionVerbose': 'No code or response returned from RAMCO. Please verify RAMCO API is working, and report this error to package maintainer at https://pypi.org/project/pyramco/'
}


# input parsing

# all replies from RAMCO are passed through the handler
def handler(reply):
    '''
    accepts a RAMCO API reply packet
    returns parsed results or error info
    '''

    # successful returns with data
    if reply['ResponseCode'] == 200 or reply['ResponseCode'] == 206:

        # replies contain a section 'Data' with returned information
        complete_data = reply['Data']

        # handles streamtoken responses
        while 'StreamToken' in reply:
            reply = resume_streamtoken(reply['StreamToken'])
            partial_data = reply['Data']

            # continue adding the 'Data' section to the full list
            complete_data.extend(partial_data)

        # return the original reply header and combined 'Data'
        reply['Data'] = complete_data
        return(reply)

    # return unmodified results if reply is 'OK - No data'
    elif reply['ResponseCode'] == 204:
        return(reply)

    # handle all errors, return results plus additional error text from documentation
    elif reply['ResponseCode'] == 400:
        reply = {**reply, **code_400}
        return(reply)

    elif reply['ResponseCode'] == 404:
        reply = {**reply, **code_404}
        return(reply)

    elif reply['ResponseCode'] == 422:
        reply = {**reply, **code_422}
        return(reply)

    elif reply['ResponseCode'] == 500:
        reply = {**reply, **code_500}
        return(reply)

    # return the text for other/unknown errors
    else:
        return(code_unknown)


# input parsing functions

# create string from list of attributes
def parse_attribute_list(attributes_list):
    '''
    accepts a list of attribute names
    returns them as a comma-separated string
    '''

    # join strings in the list with commas
    attributes_string = ','.join(attributes_list)

    return attributes_string


# create formatted strings from attribute/value dicts
def parse_attribute_values(attribute_values, string_delimiter='#'):
    '''
    accepts a dict of attribute/value pairs and 
    optionally a string delimiter 
    returns a formatted string of attribute/values 
    '''

    # remove any None values from attribute_values dict
    attribute_values = {k: v for k, v in attribute_values.items() if v is not None}

    # create a blank attribute_values list
    attribute_values_list = []

    # iterate over the dict items and assign them to strings
    for k, v in attribute_values.items():

        # if value type is str, use string delimiter and add string to list
        if type(v) == str:

            # handle literal # character in strings by b64encoding it
            v = v.replace("#", "Iw==")

            # add string to list
            attribute_values_list.append(f'{k}={string_delimiter}{v}{string_delimiter}')

        # for other value types just write the value
        else:
            attribute_values_list.append(f'{k}={v}')

    # join strings in the list to a single string
    attribute_values_string = ','.join(attribute_values_list)

    return attribute_values_string


# metadata operations

def get_entity_types(api_key=api_key, output=None):
    '''
    no arguments are accepted
    returns all entity names
    '''

    if api_key == None:
        return(no_api_key)

    else:
        payload = {
            'Key': api_key,
            'Operation': 'GetEntityTypes'
        }

        reply = handler(requests.post(url, payload).json())

        if output == 'json':
            return(json.dumps(reply))

        else:
            return reply


def get_entity_metadata(entity, output=None):
    '''
    accepts a valid entity schema name 
    returns all metadata for that entity
    '''

    if api_key == None:
        return(no_api_key)

    else:
        payload = {
            'Key': api_key,
            'Operation': 'GetEntityMetadata',
            'Entity': entity
        }

        reply = handler(requests.post(url, payload).json())

        if output == 'json':
            return(json.dumps(reply))

        else:
            return reply


def get_option_set(entity, attribute, api_key=api_key, output=None):
    '''
    accepts a valid entity schema name,
    and a single attribute name
    returns information for the specified OptionSet
    '''

    if api_key == None:
        return(no_api_key)

    else:
        payload = {
            'Key': api_key,
            'Operation': 'GetOptionSet',
            'Entity': entity,
            'Attribute': attribute
        }
        reply = handler(requests.post(url, payload).json())

        if output == 'json':
            return(json.dumps(reply))

        else:
            return reply


def clear_cache():
    '''
    no arguments are accepted
    clears the server-side metadata cache
    '''

    if api_key == None:
        return(no_api_key)

    else:
        payload = {
            'Key': api_key,
            'Operation': 'ClearCache'
        }

        reply = handler(requests.post(url, payload).json())
        return(reply)


# data querying operations

def get_entity(entity, guid, attributes, api_key=api_key, output=None):
    '''
    accepts an entity name, guid, output type,
    and a formatted string or list of attribute names
    returns attribute values for 
    the specified entity matching the guid
    '''

    if api_key == None:
        return(no_api_key)

    else:

        if type(attributes) is str:
            attributes_string = attributes

        else:
            attributes_string = parse_attribute_list(attributes)

        payload = {
            'Key': api_key,
            'Operation': 'GetEntity',
            'Entity': entity,
            'Guid': guid,
            'Attributes': attributes_string
        }

        reply = handler(requests.post(url, payload).json())

        if output == 'json':
            return(json.dumps(reply))

        else:
            return reply


def get_entities(entity, attributes, filters='', string_delimiter='#', max_results='', api_key=api_key, output=None):
    '''
    accepts an entity name, a formatted string or list of attribute names,
    and optionally a filter string, a string delimiter 
    character, an output type, and/or an int value for max results
    returns all results, or the first n results
    ## TODO - expand filter functionality
    '''

    if api_key == None:
        return(no_api_key)

    else:

        if type(attributes) is str:
            attributes_string = attributes

        else:
            attributes_string = parse_attribute_list(attributes)

        payload = {
            'Key': api_key,
            'Operation': 'GetEntities',
            'Entity': entity,
            'Filter': filters,
            'Attributes': attributes_string,
            'StringDelimiter': string_delimiter,
            'MaxResults': max_results
        }

        reply = handler(requests.post(url, payload).json())

        if output == 'json':
            return(json.dumps(reply))

        else:
            return reply


def resume_streamtoken(streamtoken, api_key=api_key):
    '''
    accepts a valid streamtoken and resumes 
    the get_entities request that generated it
    returns resumed results
    '''

    if api_key == None:
        return(no_api_key)

    else:
        payload = {
            'Key': api_key,
            'Operation': 'GetEntities',
            'StreamToken': streamtoken
        }

        reply = handler(requests.post(url, payload).json())
        return(reply)


def validate_user(username, password, api_key=api_key):
    '''
    accepts a username and password
    if valid: returns corresponding Contact's guid
    if invalid: returns 422 error
    '''

    if api_key == None:
        return(no_api_key)

    else:
        payload = {
            'Key': api_key,
            'Operation': 'ValidateUser',
            'cobalt_username': username,
            'cobalt_password': password
        }

        reply = handler(requests.post(url, payload).json())
        return(reply)


# data transformation operations

def update_entity(entity, guid, attribute_values, string_delimiter='#', api_key=api_key):
    '''
    accepts a valid entity name and guid, a formatted
    string or dict of of attribute: value pairs 
    and optionally a string delimiter character 
    returns '204 no data' if successful
    '''

    if api_key == None:
        return(no_api_key)

    else:

        if type(attribute_values) is str:
            attribute_values_string = attribute_values

        else:
            attribute_values_string = parse_attribute_values(attribute_values, string_delimiter)

        payload = {
            'Key': api_key,
            'Operation': 'UpdateEntity',
            'Entity': entity,
            'Guid': guid,
            'AttributeValues': attribute_values_string,
            'StringDelimiter': string_delimiter
        }

        reply = handler(requests.post(url, payload).json())
        return(reply)


def create_entity(entity, attribute_values, string_delimiter='#'):
    '''
    accepts a valid entity name, a formatted string or
    dict of of attribute: value pairs, and optionally
    a string delimiter character 
    returns created entity guid
    in 'reply['Data']' if successful
    '''

    if api_key == None:
        return(no_api_key)

    else:

        if type(attribute_values) is str:
            attribute_values_string = attribute_values

        else:
            attribute_values_string = parse_attribute_values(attribute_values, string_delimiter)

        payload = {
            'Key': api_key,
            'Operation': 'CreateEntity',
            'Entity': entity,
            'AttributeValues': attribute_values_string,
            'StringDelimiter': string_delimiter
        }

        reply = handler(requests.post(url, payload).json())
        return(reply)


def delete_entity(entity, guid):
    '''
    accepts a valid entity name and guid,
    deletes the corresponding record
    returns '204 no data' if successful
    '''

    if api_key == None:
        return(no_api_key)

    else:
        payload = {
            'Key': api_key,
            'Operation': 'DeleteEntity',
            'Entity': entity,
            'Guid': guid
        }

        reply = handler(requests.post(url, payload).json())
        return(reply)


# base64 encoder/decoder for attachments
def base64_encode(input):
    output = str(base64.standard_b64encode(input))
    return(output)


def base64_decode(input):
    output = base64.standard_b64decode(input)
    return(output)

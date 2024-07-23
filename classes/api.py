import requests

def api_post(url, data, headers=None):
    """
    Function to send a POST request to the API.

    :param url: The URL of the API endpoint.
    :param data: The data to be sent in the POST request.
    :param headers: Optional headers to include in the request.
    :return: Response object.
    """
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def api_get(url, headers=None):
    """
    Function to send a GET request to the API.

    :param url: The URL of the API endpoint.
    :param params: The parameters to be sent in the GET request.
    :param headers: Optional headers to include in the request.
    :return: Response object.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

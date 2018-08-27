def fetchBundle(address):
    import requests
    try:
        response = requests.get(address)
        if not response.status_code == 200:
            print("HTTP error ", response.status_code)
        else:
            try:
                response_data = response.json()
                return response_data
            except:
                print("Response not in valid json format.")
    except Exception as e:
        return e

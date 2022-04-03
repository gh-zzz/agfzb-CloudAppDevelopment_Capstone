import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        api_key = kwargs.get('api_key', None)
        if api_key != None:
            del kwargs['api_key']
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        api_key = kwargs.get('api_key', None)
        if api_key != None:
            del kwargs['api_key']
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'},
                                     params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'},
                                     params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result.get("dealerships", [])
        # For each dealer object
        for dealer in dealers:
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result.get("reviews", [])
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                dealership=review['dealership'],
                name=review['name'],
                purchase=review['purchase'],
                review=review['review'],
                purchase_date=review.get('purchase_date', ''),
                car_make=review.get('car_make', ''),
                car_model=review.get('car_model', ''),
                car_year=review.get('car_year', ''),
                sentiment=analyze_review_sentiments(review['review']),
                id=review.get('id', ''))
            results.append(review_obj)

    return results

def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    return get_dealers_from_cf(url, id=dealerId)

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/bf30f25c-b246-47bb-b407-bbf8f1af7f5b/v1/analyze'
    api_key = '1wpMe0SMPCHyJvzZpYt6CW7J051m1Uq9EI1BkWN1kGo1'
    payload = {
        "text": text,
        "features": {
            "sentiment": {
            }
        },
        "language": "en"
    }
    response = post_request(url, payload,
        api_key=api_key,
        version='2021-08-01'
    )
    print(response)
    return response["sentiment"]["document"]["label"]




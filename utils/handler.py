import requests

def post_request_for_elastic(logging, collection_name, data):
    url = "https://orangeshine.ent.us-central1.gcp.cloud.es.io/api/as/v1/engines/{}/documents".format(collection_name)
    headers = {
        'Authorization': 'Bearer private-c6dqiqjv2pftfdsip9ubbxdw',
        'Content-Type': 'application/json'
    }

    logging.info("Going To Insert In Engine = "+str(collection_name))
    try:
        response = requests.post(url, json=data, headers=headers)
        logging.info("Response is: "+str(response.json()))

    except Exception as e:
        logging.error("Response is: "+str( response.json()))


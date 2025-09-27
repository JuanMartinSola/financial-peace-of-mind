from apify_client import ApifyClient
import os
from dotenv import load_dotenv
def news_scrapper(query):
    # Initialize the ApifyClient with your API token

    load_dotenv()
    api_token = os.getenv("apify_API_KEY")
    openai_token = os.getenv("openai_API_KEY")
    client = ApifyClient(api_token)

    # Prepare the Actor input
    run_input = {
        "query": query,
        #"blacklistedWords": ["UPS Shipping Times"],
        "limit": 15,
        "includeSummary": True,
        "openaiKey": openai_token,
        "when": "1d",
        #"gl": "US",
        #"hl": "en-US",
        #"ceid": "US:en",
    }

    # Run the Actor and wait for it to finish
    run = client.actor("tRoh6zObCn8ADFJkT").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    return client.dataset(run["defaultDatasetId"]).iterate_items()
    #for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    #    print(item)
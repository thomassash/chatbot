
import json





def process(question,supabase_client):
    response = supabase_client.functions.invoke(
        "ask-custom-data",
        invoke_options={"body": json.dumps({ "query": question })})
    return response



from llmdomainrating import create_api_client, get_domain_to_query
import sys
import os
from tqdm.contrib.concurrent import thread_map

N_THREADS = 15

domain_list_path = sys.argv[1]
provider = sys.argv[2]
model = sys.argv[3]
output_root = sys.argv[4]
n_threads = int(sys.argv[5]) if len(sys.argv) > 5 else N_THREADS

client = create_api_client(provider)
domains_to_query = get_domain_to_query(domain_list_path, output_root)


def query_one(domain):
    resp = client.query_model(domain, model)
    if resp is None:
        print(f"No response for {domain}")
        return
    with open(os.path.join(output_root, f"{domain}.txt"), "w") as f:
        f.write(resp)


thread_map(query_one, domains_to_query, max_workers=n_threads, desc="Querying domains")

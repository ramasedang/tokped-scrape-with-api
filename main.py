import io
import pandas as pd
from task import *
from resource.utils import *
from resource.allreq import *
import concurrent.futures
import argparse
from resource.service import *
import time

webhook_url = "https://discord.com/api/webhooks/1023818941715456035/g1gXRsu-0Oe3W6BVvNWJN3NP5ScHR9FKSAxPSR1Az1RWlJLDSAiFTxhA6DQQrtTtRHbK"


def work(keyword, datatable):
    # print(datatable)
    return getLstProduct(keyword, datatable)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=str, help="Keyword argument")
    parser.add_argument("-c", type=str, help="Category argument")
    args = parser.parse_args()

    if args.c == "all":
        for key in byCategory:
            content_start = f"Start scraping {key} category"
            send_webhook_message(webhook_url, content_start)
            cat_list = byCategory[key]["lis_category"]
            cat_name = byCategory[key]["cat"]
            datatable = byCategory[key]["datatable"]
            start_time = time.time()  # Start time
            data = getCat(cat_name, cat_list, datatable)
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            # convert elapsed time to hh:mm:ss format and add date
            
            content_done = f"Scraping {key} category done\nElapsed Time: {elapsed_time} seconds"
            send_webhook_message(webhook_url, content_done)

    if args.k == "all":
        for key in byKeyword:
            content_start = f"Start scraping {key}"
            start_time = time.time()
            send_webhook_message(webhook_url, content_start)

            allProduct = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                results = executor.map(work, byKeyword[key]["list_keywords"])
                allProduct += [item for sublist in results for item in sublist]
            df = pd.DataFrame(allProduct)
            df.to_csv(f"{key}_data.csv", index=False)
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            content_done = f"Scraping {key} category done\nElapsed Time: {elapsed_time} seconds"
            send_webhook_message(webhook_url, content_done)
    elif args.k in byKeyword:
        content_start = f"Start scraping {args.k}"
        send_webhook_message(webhook_url, content_start)
        start_time = time.time()
        allProduct = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = executor.map(
                work,
                byKeyword[args.k]["list_keywords"],
                [byKeyword[args.k]["datatable"]]
                * len(byKeyword[args.k]["list_keywords"]),
            )
            allProduct += [item for sublist in results for item in sublist]
        with io.open(f"{args.k}_data.json", "w", encoding="utf-8") as f:
            json.dump(allProduct, f, ensure_ascii=False, indent=4)
        df = pd.DataFrame(allProduct)
        df.to_csv(f"{args.k}_data.csv", index=False)
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        content_done = f"Scraping {args.k} category done\nElapsed Time: {elapsed_time} seconds"
        send_webhook_message(webhook_url, content_done)
    elif args.c in byCategory:  # Add this block
        content_start = f"Start scraping {args.c} category"
        send_webhook_message(webhook_url, content_start)

        cat_list = byCategory[args.c]["lis_category"]
        cat_name = byCategory[args.c]["cat"]
        datatable = byCategory[args.c]["datatable"]
        start_time = time.time()  # Start time
        data = getCat(cat_name, cat_list, datatable)
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        content_done = f"Scraping {args.c} category done\nElapsed Time: {elapsed_time} seconds"
        send_webhook_message(webhook_url, content_done)
    else:
        print(f"No keywords or categories found for {args.k} or {args.c}")
        content_start = f"No keywords or categories found for {args.k} or {args.c}"
        send_webhook_message(webhook_url, content_start)

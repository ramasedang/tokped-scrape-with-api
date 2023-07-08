import io
import pandas as pd
from task import *
from resource.utils import *
from resource.allreq import *
import concurrent.futures
import argparse
from resource.service import *

webhook_url = "https://discord.com/api/webhooks/1023818941715456035/g1gXRsu-0Oe3W6BVvNWJN3NP5ScHR9FKSAxPSR1Az1RWlJLDSAiFTxhA6DQQrtTtRHbK"


def work(keyword, datatable):
    # print(datatable)
    return getLstProduct(keyword, datatable)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=str, help="Keyword argument")
    # add argument -c
    parser.add_argument("-c", type=str, help="Category argument")
    args = parser.parse_args()

    if args.c == "all":
        for key in byCategory:
            # msg start scraping to webhook
            content_start = f"start scraping {key} category"
            send_webhook_message(webhook_url, content_start)
            cat_list = byCategory[key]["lis_category"]
            cat_name = byCategory[key]["cat"]
            datatable = byCategory[key]["datatable"]
            data = getCat(cat_name, cat_list, datatable)
            content_start = f"scraping {key} category done total {len(data)} data"
            send_webhook_message(
                webhook_url,
                content_start,
            )

    if args.k == "all":
        for key in byKeyword:
            allProduct = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                results = executor.map(work, byKeyword[key]["list_keywords"])
                allProduct += [
                    item for sublist in results for item in sublist
                ]  # Flatten list of lists
            df = pd.DataFrame(allProduct)
            df.to_csv(f"{key}_data.csv", index=False)
    elif args.k in byKeyword:
        allProduct = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = executor.map(
                work,
                byKeyword[args.k]["list_keywords"],
                [byKeyword[args.k]["datatable"]]
                * len(byKeyword[args.k]["list_keywords"]),
            )
            allProduct += [
                item for sublist in results for item in sublist
            ]  # Flatten list of lists
        # save as json
        with io.open(f"{args.k}_data.json", "w", encoding="utf-8") as f:
            json.dump(allProduct, f, ensure_ascii=False, indent=4)
        df = pd.DataFrame(allProduct)
        df.to_csv(f"{args.k}_data.csv", index=False)
    else:
        print(f"No keywords found for {args.k}")

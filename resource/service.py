import io
import pandas as pd
from task import *
from resource.utils import *
from resource.allreq import *
import concurrent.futures
import argparse
from push import *


def proccessData(data):
    try:
        data = json.dumps(data)
        data = json.loads(data)
        product = data
        url = product["url"]
        product_link = url
        # replace https://www.tokopedia.com/ with ''
        url = url.replace("https://www.tokopedia.com/", "")
        # remove ?extParam= ke belakang
        url = url.split("?extParam")[0]
        product_title = product["name"]
        shopDomain = url.split("/")[0]
        productKey = url.split("/")[1]
        detailData = getDetailProduct(shopDomain, productKey)
        if detailData is None:
            return None
        detailData = json.dumps(detailData)
        detailData = json.loads(detailData)
        detailData = detailData[0]
        shopid = detailData["data"]["pdpGetLayout"]["basicInfo"]["shopID"]
        # print(shopid)
        itemid = detailData["data"]["pdpGetLayout"]["basicInfo"]["id"]
        # set brand to null
        brand = None
        price = detailData["data"]["pdpGetLayout"]["components"][3]["data"][0]["price"][
            "value"
        ]
        rating = detailData["data"]["pdpGetLayout"]["basicInfo"]["stats"]["rating"]
        historical_sold = detailData["data"]["pdpGetLayout"]["basicInfo"]["txStats"][
            "countSold"
        ]
        review_count = detailData["data"]["pdpGetLayout"]["basicInfo"]["stats"][
            "countReview"
        ]
        view_count = detailData["data"]["pdpGetLayout"]["basicInfo"]["stats"][
            "countView"
        ]
        finalObj = {
            "marketplace": "tokopedia",
            "itemid": itemid,
            "shopid": shopid,
            "product_link": product_link,
            "product_title": product_title,
            "brand": brand,
            "price": price,
            "rating": rating,
            "historical_sold": historical_sold,
            "review_count": review_count,
            "view_count": view_count,
        }
        return finalObj
    except TypeError:
        return None


def addAdditionalData(data, keyword, product):
    try:
        _product = json.dumps(product)
        _product = json.loads(_product)
        # print(product)
        try:
            store_type = _product["shop"]["isOfficial"]
            store_location = _product["shop"]["city"]
        except KeyError:
            store_type = _product["shop"]["official"]
            store_location = _product["shop"]["location"]
        store_name = _product["shop"]["name"]
        store_link = _product["shop"]["url"]

        if (
            store_type == "true"
            or store_type == True
            or store_type == 1
            or store_type == "1"
            or store_type == "True"
            or store_type == "TRUE"
        ):
            store_type = True
        else:
            # set store type to numeric 0
            store_type = False
        data["cat_slug"] = keyword
        data["store_type"] = store_type
        data["datescrap"] = datetime.datetime.now().strftime("%Y-%m-%d")
        data["store_name"] = store_name
        data["store_link"] = store_link
        data["store_location"] = store_location

        return data
    except TypeError:
        print("Error")
        return None


def processProduct(product, keyword):
    processed_data = proccessData(product)
    # print(processed_data)

    if processed_data is None:
        return None

    return addAdditionalData(processed_data, keyword, product)


def getLstProduct(keyword, datatable):
    print("Getting product for keyword:", keyword)
    allProduct = []
    stopPage = False
    page = 1
    while not stopPage:
        lst = json.dumps(getListProduct(keyword, page))
        lst = json.loads(lst)
        lst = lst["data"]["ace_search_product_v4"]
        if lst["header"]["totalData"] == 0:
            print("No product found for keyword:", keyword)
            print(lst["header"]["totalData"])
            stopPage = True
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            result = list(
                executor.map(
                    processProduct,
                    lst["data"]["products"],
                    [keyword] * len(lst["data"]["products"]),
                )
            )
        allProduct += [product for product in result if product is not None]
        # filter result if not None
        result = [product for product in result if product is not None]
        print("Getting page:", page)
        if not stopPage:  # Only increase the page if we have not reached the last page
            page += 1
            insert_rows_no_convert(result, datatable)
            print("Page:" + str(page) + "done")

        # filter if itemid null or "" or None
        allProduct = [
            product
            for product in allProduct
            if product["itemid"] is not None and product["itemid"] != ""
        ]
    return allProduct


def getCat(cat, list_cat, datatable):
    url_to_scrap = []
    catList = getCategory()
    catList = json.dumps(catList)
    catList = json.loads(catList)
    allResult = []

    df = pd.read_csv("mapping/catmapping.csv")
    filtered_df = df[df[cat].isin(list_cat)].copy()

    for index, row in filtered_df.iterrows():
        level_1_id = row["cat1_id"]
        level_2_id = row["cat2_id"]
        level_3_id = row["cat3_id"]

        for cat_lvl1 in catList:
            if cat_lvl1["id"] == level_1_id:
                for cat_lvl2 in cat_lvl1["children"]:
                    if cat_lvl2["id"] == level_2_id:
                        for cat_lvl3 in cat_lvl2["children"]:
                            if cat_lvl3["id"] == level_3_id:
                                obj = {
                                    # cat slug cat_lvl1["name"]+"-"+cat_lvl2["name"]+"-"+cat_lvl3["name"]
                                    "cat_slug": cat_lvl1["name"]
                                    + "-"
                                    + cat_lvl2["name"]
                                    + "-"
                                    + cat_lvl3["name"],
                                    "url": cat_lvl3["url"],
                                    "cat_lvl3_id": cat_lvl3["id"],
                                }
                                url_to_scrap.append(obj)
    print("Total url to scrap:", len(url_to_scrap))

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(
            process_url,
            url_to_scrap,
            [allResult] * len(url_to_scrap),
            [datatable] * len(url_to_scrap),
        )

    return allResult


def process_url(url, allResult, datatable):
    print("Url to scrap:", url["url"])
    page = 1
    stopPage = False
    while not stopPage:
        print("All result:", len(allResult))
        detail = getListProductCat(url["cat_lvl3_id"], page)
        if detail["data"]["CategoryProducts"]["count"] == 0:
            print("No product found for category:", url["cat_slug"])
            print(detail["data"]["CategoryProducts"]["count"])
            stopPage = True
        # save detail to json
        product = json.dumps(detail)
        product = json.loads(product)
        product = product["data"]["CategoryProducts"]["data"]
        result = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            processed_products = list(
                executor.map(processProduct, product, [url["cat_slug"]] * len(product))
            )
            result += [p for p in processed_products if p is not None]

        allResult += [p for p in result if p is not None]
        print("Page:" + str(page) + " done")
        if not stopPage:
            page += 1
            insert_rows_no_convert(result, datatable)

        # filter if itemid null or "" or None
        allResult = [
            p for p in allResult if p["itemid"] is not None and p["itemid"] != ""
        ]

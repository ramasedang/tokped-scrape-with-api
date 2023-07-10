import requests
import sys
from urllib.parse import quote
import random
import json
import urllib
import io
import datetime
import re
from resource.utils import *
import time


def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]
    random_index = random.randint(0, len(user_agents) - 1)

    return user_agents[random_index]


def getCookies(max_retries=3):
    userAgents = random_user_agent()
    headers = {
        "authority": "www.tokopedia.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.6",
        "cache-control": "max-age=0",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": userAgents,
    }

    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(
                "https://www.tokopedia.com/", headers=headers, timeout=5
            )
            cookies = response.cookies
            return cookies
        except ConnectionError as e:
            print(f"Connection error occurred: {e}")
            print(f"Retrying ({retries + 1}/{max_retries})...")
            retries += 1

    print("Max retries exceeded. Unable to establish a connection.")
    return None


def getListProduct(keyword, page):
    if int(page) == 1:
        start = 0
    else:
        start = (int(page) - 1) * 200

    headers = {
        "Tkpd-UserId": "10731773",
        "X-Version": "6730998",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": random_user_agent(),
        "content-type": "application/json",
        "accept": "*/*",
        "Referer": "https://www.tokopedia.com/",
        "X-Source": "tokopedia-lite",
        "x-device": "desktop-0.0",
        "X-Tkpd-Lite-Service": "zeus",
        "sec-ch-ua-platform": '"Windows"',
    }

    json_data = [
        {
            "operationName": "SearchProductQueryV4",
            "variables": {
                "params": f"device=desktop&navsource=&ob=23&page=P{page}&q={quote(keyword)}&related=true&rows=200&safe_search=false&scheme=https&shipping=&show_adult=false&source=search&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&start={start}&topads_bucket=true&unique_id=2a84016eeb7220f769135a8dee41e1b8&user_addressId=194047705&user_cityId=252&user_districtId=3534&user_id=10731773&user_lat=-7.294156364632453&user_long=112.80760947614907&user_postCode=60111&user_warehouseId=0&variants=&warehouses=0%232h%2C0%2315m"
            },
            "query": "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      componentId\n      __typename\n    }\n    data {\n      banner {\n        position\n        text\n        imageUrl\n        url\n        componentId\n        trackingOption\n        __typename\n      }\n      backendFilters\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        componentId\n        trackingOption\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        position\n        trackingOption\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              adsId: id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            badges {\n              title\n              imageUrl\n              show\n              __typename\n            }\n            ratingAverage\n            labelGroups {\n              position\n              type\n              title\n              url\n              __typename\n            }\n            componentId\n            __typename\n          }\n          componentId\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        componentId\n        trackingOption\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          adsId: id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        customVideoURL\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          url\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        ratingAverage\n        shop {\n          shopId: id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        }
    ]
    cookies = getCookies()

    response = post_request_with_retry2(
        "https://gql.tokopedia.com/graphql/SearchProductQueryV4",
        headers=headers,
        payload=json_data,
        cookieJar=cookies,
    )

    json_str = json.dumps(response)
    data = json.loads(json_str)
    data = data[0]
    # print(data)
    return data


def post_request_with_retry2(url, headers, payload, cookieJar):
    cookies = cookieJar
    for i in range(4):
        session = requests.Session()
        try:
            time.sleep(random.randint(1, 2))
            response = session.post(
                url, headers=headers, json=payload, timeout=3, cookies=cookies
            )
            response.raise_for_status()
            return json.loads(response.text)
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError):
            print(f"Timeout on attempt {i+1}")
            cookies = getCookies()
            time.sleep(2)  # Wait for 5 seconds before retrying
            print(f"Retrying attempt {i+1}...")
        except Exception as e:
            print("An error occurred:", e)
            break
        finally:
            session.close()
    print("Failed to get detail product after 5 retries.")
    return None


def post_request_with_retry(url, headers, payload, productKey, cookieJar):
    cookies = cookieJar
    for i in range(5):
        session = requests.Session()
        try:
            time.sleep(random.randint(1, 2))
            response = session.post(
                url, headers=headers, data=payload, timeout=3, cookies=cookies
            )
            response.raise_for_status()
            return json.loads(response.text)
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError):
            print(f"Timeout on attempt {i+1}: {productKey}")
            cookies = getCookies()
            time.sleep(2)  # Wait for 5 seconds before retrying
            print(f"Retrying attempt {i+1}...")
        except Exception as e:
            print("An error occurred:", e)
            break
        finally:
            session.close()
    print("Failed to get detail product after 5 retries.")
    return None


def commonGet(url):
    headers = {"User-Agent": random_user_agent()}

    response = requests.get(url, headers=headers)
    # save to file
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(response.text)


def getCategory():
    url = "https://gql.tokopedia.com/graphql/headerMainData"

    payload = json.dumps(
        [
            {
                "operationName": "headerMainData",
                "variables": {},
                "query": "query headerMainData {\n  dynamicHomeIcon {\n    categoryGroup {\n      id\n      title\n      desc\n      categoryRows {\n        id\n        name\n        url\n        imageUrl\n        type\n        categoryId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  categoryAllListLite {\n    categories {\n      id\n      name\n      url\n      iconImageUrl\n      isCrawlable\n      children {\n        id\n        name\n        url\n        isCrawlable\n        children {\n          id\n          name\n          url\n          isCrawlable\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
            }
        ]
    )

    headers = {
        "User-Agent": random_user_agent(),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.tokopedia.com/",
        "X-Tkpd-Lite-Service": "zeus",
        "X-Version": "a61214f",
        "content-type": "application/json",
        "x-device": "desktop-0.0",
        "X-Source": "tokopedia-lite",
        "Origin": "https://www.tokopedia.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers",
    }

    retries = 3  # Number of retries
    timeout = 5  # Request timeout in seconds

    for attempt in range(retries):
        try:
            response = requests.post(
                url, headers=headers, data=payload, timeout=timeout
            )
            response.raise_for_status()
            break  # Successful request, exit the loop
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                # Sleep for 1 second before retrying
                time.sleep(1)
                continue
            else:
                # Handle the case when all retries fail
                print("Failed to retrieve data after multiple attempts.")
                return None

    resjson = json.dumps(response.json(), indent=4, ensure_ascii=False)
    # get first array index
    resjson = json.loads(resjson)[0]
    # get data key
    resjson = resjson["data"]["categoryAllListLite"]["categories"]
    #
    return resjson


def getDetailProduct(shopDomain, productKey):
    url = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"
    cookies = getCookies()

    payload = json.dumps(
        [
            {
                "operationName": "PDPGetLayoutQuery",
                "variables": {
                    "shopDomain": shopDomain,
                    "productKey": productKey,
                    "layoutID": "",
                    "apiVersion": 1,
                    "tokonow": {
                        "shopID": "11530573",
                        "whID": "12210375",
                        "serviceType": "2h",
                    },
                    "userLocation": {
                        "cityID": "176",
                        "addressID": "0",
                        "districtID": "2274",
                        "postalCode": "",
                        "latlon": "",
                    },
                    "extParam": "ivf%3Dtrue",
                },
                "query": "fragment ProductVariant on pdpDataProductVariant {\n  errorCode\n  parentID\n  defaultChild\n  sizeChart\n  totalStockFmt\n  variants {\n    productVariantID\n    variantID\n    name\n    identifier\n    option {\n      picture {\n        urlOriginal: url\n        urlThumbnail: url100\n        __typename\n      }\n      productVariantOptionID\n      variantUnitValueID\n      value\n      hex\n      stock\n      __typename\n    }\n    __typename\n  }\n  children {\n    productID\n    price\n    priceFmt\n    optionID\n    optionName\n    productName\n    productURL\n    picture {\n      urlOriginal: url\n      urlThumbnail: url100\n      __typename\n    }\n    stock {\n      stock\n      isBuyable\n      stockWordingHTML\n      minimumOrder\n      maximumOrder\n      __typename\n    }\n    isCOD\n    isWishlist\n    campaignInfo {\n      campaignID\n      campaignType\n      campaignTypeName\n      campaignIdentifier\n      background\n      discountPercentage\n      originalPrice\n      discountPrice\n      stock\n      stockSoldPercentage\n      startDate\n      endDate\n      endDateUnix\n      appLinks\n      isAppsOnly\n      isActive\n      hideGimmick\n      isCheckImei\n      minOrder\n      __typename\n    }\n    thematicCampaign {\n      additionalInfo\n      background\n      campaignName\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMedia on pdpDataProductMedia {\n  media {\n    type\n    urlOriginal: URLOriginal\n    urlThumbnail: URLThumbnail\n    urlMaxRes: URLMaxRes\n    videoUrl: videoURLAndroid\n    prefix\n    suffix\n    description\n    variantOptionID\n    __typename\n  }\n  videos {\n    source\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCategoryCarousel on pdpDataCategoryCarousel {\n  linkText\n  titleCarousel\n  applink\n  list {\n    categoryID\n    icon\n    title\n    isApplink\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    __typename\n  }\n  campaign {\n    campaignID\n    campaignType\n    campaignTypeName\n    campaignIdentifier\n    background\n    percentageAmount\n    originalPrice\n    discountedPrice\n    originalStock\n    stock\n    stockSoldPercentage\n    threshold\n    startDate\n    endDate\n    endDateUnix\n    appLinks\n    isAppsOnly\n    isActive\n    hideGimmick\n    __typename\n  }\n  thematicCampaign {\n    additionalInfo\n    background\n    campaignName\n    icon\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  variant {\n    isVariant\n    parentID\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n  isCashback {\n    percentage\n    __typename\n  }\n  isTradeIn\n  isOS\n  isPowerMerchant\n  isWishlist\n  isCOD\n  preorder {\n    duration\n    timeUnit\n    isActive\n    preorderInDays\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCustomInfo on pdpDataCustomInfo {\n  icon\n  title\n  isApplink\n  applink\n  separator\n  description\n  __typename\n}\n\nfragment ProductInfo on pdpDataProductInfo {\n  row\n  content {\n    title\n    subtitle\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetail on pdpDataProductDetail {\n  content {\n    title\n    subtitle\n    applink\n    showAtFront\n    isAnnotation\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDataInfo on pdpDataInfo {\n  icon\n  title\n  isApplink\n  applink\n  content {\n    icon\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment ProductSocial on pdpDataSocialProof {\n  row\n  content {\n    icon\n    title\n    subtitle\n    applink\n    type\n    rating\n    __typename\n  }\n  __typename\n}\n\nquery PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow) {\n  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow) {\n    requestID\n    name\n    pdpSession\n    basicInfo {\n      alias\n      createdAt\n      isQA\n      id: productID\n      shopID\n      shopName\n      minOrder\n      maxOrder\n      weight\n      weightUnit\n      condition\n      status\n      url\n      needPrescription\n      catalogID\n      isLeasing\n      isBlacklisted\n      isTokoNow\n      menu {\n        id\n        name\n        url\n        __typename\n      }\n      category {\n        id\n        name\n        title\n        breadcrumbURL\n        isAdult\n        isKyc\n        minAge\n        detail {\n          id\n          name\n          breadcrumbURL\n          isAdult\n          __typename\n        }\n        __typename\n      }\n      txStats {\n        transactionSuccess\n        transactionReject\n        countSold\n        paymentVerified\n        itemSoldFmt\n        __typename\n      }\n      stats {\n        countView\n        countReview\n        countTalk\n        rating\n        __typename\n      }\n      __typename\n    }\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductMedia\n        ...ProductHighlight\n        ...ProductInfo\n        ...ProductDetail\n        ...ProductSocial\n        ...ProductDataInfo\n        ...ProductCustomInfo\n        ...ProductVariant\n        ...ProductCategoryCarousel\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
            }
        ]
    )
    headers = {
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
        "X-Version": "f2616c7",
        "X-TKPD-AKAMAI": "pdpGetLayout",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": random_user_agent(),
        "content-type": "application/json",
        "accept": "*/*",
        "Referer": "https://www.tokopedia.com/",
        "X-Source": "tokopedia-lite",
        "x-device": "desktop",
        "X-Tkpd-Lite-Service": "zeus",
        "sec-ch-ua-platform": '"Windows"',
    }
    response = post_request_with_retry(url, headers, payload, productKey, cookies)
    # print("OK! " + productKey)
    response = json.dumps(response)
    response = json.loads(response)
    return response


def getListProductCat(cat_lvl3_id, page):
    cookie = getCookies()
    url = "https://gql.tokopedia.com/graphql/SearchProductQuery"
    if page == 1:
        start = 1
    else:
        start = (page - 1) * 60 + 1
    payload = json.dumps(
        [
            {
                "operationName": "SearchProductQuery",
                "variables": {
                    "params": f"page={page}&ob=&sc={cat_lvl3_id}&user_id=0&rows=60&start={start}&source=directory&device=desktop&page={page}&related=true&st=product&safe_search=false",
                    "adParams": "",
                },
                "query": "query SearchProductQuery($params: String, $adParams: String) {\n  CategoryProducts: searchProduct(params: $params) {\n    count\n    data: products {\n      id\n    name\n     url\n      imageUrl: image_url\n      imageUrlLarge: image_url_700\n      catId: category_id\n      gaKey: ga_key\n      countReview: count_review\n      discountPercentage: discount_percentage\n      preorder: is_preorder\n      name\n      price\n      priceInt: price_int\n      original_price\n      rating\n      wishlist\n      labels {\n        title\n        color\n        __typename\n      }\n      badges {\n        imageUrl: image_url\n        show\n        __typename\n      }\n      shop {\n        id\n        url\n        name\n        goldmerchant: is_power_badge\n        official: is_official\n        reputation\n        clover\n        location\n        __typename\n      }\n      labelGroups: label_groups {\n        position\n        title\n        type\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  displayAdsV3(displayParams: $adParams) {\n    data {\n      id\n      ad_ref_key\n      redirect\n      sticker_id\n      sticker_image\n      productWishListUrl: product_wishlist_url\n      clickTrackUrl: product_click_url\n      shop_click_url\n      product {\n        id\n        name\n        wishlist\n        image {\n          imageUrl: s_ecs\n          trackerImageUrl: s_url\n          __typename\n        }\n        url: uri\n        relative_uri\n        price: price_format\n        campaign {\n          original_price\n          discountPercentage: discount_percentage\n          __typename\n        }\n        wholeSalePrice: wholesale_price {\n          quantityMin: quantity_min_format\n          quantityMax: quantity_max_format\n          price: price_format\n          __typename\n        }\n        count_talk_format\n        countReview: count_review_format\n        category {\n          id\n          __typename\n        }\n        preorder: product_preorder\n        product_wholesale\n        free_return\n        isNewProduct: product_new_label\n        cashback: product_cashback_rate\n        rating: product_rating\n        top_label\n        bottomLabel: bottom_label\n        __typename\n      }\n      shop {\n        image_product {\n          image_url\n          __typename\n        }\n        id\n        name\n        domain\n        location\n        city\n        tagline\n        goldmerchant: gold_shop\n        gold_shop_badge\n        official: shop_is_official\n        lucky_shop\n        uri\n        owner_id\n        is_owner\n        badges {\n          title\n          image_url\n          show\n          __typename\n        }\n        __typename\n      }\n      applinks\n      __typename\n    }\n    template {\n      isAd: is_ad\n      __typename\n    }\n    __typename\n  }\n}\n",
            }
        ]
    )
    headers = {
        "Tkpd-UserId": "0",
        "X-Version": "1423eab",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": random_user_agent(),
        "iris_session_id": "",
        "content-type": "application/json",
        "accept": "*/*",
        "Referer": "https://www.tokopedia.com",
        "X-Source": "tokopedia-lite",
        "x-device": "desktop-0.0",
        "X-Tkpd-Lite-Service": "zeus",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = post_request_with_retry(url, headers, payload, cat_lvl3_id, cookie)

    return response[0]


if __name__ == "__main__":
    getDetailProduct(
        "nutriologyindonesia",
        "granola-real-honey-400-gr-nutriology-sereal-makanan-sehat-diet-praktis-apple-cinnamon",
    )

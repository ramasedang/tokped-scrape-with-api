from db_page import page_engine, Session, Shopee_Page
from google.cloud import bigquery
import os
from datetime import datetime
# here is bigquery sender
# shopee sender
data_name   = 'pinkrabbit' 
table_name  = 'digitalocean'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{BASE_DIR}/data/key.json"
client = bigquery.Client()
table_id = f"profound-surge-368421.{data_name}.{table_name}"

def all_to_all(row):
    errors = client.insert_rows_json(table_id, row)  # Make an API request.
    if errors == []:
        print(f"New rows have been added")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))




# make chunk
def chunks(split,n) -> int:
    cunk = n//split
    split_range = list(range(0,(cunk*split)+split,split))
    cunkr = [[i+1,((count+1)*split)] for count,i in enumerate(split_range)]
    cunkr[-1][1] = (cunkr[-1][0] - 1) + n%split
    return cunkr

def get_chunks(terval_a,terval_b):
    kueri_data = f"""SELECT a.marketplace, a.cat_slug, a.itemid, a.shopid, a.product_title, a.product_link, a.brand, a.store_type, b.store_name, b.store_link, b.store_location, a.historical_sold, a.review_count,
                    a.view_count, a.price, a.rating
                    FROM
                    (SELECT *
                    FROM shopee_page
                    WHERE ROWID BETWEEN {terval_a} AND {terval_b}) as a
                    LEFT JOIN 
                    (SELECT shopid, store_name, store_link, store_location FROM shopee_seller) as b
                    ON a.shopid = b.shopid"""
    with Session(bind = page_engine) as local_session:
        local_session.begin()
        try:
            df_chunk = local_session.execute(kueri_data).all()
            df_chunk = [dict(data._mapping) for data in df_chunk]
        except:
            local_session.rollback()
            raise
        else:
            return df_chunk

def shopee_chunks_query(tanggal) -> str:
    kueri_n = f"""SELECT COUNT(itemid) as n FROM shopee_page"""
    with Session(bind = page_engine) as local_session:
        local_session.begin()
        try:
            result = local_session.execute(kueri_n).all()
            # result = [dict(data._mapping) for data in result]
            result = result[0][0]
        except:
            local_session.rollback()
            raise
        else:
            local_session.commit()
            print(result)
        
    for terval in chunks(100,result):
        print(f"terval_a:{terval[0]} - terval_b: {terval[1]}")
        hs = get_chunks(terval_a=terval[0],terval_b=terval[1])
        for item in hs:
            item['datescrap'] = tanggal
        all_to_all(hs)
        # print(hs)

if __name__ == '__main__':
    shopee_chunks_query(tanggal=str(datetime.today().date()))

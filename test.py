from resource.service import *
from task import *
import pandas as pd

if __name__ == "__main__":
    cat_list = byCategory["perawatandankecantikan"]["lis_category"]
    cat_name = byCategory["perawatandankecantikan"]["cat"]
    datatable = byCategory["perawatandankecantikan"]["datatable"]
    data = getCat(cat_name, cat_list, datatable)
    print(data)

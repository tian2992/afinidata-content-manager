import os
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'content_manager.production')

import django
django.setup()

import logging

import posts.models
from posts.models import Post, Taxonomy

import gspread_pandas
from gspread_pandas import Spread


def fix_date_post_from_dataframe(post: Post, df):
    try:
        min_r = post.min_range
        max_r = post.max_range
        mess = df["meses"]
        reg = r"(\d+)\s*-\s*(\d+).*"
        meses_search = re.search(reg, mess)
        min_d_val = int(meses_search.group(1))
        max_d_val = int(meses_search.group(2))
        if abs(min_r - min_d_val) > 0 or abs(max_r-max_d_val) > 0:
            post.min_range = min_d_val
            post.max_range = max_d_val
            post.save()
            print(f"Fixed post {post.pk} for a date difference {min_r} - {min_d_val}, {max_r}-{max_d_val}")
        else:
            print(f"Not changed dates for {post.pk}")
    except:
        logging.exception("error when setting age ranges to post, key")


def load_taxo():
    from posts.models import Area, Subarea, Componente
    areas = dict([(are.name, are) for are in Area.objects.all()])
    sub = dict([(s.name, s) for s in Subarea.objects.all()])
    com = dict([(c.name, c) for c in Componente.objects.all()])

    print(sub)
    print(com)
    return {"are": areas,
            "sub": sub,
            "com": com}


TAX = load_taxo()


def fix_taxonomy_post_from_dataframe(post: Post, df):
    try:
        are = df["ÁREA"].strip()
        sub = df["SUB-ÁREA"].strip()
        com = df["COMPONENTE"].strip()
        if are not in TAX["are"]:
            print(f"FUCK THIS! {post.id} - {are}")
        if sub not in TAX["sub"]:
            print(f"FUCK DAT! {post.id} - {sub}")
        if com not in TAX["com"]:
            print(f"FUCK DEM! {post.id} - {com}")

        try:
            taxo = post.taxonomy
        except:
            logging.exception("taxono")
            t = Taxonomy(post_id=post.id, area=TAX["are"][are], subarea=TAX["sub"][sub], component=TAX["com"][com])
            t.save()
            taxo = post.taxonomy

        #print(post.taxonomy)

    except:
        logging.exception("error when setting age ranges to post, key")


def diff_post_dataframe(post: Post, df):
    min_r = post.min_range
    max_r = post.max_range
    mess = df["meses"]
    reg = r"(-?\d+)\s*-\s*(-?\d+).*"
    meses_search = re.search(reg, mess)
    min_d_val = int(meses_search.group(1))
    max_d_val = int(meses_search.group(2))
    # print(df)
    # print(f"min- {min_r} === {min_d_val}")
    # print(f"max- {max_r} === {max_d_val}")
    return (min_r - min_d_val, max_r-max_d_val)

s = Spread("https://docs.google.com/spreadsheets/d/1EfS2W11kRg2C1H6KD2vVjR_Htvy6j7C4SSGHPA8Bvpc/edit?ts=5d22a555",
           sheet="Base de Datos")
df = s.sheet_to_df()


STATUS_CHOICES = ['draft', 'review', 'rejected', 'need_changes', 'published']

lim = 0

for k, da in df.iterrows():
    if False and lim > 15:
        break
    else:
        lim += 1

    print("-----------------")
    if da["STATUS"] == 'rejected':
        continue
    try:
       post = Post.objects.get(id=k)   #id=da["POST ID"])   # id=k
       # print("====")
       # print(fix_date_post_dataframe(post, da))
       print(fix_taxonomy_post_from_dataframe(post, da))

    except Exception as e:
        logging.exception(f"broken on key {k} - {da}")
        pass

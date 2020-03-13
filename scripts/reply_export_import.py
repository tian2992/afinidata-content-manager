import gspread_pandas
from django.forms.models import model_to_dict

from gspread_pandas import Spread
from pandas import DataFrame
from datetime import datetime

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'content_manager.production')

import django
# django.setup()

def get_replies():
    from reply_repo.models import Message
    messages = Message.objects.all()
    return messages


def df_from_replies(reps_m):
    l = []
    for rep in reps_m:
        l.append(model_to_dict(rep))
    return DataFrame(l)


def dump_replies(sp_url, l_df):
    spread = Spread(sp_url)
    spread.df_to_sheet(l_df, index=True, sheet=f"Dump {datetime.now()}")
    return spread


def run_dump(sheet_url):
    rps = get_replies()
    df = df_from_replies(rps)
    return dump_replies(sheet_url, df)


def run_up(sheet_url):
    sh = parse_sheet(sheet_url)
    return amek_replies(sh)


def parse_sheet(sheet_url):
    '''from a gsheet return a pandas df'''
    s = Spread(sheet_url,
               sheet=0)
    df = s.sheet_to_df()
    return df


def amek_replies(reply_df):
    '''Adds replies to DB'''
    import json
    from reply_repo.models import Message
    added = 0
    edited = 0

    for i, row in reply_df.iterrows():
        if row.id:
            print(f"updating row {i}")
            r = dict(row)
            del r["id"]
            m, cre = Message.objects.update_or_create(block_id=row.block_id, language=row.language, defaults=dict(row))
            if cre:
                added += 1
            else:
                edited += 1
        else:
            print(f"new row {i}")
            extra_items = row.extra_items
            try:
                json.loads(extra_items)
            except:
                print("error on extra items")
                extra_items = "{}"
            m = Message(block_id=row.block_id, language=row.language, full_locale=row.full_locale,
                                state=row.state, content=row.content, extra_items=extra_items)
            m.save()
            added += 1
    return {"added": added, "edited": edited}
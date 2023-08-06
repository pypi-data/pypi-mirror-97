#!/usr/bin/env python3
import argparse
import json
import logging
from . import Whatsapp

from .osd2futils import jsonlines_to_osd2f


parser = argparse.ArgumentParser()
parser.add_argument("--geckopath", help="Path to your gecko driver (necessary if not in $PATH)")
parser.add_argument("--blur", action="store_true")
parser.add_argument("--verbose", "-v", help="Verbose (debug) output", action="store_true")
parser.add_argument("--max-chats", help="Maximum number of chats to scrape", type=int)
parser.add_argument("--keep-open", help="Keep browser open (for debugging)", action="store_true")
parser.add_argument("--max-days", help="maximum number of days to be scraped", type=int, default=90)

args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                    format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')
myscraper = Whatsapp(geckopath=args.geckopath, days = args.max_days)
try:
    myscraper.wait_to_be_ready()
    if args.blur:
        myscraper.blur()
    for i, chat in enumerate(myscraper.get_all_chats()):
        if args.max_chats and i >= args.max_chats:
            break
        logging.info(f"Getting links from {chat.text}")
        for link in myscraper.get_links_per_chat(chat):
            print(json.dumps(link))
finally:
    if not args.keep_open:
        myscraper.quit_browser()




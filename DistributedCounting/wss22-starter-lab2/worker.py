from dataclasses import field
import logging
from typing import Any

from base import Worker
from mrds import MyRedis
from collections import Counter, defaultdict


class WcWorker(Worker):
    def serialize_dict(self, words):
        array = []
        for word, count in words.items():
            array.append(word)
            array.append(count)
        return array
    
    def run(self, **kwargs: Any) -> None:
        rds: MyRedis = kwargs['rds']
        myfilecount = 0
        # run till there are files remaining
        while True:
            filename, file_id = rds.get_file(self.name)
            if not filename:
                break
            with open(filename, "r") as file:
                words = file.read().split()
                wc = Counter(words)
                lualist = self.serialize_dict(wc)
                rds.update_words_transaction(lualist, file_id)
                # for k, v in wc.items():
                #     rds.update_words_transaction(k, v, file_id)
                myfilecount += 1

        # run till there are pending files
        while True:
            pending_tasks = rds.pending_tasks()
            print(pending_tasks)
            if pending_tasks['pending'] == 0:
                break
            filename, file_id = rds.autoclaim(self.name)
            if filename == None:
                continue
            print("CLAIMED : ", filename)
            wc = Counter(words)
            lualist = self.serialize_dict(wc)
            rds.update_words_transaction(lualist, file_id)
            # for k, v in wc.items():
            #     rds.update_words_transaction(k, v, file_id)
            myfilecount += 1

        logging.info(f"Exiting, after processing {myfilecount} file(s).")
        return wc

from dataclasses import field
import logging
from typing import Any

from base import Worker
from mrds import MyRedis
from collections import Counter, defaultdict


class WcWorker(Worker):
    def run(self, **kwargs: Any) -> None:
        rds: MyRedis = kwargs['rds']
        all_words = defaultdict(int)

        # run till there are files remaining
        while True:
            filename, file_id = rds.get_file(self.name)
            if not filename:
                break
            with open(filename, "r") as file:
                words = file.read().split()
                wc = Counter(words)
                for k, v in wc.items():
                    all_words[k] += v
                rds.ack(file_id)

        while True:
            filename, file_id = rds.autoclaim(self.name)
            if filename == None:
                break
            print("claimed : ", filename)
            wc = Counter(words)
            for k, v in wc.items():
                all_words[k] += v
            rds.ack(file_id)

        # Once all files are done, update in redis
        for k, v in all_words.items():
            rds.increment_word(k, v)

        logging.info("Exiting")
        return wc

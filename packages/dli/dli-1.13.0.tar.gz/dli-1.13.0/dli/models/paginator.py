#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import math
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock


class Paginator:

    def __init__(self, url, model,
         instantiation_method=None, instantiation_override=None,
         page=1, total_field=None, page_size=25, max_workers=10,
         filters=None
    ):
        self.page = page
        self.filters = filters
        self.page_size = page_size
        self.url = url
        self.model = model
        self.instantiation_factory = instantiation_method
        self.override = instantiation_override
        self.cache = []
        self.total_field = total_field
        self.lock = Lock()
        self.max_workers = max_workers

    def _request(self, page=None):

        params={
            'page': self.page if not page else page,
        }

        if self.filters and type(self.filters) is dict:
            params.update(self.filters)


        if self.page_size:
            params['page_size'] = self.page_size

        s = self.model._client.session.get(
            self.url,
            params=params
        )

        return s.json()

    def __iter__(self):
        if not self.cache:
            try:
                tp = ThreadPoolExecutor(max_workers=self.max_workers)

                inst = self._request()
                key = None
                if inst.get("entities", None) is not None:
                    # v1 route
                    key = "entities"
                    block = "properties"
                    count = "pages_count"
                else:
                    # v2 route
                    key = "data"
                    block = "meta"
                    count = "total_pages"

                if key:

                    def _get_and_instantiate(page):
                        inst = self._request(page)
                        self._iter_instance(inst, key)

                    self._iter_instance(inst, key)

                    if not self.total_field:
                        total_pages = inst[block][count] + 1
                    else:
                        # total field gives us how many of X
                        # so we must divide by the page_size
                        # todo this is code-debt caused by dictionary
                        # todo pagination from catalogue DL-2809
                        total_count = inst[block][self.total_field]
                        total_pages = math.ceil(total_count / self.page_size) + 1

                    rng = range(2, total_pages)

                    list(tp.map(_get_and_instantiate, rng))

            finally:
                tp.shutdown(wait=True)

        yield from self.cache

    def _iter_instance(self, inst, key):
        obj = inst if not key else inst.get(key, [])

        # we use the __init__ method of the class unless
        # (or) provided instantiation method
        # ... useful to transform data first
        # (or) provided override to control cache insertion
        # ... useful to flatten multi-item

        if not self.override:
            for f in obj:
                if not self.instantiation_factory:
                    m = self.model(f)
                else:
                    m = self.instantiation_factory(f, page_size=self.page_size)

                with self.lock:
                    self.cache.append(m)
        else:
            self.override(obj, self.cache)

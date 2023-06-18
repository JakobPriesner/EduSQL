import asyncio
import concurrent.futures
import multiprocessing


class ProcessHandler:
    __pool = None
    __waiting_tasks = 0

    @classmethod
    def get_pool(cls):
        if cls.__pool is None:
            cls.__pool = concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count())
        return cls.__pool

    @classmethod
    async def close_async(cls):
        if cls.__pool is not None:
            cls.__pool.shutdown(wait=True)

    @classmethod
    def close(cls):
        if cls.__pool is not None:
            cls.__pool.shutdown(wait=True)

    @classmethod
    async def map_async(cls, func, *iterables):
        return await asyncio.gather(*[cls.submit_async(func, item) for item in iterables[0]])

    @classmethod
    def map(cls, func, *iterables, timeout=None, chunksize=1):
        pool = cls.get_pool()
        return pool.map(func, *iterables, timeout=timeout, chunksize=chunksize)

    @classmethod
    async def submit_async(cls, func, *args):
        return await func(*args)

    @classmethod
    def submit(cls, func, *args, **kwargs):
        pool = cls.get_pool()
        return pool.submit(func, *args, **kwargs)

    @classmethod
    def wait(cls, fs, timeout=None, return_when=concurrent.futures.ALL_COMPLETED):
        if isinstance(fs, concurrent.futures.Future):
            fs = [fs]
        concurrent.futures.wait(fs, timeout=timeout, return_when=return_when)


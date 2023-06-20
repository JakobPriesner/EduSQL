import asyncio
import platform

from dotenv import load_dotenv
from injector import Injector

from api import Api
from configuration import Configuration
from generator.create_data import DataGenerator


def main():
    injector: Injector = Injector(modules=[Configuration])
    injector.binder.bind(Injector, to=injector)

    asyncio.run(injector.get(DataGenerator).create_data_if_not_exist())

    api: Api = injector.get(Api)
    try:
        api.start()
    except KeyboardInterrupt:
        pass
    finally:
        api.stop()


if __name__ == '__main__':
    load_dotenv()
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    main()

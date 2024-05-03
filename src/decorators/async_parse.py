import asyncio
import traceback
from types import FunctionType

from aiohttp import ClientSession, ClientTimeout, TCPConnector, ClientConnectorError
from fake_useragent import UserAgent


def aiohttp_timeout_receiver(timeout: int | float = 0.5):
    def decorator(func: FunctionType):
        async def wrapper(attempts=5, *args, **kwargs):
            ua = UserAgent().random
            headers = {"User-Agent": ua}

            connector = TCPConnector(verify_ssl=False, limit_per_host=10)
            t = ClientTimeout(total=float(timeout))

            session = ClientSession(trust_env=True, headers=headers, timeout=t)

            args = list(args)
            args.insert(0, session)
            args = tuple(args)
            try:
                data = await func(*args, **kwargs)
                return data
            except (TimeoutError, ClientConnectorError):
                if not attempts:
                    raise NotImplementedError('Попытки закончились')

                await asyncio.sleep(timeout + 0.5)

                await session.close()

                args = list(args)
                args.pop(0)
                args = tuple(args)

                return await wrapper(*args, **kwargs, attempts=attempts - 1)
            except Exception:
                pass

        return wrapper

    return decorator

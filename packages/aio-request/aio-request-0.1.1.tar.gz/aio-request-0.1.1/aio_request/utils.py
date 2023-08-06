import asyncio
import contextlib
from typing import Any, Callable, Collection, Dict, Mapping, Optional, Protocol, TypeVar

import multidict
import yarl

EMPTY_HEADERS = multidict.CIMultiDictProxy[str](multidict.CIMultiDict[str]())


class Closable(Protocol):
    async def close(self) -> None:
        ...


TClosable = TypeVar("TClosable", bound=Closable)


async def _close(item: TClosable) -> None:
    with contextlib.suppress(Exception):
        await item.close()


T = TypeVar("T")


async def close_futures(items: Collection[asyncio.Future[T]], as_close: Callable[[T], TClosable]) -> None:
    for item in items:
        if item.cancelled():
            continue
        try:
            await _close(as_close(await item))
        except asyncio.CancelledError:
            if not item.cancelled():
                raise


async def close(items: Collection[TClosable]) -> None:
    for item in items:
        await _close(item)


async def cancel_futures(futures: Collection[asyncio.Future[T]]) -> None:
    for future in futures:
        if future.done():
            continue
        future.cancel()


def substitute_path_parameters(url: yarl.URL, parameters: Optional[Mapping[str, str]] = None) -> yarl.URL:
    if not parameters:
        return url

    path = url.path
    for name, value in parameters.items():
        path = path.replace(f"{{{name}}}", value)

    build_parameters: Dict[str, Any] = dict(
        scheme=url.scheme,
        user=url.user,
        password=url.password,
        host=url.host,
        port=url.port,
        path=path,
        query=url.query,
        fragment=url.fragment,
    )

    return yarl.URL.build(**{k: v for k, v in build_parameters.items() if v is not None})

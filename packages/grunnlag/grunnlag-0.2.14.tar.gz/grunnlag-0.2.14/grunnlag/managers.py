from bergen.types.model import ArnheimAsyncModelManager, ArnheimModelManager
from concurrent.futures import ThreadPoolExecutor
import asyncio
class RepresentationManager(ArnheimModelManager["Representation"]):

    def from_xarray(self, array, compute=True, **kwargs):
        instance = self.create(**kwargs)
        instance.save_array(array, compute=compute)
        print(instance)
        instance = self.update(id=instance.id, **kwargs)
        return instance


class AsyncRepresentationManager(ArnheimAsyncModelManager["Representation"]):

    async def from_xarray(self, array, compute=True, **kwargs):
        instance = await self.create(**kwargs)
        with ThreadPoolExecutor(max_workers=1) as executor:
            co_future = executor.submit(instance.save_array, array, compute=True)
            await asyncio.wrap_future(co_future)    
        instance = await self.update(id=instance.id, **kwargs)
        return instance
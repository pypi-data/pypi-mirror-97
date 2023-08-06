from bergen.registries.arnheim import get_current_arnheim
import os
import s3fs
import xarray as xr


class Array:

    def _getZarrStore(self):
        settings = get_current_arnheim().getExtensions("elements")
        s3_protocol = "http:"
        endpoint_url = s3_protocol + "//" + settings["path"]

        os.environ["AWS_ACCESS_KEY_ID"] = settings["params"]["access_key"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = settings["params"]["secret_key"]

        s3_path = f"zarr/{self.store}"
        store = s3fs.S3FileSystem(client_kwargs={"endpoint_url": endpoint_url})
        return store.get_mapper(s3_path)


    @property
    def data(self) -> xr.DataArray:
        return xr.open_zarr(store=self._getZarrStore(), consolidated=True)["data"]


    def save_array(self, array: xr.DataArray, compute=True):
        apiversion = "0.1"
        fileversion = "0.1"

        if apiversion == "0.1":
            dataset = array.to_dataset(name="data")
            dataset.attrs["apiversion"] = apiversion
            dataset.attrs["fileversion"] = fileversion
            if fileversion == "0.1":
                dataset.attrs["model"] = str(self.Meta.identifier)
                dataset.attrs["unique"] = str(self.unique)
            else:
                raise NotImplementedError("This FileVersion has not been Implemented yet")
        else:
            raise NotImplementedError("This API Version has not been Implemented Yet")

        return dataset.to_zarr(store=self._getZarrStore(), consolidated=True, compute=compute)








class RepresentationPrettifier:
    ''' Just a little helper to make our User look nicer in Jupyter Notebooks'''

    def _repr_html_(self):
        string = f"{self.name}</br>"
        if self.image is not None:
            string += f"<img src='{self.image}' alt='representationimage' height=100 width=100></img>"
        if self.data is not None:
            string += self.data._repr_html_()
        
        return string
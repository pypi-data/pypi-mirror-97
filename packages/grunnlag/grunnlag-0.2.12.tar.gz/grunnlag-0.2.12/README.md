# Grunnlag

### Idea

Grunnlag is a Schema Provider for the Bergen Client accessing your Arnheim Framework
 
### Prerequisites

Bergen (and in Conclusion Grunnlag) only works with a running Arnheim Instance (in your network or locally for debugging).

### Usage

In order to initialize the Client you need to connect it as a Valid Application with your Arnheim Instance

```python
from bergen import Bergen

client = Bergen(host="p-tnagerl-lab1",
    port=8000,
  client_id="APPLICATION_ID_FROM_ARNHEIM", 
  client_secret="APPLICATION_SECRET_FROM_ARNHEIM",
  name="karl",
)
```

In your following code you can simple query your data according to the Schema of the Datapoint


Example 1:
```python
from grunnlag.schema import Node

rep = Representation.objects.get(id=1)
print(rep.shape)

```
Access a Representation (Grunnlags Implementation of a 5 Dimensional Array e.g Image Stack, Time Series Photography) and display the dimensions

Example 2:
```python
from grunnlag.schema import Representation, Sample
from bergen.query import TypedGQL

samples = TypedGQL("""
query {
  samples(creator: 1){
    id
    representations(name: "initial", dims: ["x","y","z"]) {
      id
      store
    }
  }
}
""", Sample).run({})

for sample in samples:
    print(sample.id)
    for representation in sample.representations:
        print(representation.data.shape)

```
Get all Samples and include the representations if they have the name "initial" and contains the required dimensions. (An automatically documented and browsable Schema can be found at your Arnheim Instance /graphql)


Example 3:
```python
from grunnlag.schema import Representation, Sample
from bergen.query import TypedGQL
import xarray as xr


massive_array = xr.DataArray(da.zeros(1024,1024,100,40,4), dims=["x","y","z","t","c"])
rep = Representation.objects.from_xarray(massive_array, name="massive", sample=1)


```
The Grunnlag Implementation allows for upload of massive arrays do to its reliance on Xarray, dask, and zarr, combined with
S3 Storage on the Backend. Client Data gets compresed and send over to the S3 Storage and automatically added to the system.
(Permissions required!)

Example 4:
```python
from grunnlag.schema import Representation, Sample
from bergen.query import TypedGQL
import xarray as xr
import napari

rep = Representation.objects.get(name="massive", sample=1)

with napari.gui_qt() as gui:
    viewer = napari.view_image(rep.data.sel(c=0).data)

```
Combined with Napari that is able to handle dask arrays, data visualization of massive Datasets becomes a breeze as only required chunks are downloaded form the storage backend.

### Testing and Documentation

So far Grunnlad does only provide limitedunit-tests and is in desperate need of documentation,
please beware that you are using an Alpha-Version


### Build with

- [Arnheim](https://github.com/jhnnsrs/arnheim)
- [Pydantic](https://github.com/jhnnsrs/arnheim)


## Roadmap

This is considered pre-Alpha so pretty much everything is still on the roadmap


## Deployment

Contact the Developer before you plan to deploy this App, it is NOT ready for public release

## Versioning

There is not yet a working versioning profile in place, consider non-stable for every release 

## Authors

* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) 

## Acknowledgments

* EVERY single open-source project this library used (the list is too extensive so far)
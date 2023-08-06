# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grunnlag', 'grunnlag.gql']

package_data = \
{'': ['*']}

install_requires = \
['bergen>=0.3.50,<0.4.0',
 'dask[dataframe,array]>=2020.12.0,<2021.0.0',
 's3fs>=0.5.2,<0.6.0',
 'xarray>=0.16.2,<0.17.0',
 'zarr>=2.6.1,<3.0.0']

setup_kwargs = {
    'name': 'grunnlag',
    'version': '0.2.15',
    'description': 'Basic Schema for interacting with Arnheim through Bergen',
    'long_description': '# Grunnlag\n\n### Idea\n\nGrunnlag is a Schema Provider for the Bergen Client accessing your Arnheim Framework\n \n### Prerequisites\n\nBergen (and in Conclusion Grunnlag) only works with a running Arnheim Instance (in your network or locally for debugging).\n\n### Usage\n\nIn order to initialize the Client you need to connect it as a Valid Application with your Arnheim Instance\n\n```python\nfrom bergen import Bergen\n\nclient = Bergen(host="p-tnagerl-lab1",\n    port=8000,\n  client_id="APPLICATION_ID_FROM_ARNHEIM", \n  client_secret="APPLICATION_SECRET_FROM_ARNHEIM",\n  name="karl",\n)\n```\n\nIn your following code you can simple query your data according to the Schema of the Datapoint\n\n\nExample 1:\n```python\nfrom grunnlag.schema import Node\n\nrep = Representation.objects.get(id=1)\nprint(rep.shape)\n\n```\nAccess a Representation (Grunnlags Implementation of a 5 Dimensional Array e.g Image Stack, Time Series Photography) and display the dimensions\n\nExample 2:\n```python\nfrom grunnlag.schema import Representation, Sample\nfrom bergen.query import TypedGQL\n\nsamples = TypedGQL("""\nquery {\n  samples(creator: 1){\n    id\n    representations(name: "initial", dims: ["x","y","z"]) {\n      id\n      store\n    }\n  }\n}\n""", Sample).run({})\n\nfor sample in samples:\n    print(sample.id)\n    for representation in sample.representations:\n        print(representation.data.shape)\n\n```\nGet all Samples and include the representations if they have the name "initial" and contains the required dimensions. (An automatically documented and browsable Schema can be found at your Arnheim Instance /graphql)\n\n\nExample 3:\n```python\nfrom grunnlag.schema import Representation, Sample\nfrom bergen.query import TypedGQL\nimport xarray as xr\n\n\nmassive_array = xr.DataArray(da.zeros(1024,1024,100,40,4), dims=["x","y","z","t","c"])\nrep = Representation.objects.from_xarray(massive_array, name="massive", sample=1)\n\n\n```\nThe Grunnlag Implementation allows for upload of massive arrays do to its reliance on Xarray, dask, and zarr, combined with\nS3 Storage on the Backend. Client Data gets compresed and send over to the S3 Storage and automatically added to the system.\n(Permissions required!)\n\nExample 4:\n```python\nfrom grunnlag.schema import Representation, Sample\nfrom bergen.query import TypedGQL\nimport xarray as xr\nimport napari\n\nrep = Representation.objects.get(name="massive", sample=1)\n\nwith napari.gui_qt() as gui:\n    viewer = napari.view_image(rep.data.sel(c=0).data)\n\n```\nCombined with Napari that is able to handle dask arrays, data visualization of massive Datasets becomes a breeze as only required chunks are downloaded form the storage backend.\n\n### Testing and Documentation\n\nSo far Grunnlad does only provide limitedunit-tests and is in desperate need of documentation,\nplease beware that you are using an Alpha-Version\n\n\n### Build with\n\n- [Arnheim](https://github.com/jhnnsrs/arnheim)\n- [Pydantic](https://github.com/jhnnsrs/arnheim)\n\n\n## Roadmap\n\nThis is considered pre-Alpha so pretty much everything is still on the roadmap\n\n\n## Deployment\n\nContact the Developer before you plan to deploy this App, it is NOT ready for public release\n\n## Versioning\n\nThere is not yet a working versioning profile in place, consider non-stable for every release \n\n## Authors\n\n* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)\n\nSee also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.\n\n## License\n\nAttribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) \n\n## Acknowledgments\n\n* EVERY single open-source project this library used (the list is too extensive so far)',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jhnnsrs/grunnlag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

from grunnlag.gql.sample import CREATE_SAMPLE, FILTER_SAMPLE, GET_SAMPLE
from grunnlag.gql.representation import CREATE_REPRESENTATION, GET_REPRESENTATION, REPRESENTATION_SELECTOR, UPDATE_REPRESENTATION, FILTER_REPRESENTATION
from grunnlag.managers import AsyncRepresentationManager, RepresentationManager
from typing import List, Optional
from bergen.types.model import ArnheimModel
from bergen.schema import User
from enum import Enum
from grunnlag.extenders import Array, RepresentationPrettifier
try:
	# python 3.8
	from typing import ForwardRef
except ImportError:
	# ForwardRef is private in python 3.6 and 3.7
	from typing import _ForwardRef as ForwardRef


Representation = ForwardRef("Representation")
Sample = ForwardRef("Sample")
Experiment = ForwardRef("Experiment")


class RepresentationVariety(str, Enum):
    VOXEL = "VOXEL"
    MASK = "MASK"
    UNKNOWN = "UNKNOWN"



class Representation(RepresentationPrettifier, Array, ArnheimModel):
    id: Optional[int]
    name: Optional[str]
    package: Optional[str]
    store: Optional[str]
    shape: Optional[List[int]]
    image: Optional[str]
    unique: Optional[str]
    variety: Optional[RepresentationVariety]
    sample: Optional[Sample]
    tags: Optional[List[str]]

    objects = RepresentationManager()
    asyncs = AsyncRepresentationManager()

    class Meta:
        identifier = "representation"
        get = GET_REPRESENTATION
        create = CREATE_REPRESENTATION
        update = UPDATE_REPRESENTATION
        filter = FILTER_REPRESENTATION
        selector_query = REPRESENTATION_SELECTOR


class Sample(ArnheimModel):
    id: Optional[int]
    representations: Optional[List[Representation]]
    creator: Optional[User]
    experiment: Optional[Experiment]
    name: Optional[str]

    class Meta:
        identifier = "sample"
        get = GET_SAMPLE
        filter = FILTER_SAMPLE
        create = CREATE_SAMPLE


class Experiment(ArnheimModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    descriptionLong: Optional[str]
    creator: Optional[User]
    sampleSet: Optional[Sample]

    class Meta:
        identifier = "experiment"
        


Representation.update_forward_refs()
Sample.update_forward_refs()
Experiment.update_forward_refs()


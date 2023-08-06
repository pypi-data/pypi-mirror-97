from bergen.query import DelayedGQL


GET_SAMPLE = DelayedGQL("""
query Sample($id: ID!){
  sample(id: $id){
    id
    name
  }
}
""")


FILTER_SAMPLE = DelayedGQL("""
query Samples($creator: ID) {
  samples(creator: $creator) {
    name
    id
    representations {
        id
    }
  }
}
""")


CREATE_SAMPLE = DelayedGQL("""
mutation SampleCreate($name: String!) {
  createSample(name: $name){
    id
    name
    creator {
        username
    }
  }
}
""")
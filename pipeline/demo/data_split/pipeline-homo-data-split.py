from pipeline.backend.config import Backend
from pipeline.backend.config import WorkMode
from pipeline.backend.pipeline import PipeLine
from pipeline.component.dataio import DataIO
from pipeline.component.homo_data_split import HomoDataSplit
from pipeline.component.input import Input
from pipeline.interface.data import Data

guest = 9999
host = 10000
arbiter = 10002

guest_train_data = {"name": "breast_homo_guest", "namespace": "experiment"}
host_train_data = {"name": "breast_homo_host", "namespace": "experiment"}

input_0 = Input(name="train_data")
print ("get input_0's init name {}".format(input_0.name))

pipeline = PipeLine().set_initiator(role='guest', party_id=guest).set_roles(guest=guest, host=host, arbiter=arbiter)

dataio_0 = DataIO(name="dataio_0")

dataio_0.get_party_instance(role='guest', party_id=guest).algorithm_param(with_label=True, output_format="dense")
dataio_0.get_party_instance(role='host', party_id=host).algorithm_param(with_label=True)

homo_data_split_0 = HomoDataSplit(name="homo_data_split_0", stratified=True, test_size=0.2, validate_size=0.1)

print ("get input_0's name {}".format(input_0.name))
pipeline.add_component(dataio_0, data=Data(data=input_0.data))
pipeline.add_component(homo_data_split_0, data=Data(data=dataio_0.output.data))

pipeline.compile()

pipeline.fit(backend=Backend.EGGROLL, work_mode=WorkMode.STANDALONE,
             feed_dict={input_0:
                           {"guest": {9999: guest_train_data},
                            "host": {
                              10000: host_train_data
                             }
                            }

                       })

print (pipeline.get_component("dataio_0").get_model_param())
print (pipeline.get_component("homo_data_split_0").get_summary())


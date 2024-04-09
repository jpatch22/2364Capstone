import vart
import numpy as np
import torch
from vart import Runner
import xir
import torch.nn.functional as F
from app.Annotation import Annotation
import yaml

class Classification_Model_Runner:
    def __init__(self):
        xmodel_file = "app/models/class_v1/class_v1.xmodel"
        graph = xir.Graph.deserialize(xmodel_file)
        subgraph = graph.get_root_subgraph().toposort_child_subgraph()
        index = -1
        for i, s in enumerate(subgraph):
            #print(s.get_attr("device"))
            if s.get_attr("device") == "DPU":
                index = i
        self.runner = Runner.create_runner(subgraph[index], "run")
        

    def get_child_subgraph_dpu(self, graph):
        assert graph is not None, "'graph' should not be None"
        root_subgraph = graph.get_root_subgraph()
        assert (root_subgraph is not None), "Failed to get root graph"
        print(root_subgraph, root_subgraph.is_leaf)
        if root_subgraph.is_leaf:
            return []
    
        child_subgraphs = root_subgraph.toposort_child_subgraph()
        return [
                cs
                for cs in child_subgraphs
                if cs.has_attr("device") and cs.get_attr("device").upper() == "DPU"
                ]
    
    def execute_async(self, dpu, tensor_buffers_dict):
        input_tensor_buffers = [
        tensor_buffers_dict[t.name] for t in dpu.get_input_tensors()
                ]
        output_tensor_buffers = [
                        tensor_buffers_dict[t.name] for t in dpu.get_output_tensors()
                            ]
        jid = dpu.execute_async(input_tensor_buffers, output_tensor_buffers)
        return dpu.wait(jid)

    def pre_process_images(self, image, height, width):
        image = image.resize((height, width))
        image_array = np.array(image)
        data = image_array.astype("float32")
        data /= 255.0
        return data

    def run_dpu(self, images):
        dpu = self.runner
        num_samples = 1
        num_channels = 3
        image_height = 32
        image_width = 32
        num_classes = 10
        input_shape = (num_channels, image_height, image_width)

        image_list = [self.pre_process_images(img, image_height, image_width) for img in images]
    
        input_tensor = dpu.get_input_tensors()
        output_tensor = dpu.get_output_tensors()
    
        input_dims = tuple(input_tensor[0].dims)
        output_dims = tuple(output_tensor[0].dims)
        out = np.zeros(output_dims, dtype='float32')
        batch_size = input_dims[0]
        num_samples = len(image_list)
        n_of_images = num_samples
        sample_input = torch.randn(num_samples, *input_shape)
        count = 0
        outputData = []
        while count < num_samples:
            if (count + batch_size <= num_samples):
                runSize = batch_size 
            else:
                runSize = num_samples - count
            inputData = []
            inputData = [np.empty(input_dims, dtype=np.float32, order="C")]
            for j in range(runSize):
                imageRun = inputData[0]
                #random_data = np.random.rand(*input_dims[1:])
                imageRun[j, ...] = image_list[(count + j) % n_of_images].reshape(input_dims[1:])
    
    
            #execute_async(dpu, {"JacksCNNModel__input_0_fix": inputData[0], "JacksCNNModel__JacksCNNModel_ret_fix": out})
            self.execute_async(dpu, {"ImageClassifier__input_0_fix": inputData[0], "ImageClassifier__ImageClassifier_Linear_fc2__ret_fix": out})
    
            count += runSize 
            for i in range(runSize):
                outputs = out[i, :]
                outputs_tensor = torch.from_numpy(outputs)
    
                probabilities = F.softmax(outputs_tensor, dim=0)
    
                predicted_class = torch.argmax(probabilities)
                outputData.append((predicted_class.clone().item(), torch.max(probabilities).item()))
    
        return outputData
    
    def load_class_dict_from_yaml(self, yaml_path):
        with open(yaml_path, 'r') as file:
            class_dict = yaml.safe_load(file)
        return class_dict

    def supply_annotations(self, image_list):
        mapping_dic = self.load_class_dict_from_yaml("app/models/custom_classification/class_mappings.yaml")
        rev_dic = {v : k for k, v in mapping_dic.items()}
        imdic = {}
        x = self.run_dpu(image_list)
        print(rev_dic.keys())

        for i in range(len(image_list)):
            annotations = []
            annotation = Annotation(None, None, None, None, (rev_dic[x[i][0]], x[i][1]))
            annotation.box = None
            annotations.append(annotation)

            imdic[i] = annotations
        print(imdic)

        return imdic

def main():
    # create graph runner
    modelRunner = Classification_Model_Runner()
    x = modelRunner.run_dpu()
    print(x)

    return

if __name__ == "__main__":
    main()

import os
import shutil
import unittest

from datasets import load_dataset
from nlp_toolkit import DataAugmentation


def build_fake_dataset(save_path):
    from datasets import load_dataset
    from nlp_toolkit.preprocessing.utils import EOS

    split = 'validation'
    count = 10
    dataset = load_dataset('glue', 'sst2', split='validation')
    origin_data = os.path.join(save_path, split + '.csv')
    with open(origin_data, 'w') as fw:
        fw.write('label' + '\t' + 'sentence' + '\n')
        for d in dataset:
            fw.write(str(d['label']) + '\t' + d['sentence'] + EOS + '\n')
            count -= 1
            if count == 0:
                break
    return origin_data


class TestDataAugmentation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        os.makedirs("test_data", exist_ok=True)
        self.result_path = "test_data"
        self.origin_data = build_fake_dataset(self.result_path)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.result_path, ignore_errors=True)

    def test_text_generation_augmentation(self):
        aug = DataAugmentation(augmenter_type="TextGenerationAug")
        aug.input_dataset = self.origin_data
        aug.output_path = os.path.join(self.result_path, "test1.cvs")
        aug.augmenter_arguments = {'model_name_or_path': 'gpt2-medium'}
        aug.data_augment()
        raw_datasets = load_dataset("csv", data_files=aug.output_path, delimiter="\t", split="train")
        self.assertTrue(len(raw_datasets) == 10)

    def test_keyboard_augmentation(self):
        aug = DataAugmentation(augmenter_type="KeyboardAug")
        aug.input_dataset = self.origin_data
        aug.column_names = "sentence"
        aug.output_path = os.path.join(self.result_path, "test2.cvs")
        aug.data_augment()
        raw_datasets = load_dataset("csv", data_files=aug.output_path, delimiter="\t", split="train")
        self.assertTrue(len(raw_datasets) == 10)


if __name__ == "__main__":
    unittest.main()
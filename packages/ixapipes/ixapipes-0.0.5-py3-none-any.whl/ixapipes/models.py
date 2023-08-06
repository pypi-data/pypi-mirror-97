from ixapipes.utils import download_file
import os

models = {
    "morph-models-1.5.0/de/de-lemma-perceptron-conll09.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/de/de-lemma-perceptron-conll09.bin",
    "morph-models-1.5.0/de/de-pos-perceptron-autodict01-conll09.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/de/de-pos-perceptron-autodict01-conll09.bin",
    "morph-models-1.5.0/en/en-lemma-perceptron-conll09.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/en/en-lemma-perceptron-conll09.bin",
    "morph-models-1.5.0/en/en-pos-perceptron-autodict01-conll09.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/en/en-pos-perceptron-autodict01-conll09.bin",
    "morph-models-1.5.0/es/es-lemma-perceptron-ancora-2.0.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/es/es-lemma-perceptron-ancora-2.0.bin",
    "morph-models-1.5.0/es/es-pos-perceptron-autodict01-ancora-2.0.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/es/es-pos-perceptron-autodict01-ancora-2.0.bin",
    "morph-models-1.5.0/eu/eu-lemma-perceptron-epec.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/eu/eu-lemma-perceptron-epec.bin",
    "morph-models-1.5.0/eu/eu-pos-perceptron-epec.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/eu/eu-pos-perceptron-epec.bin",
    "morph-models-1.5.0/fr/fr-lemma-perceptron-sequoia.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/fr/fr-lemma-perceptron-sequoia.bin",
    "morph-models-1.5.0/fr/fr-pos-perceptron-autodict01-sequoia.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/fr/fr-pos-perceptron-autodict01-sequoia.bin",
    "morph-models-1.5.0/gl/gl-lemma-perceptron-autodict05-ctag.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/gl/gl-lemma-perceptron-autodict05-ctag.bin",
    "morph-models-1.5.0/gl/gl-pos-perceptron-autdict05-ctag.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/gl/gl-pos-perceptron-autdict05-ctag.bin",
    "morph-models-1.5.0/nl/nl-lemma-perceptron-alpino.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/nl/nl-lemma-perceptron-alpino.bin",
    "morph-models-1.5.0/nl/nl-pos-perceptron-autodict01-alpino.bin": "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/morph-models-1.5.0/nl/nl-pos-perceptron-autodict01-alpino.bin",
}


def get_model(model_name_or_path: str) -> str:
    if model_name_or_path in models:
        cache_path = os.path.join(
            os.path.expanduser("~/.cache/python-ixa-pipes/"), model_name_or_path
        )

        if os.path.exists(cache_path):
            return cache_path
        else:
            print(f"Downloading model to: {cache_path}")
            download_file(url=models[model_name_or_path], output_path=cache_path)

        return cache_path

    else:
        print(
            f"{model_name_or_path} not found in model list, assuming that it is a path to a model"
        )

        return model_name_or_path

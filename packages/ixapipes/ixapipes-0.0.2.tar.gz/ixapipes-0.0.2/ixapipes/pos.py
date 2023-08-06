import os
from typing import List
from shlex import quote
from IxaPipesModule import IxaPipesModule
from models import get_model


class IxaPipesPosTagger(IxaPipesModule):

    model: str
    lemmatizer_model: str
    beamSize: int
    multiwords: bool
    dictag: bool
    allMorphology: bool
    _executable_path: str = os.path.expanduser(
        "~/.cache/python-ixa-pipes/ixa-pipe-pos-1.5.3-exec.jar"
    )
    _wget_url: str = "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/ixa-pipe-pos-1.5.3-exec.jar"

    def __init__(
        self,
        language: str,
        model: str,
        lemmatizer_model: str,
        port: int = 8891,
        executable_path: str = None,
        beamSize: int = None,
        multiwords: bool = False,
        dictag: bool = False,
        allMorphology: bool = False,
        output_format: str = "naf",
    ):

        if executable_path:
            self._executable_path = executable_path

        self.model = get_model(model)
        self.lemmatizer_model = get_model(lemmatizer_model)

        self.executable_path = executable_path
        self.beamSize = beamSize
        self.multiwords = multiwords
        self.dictag = dictag
        self.allMorphology = allMorphology

        super().__init__(
            language=language,
            server_port=port,
            executable_path=self._executable_path,
            wget_url=self._wget_url,
            run_server_function=self._run_server,
            output_format=output_format,
        )

    def _run_server(
        self,
    ):

        options: List[str] = []

        if self.beamSize:
            options.append(f"--beamSize {quote(str(self.beamSize))}")

        if self.multiwords:
            options.append("--multiwords")

        if self.dictag:
            options.append("--dictag")

        if self.allMorphology:
            options.append("--allMorphology")

        options.append(f"--outputFormat {quote(self.output_format)}")

        print(f"Loading post tagger from {quote(self._executable_path)}")
        command: str = (
            f"java -jar {quote(self._executable_path)} server "
            f"--model {quote(self.model)} "
            f"--lemmatizerModel {quote(self.lemmatizer_model)} "
            f"-l {quote(self.language)} "
            f"-p {quote(str(self.server_port))} "
            f"{' '.join(options)}"
        )

        os.system(command)

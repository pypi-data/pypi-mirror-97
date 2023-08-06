import os
from typing import List
from shlex import quote
from IxaPipesModule import IxaPipesModule


class IxaPipesTokenizer(IxaPipesModule):

    notok: bool
    normalize: str
    untokenizable: str
    output_format: str
    offsets: bool
    inputkaf: bool
    hardParagraph: bool
    kafversion: str
    _executable_path: str = os.path.expanduser(
        "~/.cache/python-ixa-pipes/ixa-pipe-tok-2.0.0-exec.jar"
    )
    _wget_url: str = "https://github.com/ikergarcia1996/IxaPipes-models-executables/raw/main/ixa-pipe-tok-2.0.0-exec.jar"

    def __init__(
        self,
        language: str,
        port: int = 8890,
        executable_path: str = None,
        notok: bool = False,
        normalize: str = None,
        untokenizable: str = None,
        offsets: bool = False,
        inputkaf: bool = False,
        hardParagraph: bool = False,
        kafversion: str = None,
        output_format: str = "naf",
    ):

        if executable_path:
            self._executable_path = executable_path

        self.notok = notok
        self.normalize = normalize
        self.untokenizable = untokenizable
        self.output_format = output_format
        self.offsets = offsets
        self.inputkaf = inputkaf
        self.hardParagraph = hardParagraph
        self.kafversion = kafversion

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

        if self.notok:
            options.append("--notok")

        if self.normalize:
            options.append(f"--normalize {quote(self.normalize)}")

        if self.untokenizable:
            options.append(f"--untokenizable {quote(self.untokenizable)}")

        if self.offsets:
            options.append("--offsets")

        if self.inputkaf:
            options.append("--inputkaf")

        if self.hardParagraph:
            options.append("--hardParagraph")

        if self.kafversion:
            options.append(f"--kafversion {quote(self.kafversion)}")

        options.append(f"--outputFormat {quote(self.output_format)}")

        print(f"Loading tokenizer from {quote(self._executable_path)}")
        command: str = (
            f"java -jar {quote(self._executable_path)} server "
            f"-l {quote(self.language)} "
            f"-p {quote(str(self.server_port))} "
            f"{' '.join(options)}"
        )
        os.system(command)

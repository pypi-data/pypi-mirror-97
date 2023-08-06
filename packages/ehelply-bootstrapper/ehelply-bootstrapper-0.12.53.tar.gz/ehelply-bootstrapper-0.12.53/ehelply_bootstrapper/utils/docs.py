from pathlib import Path
import os.path as OSPath
from typing import List
import re
import os

import pdoc
from pdoc.cli import _open_write_file


def export_code_docs(root_path: Path, modules: List[str]):
    output_dir: Path = root_path.joinpath('docs')

    context = pdoc.Context()

    modules = [pdoc.Module(mod, context=context)
               for mod in modules]
    pdoc.link_inheritance(context)

    def recursive_htmls(mod):
        yield mod.name, mod.html(), mod.url()
        for submod in mod.submodules():
            yield from recursive_htmls(submod)

    for mod in modules:

        for module_name, html, url in recursive_htmls(mod):
            module_name: str
            url: str
            html: str

            url_components: List[str] = url.split("/")
            url_components.pop(0)
            url: str = '/'.join(url_components)

            filepath: str = OSPath.join(str(output_dir), *re.sub(r'\.html$', '.html', url).split('/'))

            dirpath = OSPath.dirname(filepath)
            if not os.access(dirpath, os.R_OK):
                os.makedirs(dirpath)

            with _open_write_file(filepath) as f:
                f.write(html)
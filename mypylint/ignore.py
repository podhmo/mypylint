# -*- coding:utf-8 -*-
import re
from astroid.builder import AstroidBuilder
from astroid import nodes


def register_ignore_module_pattern(manager, pattern):
    """matched module is ignored"""
    rx = re.compile(pattern)

    skip_comment = AstroidBuilder(manager).string_build("#pylint: skip-file")

    def set_skip_comment(module):
        if not rx.match(module.name):
            return
        module.file_bytes = skip_comment.file_bytes
    manager.register_transform(nodes.Module, set_skip_comment)

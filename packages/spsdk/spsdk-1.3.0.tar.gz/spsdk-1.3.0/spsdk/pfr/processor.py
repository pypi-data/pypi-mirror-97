#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020-2021 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Processor for conditions in rules."""

import ast
import logging
import re
from typing import Tuple

import astunparse

from .translator import Translator


class MyTransformer(ast.NodeTransformer):
    """AST-based transformer for replacing string names with actual values."""

    def __init__(self, translator: Translator) -> None:
        """Initialize Transformer.

        :param translator: Translator instance
        """
        self.translator = translator
        self.logger = logging.getLogger("transformer")

    def visit_Attribute(self, node: ast.Attribute) -> ast.Constant:  # pylint: disable=invalid-name
        """Translate Attribute Nodes."""
        self.logger.debug("Transforming node attribute...")
        thing = astunparse.unparse(node).strip()
        value = self.translator.translate(thing)
        self.logger.debug(f"Attribute '{thing}' transformed into {value:x}")
        result = ast.Constant(value=value, kind=None)
        return ast.copy_location(result, node)


class Processor:
    """Class responsible for processing conditions.

    Processor is responsible for processing condition
        - parsing the condition string (lookup)
        - calling translator for individual keys (registers)

    Translator is responsible for looking up values for given keys
    """

    def __init__(self, translator: Translator) -> None:
        """Initialize processor.

        :param translator: Translator instance
        """
        self.logger = logging.getLogger("processor")
        self.transformer = MyTransformer(translator)

    def process(self, condition: str) -> Tuple[bool, str]:
        """Process individual condition from rules.

        :param condition: condition to quantify
        :return: Boolean result and values for translated keys
        """
        self.logger.debug("Transforming condition: {}".format(condition))
        org_node = ast.parse(condition, mode="eval")
        new_node = self.transformer.visit(org_node)
        self.logger.debug("Transformed condition: {}".format(new_node))
        node_str = astunparse.unparse(new_node)
        node_str = self._replaceIntAsHex(node_str)
        result = eval(compile(new_node, filename="", mode="eval"))
        return result, node_str

    @staticmethod
    def _replaceIntAsHex(string: str) -> str:
        """Converts all numeric occurrences in `string` in decimal form into hexadecimal form.

        :param string: string to process
        :return: returns a string, where all numbers represented as in dec form are converted to hex form
        """
        replaced_string = ""
        for sub_string in re.split("([0-9]+)", string):
            replaced_string += hex(int(sub_string, 0)) if sub_string.isnumeric() else sub_string

        return replaced_string

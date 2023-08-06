#
# ddSMT: A delta debugger for SMT benchmarks in SMT-Lib v2 format.
#
# This file is part of ddSMT.
#
# Copyright (C) 2013-2021 by the authors listed in AUTHORS file.
#
# ddSMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ddSMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ddSMT.  If not, see <https://www.gnu.org/licenses/>.

import re

from .smtlib import *
from .mutator_utils import Simplification


class CheckSatAssuming:
    """Replaces a ``check-sat-assuming`` by a regular ``check-sat``, discarding
    the assumption."""
    def filter(self, node):
        return node.has_ident() and node.get_ident() == 'check-sat-assuming'

    def mutations(self, node):
        return [Simplification({node.id: Node(Node('check-sat'))}, [])]

    def __str__(self):
        return 'substitute check-sat-assuming by check-sat'


class EliminateVariable:
    """Eliminate a variable using an equality with this variable.

    Tries to globally replace every leaf node from an equality by every
    other node from the same equality. For example, for ``(= x (* a b)
    (+ c d))`` the variable ``x`` is replaced by either ``(* a b)`` or
    ``(+ c d)``.
    """
    def filter(self, node):
        return is_eq(node) and any(map(lambda n: n.is_leaf(), node[1:]))

    def global_mutations(self, linput, ginput):
        ops = linput[1:]
        targets = list(filter(lambda n: n.is_leaf(), ops))
        for t in targets:
            for c in ops:
                if c == t:
                    continue
                if t in nodes.dfs(c):
                    # Avoid cycles (for example with core.ReplaceByChild)
                    continue
                substs = {}
                for n in nodes.dfs(ginput):
                    if n == t and not is_definition_node(n):
                        substs[n.id] = c
                if substs:
                    yield Simplification(substs, [])

    def __str__(self):
        return 'eliminate variable from equality'


class InlineDefinedFuns:
    """Explicitly inlines a defined function."""
    def filter(self, node):
        return is_defined_fun(node)

    def mutations(self, node):
        if node.id in map(lambda n: n.id, nodes.dfs(get_defined_fun(node))):
            # we are about to inline the function into its own body
            return []
        if is_definition_node(node):
            # we are about to inline the function into its own name
            return []
        res = get_defined_fun(node)
        if res == node:
            return []
        return [Simplification({node.id: res}, [])]

    def __str__(self):
        return 'inline defined function'


class IntroduceFreshVariable:
    """Replace a term by a fresh variable of the appropriate type."""
    def filter(self, node):
        # introducing a fresh variable may lead to cycles in various cases,
        # thus we exclude a variety of nodes here:
        # - constants, leaf nodes
        # - BV terms with a single variable and smaller bit-width.
        if is_const(node) or node.is_leaf() or is_definition_node(node):
            return False
        sort = get_sort(node)
        if sort is None:
            return False
        if is_bv_sort(sort):
            found = False
            for n in nodes.dfs(node):
                if is_var(n):
                    if found:
                        return True
                    found = True
                    bw = get_bv_width(n)
                    if bw > int(sort[2].data):
                        return True
            return False
        return True

    def global_mutations(self, linput, ginput):
        varname = Node(f'x{linput.id}__fresh')
        if is_var(varname):
            return []
        var = Node('declare-const', varname, get_sort(linput))
        return [Simplification({linput.id: varname}, [var])]

    def __str__(self):
        return 'introduce fresh variable'


class LetElimination:
    """Substitutes a ``let`` expression with its body."""
    def filter(self, node):
        return is_operator_app(node, 'let')

    def mutations(self, node):
        if len(node) <= 2:
            return []
        return [Simplification({node.id: node[2]}, [])]

    def __str__(self):
        return 'eliminate let binder'


class LetSubstitution:
    """Substitutes a variable bound by a ``let`` binder into the nested
    term."""
    def filter(self, node):
        return is_operator_app(node, 'let')

    def mutations(self, node):
        if len(node) <= 2:
            return []
        for var in node[1]:
            if any(n == var[0] for n in nodes.dfs(node[2])):
                subs = nodes.substitute(node[2], {var[0]: var[1]})
                yield Simplification({node.id: Node(node[0], node[1], subs)},
                                     [])

    def __str__(self):
        return 'substitute variable into let body'


class SimplifyLogic:
    """Replaces the logic specified in ``(check-logic ...)`` by a simpler
    one."""
    def filter(self, node):
        return node.has_ident() and node.get_ident() == 'set-logic'

    def mutations(self, node):
        logic = node[1]
        cands = []
        repls = {
            'BV': '',
            'FP': '',
            'UF': '',
            'S': '',
            'T': '',
            'NRA': 'LRA',
            'LRA': '',
            'NIA': 'LIA',
            'LIA': '',
            'NIRA': 'LIRA',
            'LIRA': 'LRA'
        }
        for r in repls:
            assert logic.is_leaf()
            if r in logic.data:
                cands.append(logic.data.replace(r, repls[r]))
        yield from [
            Simplification({node.id: Node('set-logic', c)}, []) for c in cands
        ]

    def __str__(self):
        return 'simplify logic'


class SimplifyQuotedSymbols:
    """Turns a quoted symbol into a simple symbol."""
    def filter(self, node):
        return is_piped_symbol(node) and re.match(
            '\\|[a-zA-Z0-9~!@$%^&*_+=<>.?/-]+\\|', node.data) is not None

    def mutations(self, node):
        return [Simplification({node.id: get_piped_symbol(node)}, [])]

    def global_mutations(self, linput, ginput):
        return [Simplification({linput: get_piped_symbol(linput)}, [])]

    def __str__(self):
        return 'simplify quoted symbol'


class SimplifySymbolNames:
    """Simplify variable names by making them smaller.

    Should only have cosmetic impact, unless two variable names change
    their order enabling :class:`ddsmt.mutators_core.ReplaceByVariable`.
    """
    def filter(self, node):
        # check for is_const(node[1]) to avoid x -> false -> fals -> false
        # if the variable is irrelevant, false may be accepted by the solver
        return node.has_ident() and node.get_ident() in [
            'declare-const', 'declare-datatype', 'declare-datatypes',
            'declare-fun', 'declare-sort', 'define-fun', 'exists', 'forall'
        ] and not is_const(node[1])

    def global_mutations(self, linput, ginput):
        if linput.get_ident() in ['declare-datatype', 'declare-datatypes']:
            for c in self.__flatten(Node(linput[1:])):
                yield from self.__mutate_symbol(c, ginput)
            return
        if linput.get_ident() in ['exists', 'forall']:
            for v in linput[1]:
                yield from self.__mutate_symbol(v[0], ginput)
            return
        yield from self.__mutate_symbol(linput[1], ginput)

    def __flatten(self, n):
        """Yield given node as flattened sequence."""
        if n.is_leaf():
            yield n
        else:
            for e in n.data:
                yield from self.__flatten(e)

    def __mutate_symbol(self, symbol, ginput):
        """Return a list of mutations of ginput based on simpler versions of
        symbol."""
        if is_piped_symbol(symbol):
            for s in self.__simpler(get_piped_symbol(symbol)):
                if not is_var(Node('|' + s + '|')):
                    yield Simplification({symbol: Node('|' + s + '|')}, [])
        else:
            for s in self.__simpler(symbol):
                if not is_var(Node(s)):
                    yield Simplification({symbol: Node(s)}, [])

    def __simpler(self, symbol):
        """Return a list of simpler versions of the given symbol."""
        sym = symbol.data
        if len(sym) > 3:
            yield sym[:len(sym) // 2]
        if len(sym) > 1:
            yield sym[:-1]
            yield sym[1:]

    def __str__(self):
        return 'simplify symbol name'


def get_mutators():
    """Returns a mapping from mutator class names to the name of their config
    options."""
    return {
        'CheckSatAssuming': 'check-sat-assuming',
        'EliminateVariable': 'eliminate-variables',
        'InlineDefinedFuns': 'inline-functions',
        'IntroduceFreshVariable': 'introduce-fresh-variables',
        'LetElimination': 'let-elimination',
        'LetSubstitution': 'let-substitution',
        'SimplifyLogic': 'simplify-logic',
        'SimplifyQuotedSymbols': 'simplify-quoted-symbols',
        'SimplifySymbolNames': 'simplify-symbol-names',
    }

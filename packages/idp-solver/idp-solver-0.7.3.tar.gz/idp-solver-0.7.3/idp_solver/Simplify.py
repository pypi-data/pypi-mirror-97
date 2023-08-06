# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

Methods to simplify a logic expression.

This module monkey-patches the Expression class and sub-classes.


"""

import sys
from typing import List

from .Expression import (
    Constructor, Expression, IfExpr, AQuantification, \
    BinaryOperator, AEquivalence, AImplication, ADisjunction, \
    AConjunction, AComparison, ASumMinus, AMultDiv, APower, \
    AUnary, AAggregate, AppliedSymbol, UnappliedSymbol, \
    Number, Brackets, Variable, TRUE, FALSE)
from .Parse import Enumeration, Tuple
from .Assignments import Status, Assignment
from .utils import INT


# class Expression  ###########################################################

def _change(self, sub_exprs=None, ops=None, value=None, simpler=None,
            co_constraint=None):
    " change attributes of an expression, and resets derived attributes "

    if sub_exprs is not None:
        self.sub_exprs = sub_exprs
    if ops is not None:
        self.operator = ops
    if co_constraint is not None:
        self.co_constraint = co_constraint
    if value is not None:
        self.value = value
    elif simpler is not None:
        if type(simpler) in [Constructor, Number]:
            self.value = simpler
        elif simpler.value is not None:  # example: prime.idp
            self.value = simpler.value
        else:
            self.simpler = simpler
    assert self.value is None or type(self.value) in [Constructor,
                                                      Number]
    assert self.value is not self  # avoid infinite loops

    # reset derived attributes
    self.str = sys.intern(str(self))

    return self

Expression._change = _change


def update_exprs(self, new_exprs):
    """ change sub_exprs and simplify, while keeping relevant info. """
    #  default implementation, without simplification
    return self._change(sub_exprs=list(new_exprs))


# Expression.update_exprs = update_exprs
for i in [Constructor, AppliedSymbol, UnappliedSymbol, Variable, Number]:
    i.update_exprs = update_exprs


def simplify1(self):
    return self.update_exprs(self.sub_exprs)
Expression.simplify1 = simplify1



# Class IfExpr  ###############################################################


def update_exprs(self, new_exprs):
    sub_exprs = list(new_exprs)
    if_, then_, else_ = sub_exprs[0], sub_exprs[1], sub_exprs[2]
    if if_.same_as(TRUE):
        return self._change(simpler=then_, sub_exprs=sub_exprs)
    elif if_.same_as(FALSE):
        return self._change(simpler=else_, sub_exprs=sub_exprs)
    else:
        if then_.same_as(else_):
            return self._change(simpler=then_, sub_exprs=sub_exprs)
        elif then_.same_as(TRUE) and else_.same_as(FALSE):
            return self._change(simpler=if_, sub_exprs=sub_exprs)
        elif then_.same_as(FALSE) and else_.same_as(TRUE):
            return self._change(simpler=AUnary.make('¬', if_),
                                sub_exprs=sub_exprs)
    return self._change(sub_exprs=sub_exprs)
IfExpr.update_exprs = update_exprs



# Class AQuantification  ######################################################

def update_exprs(self, new_exprs):
    exprs = list(new_exprs)
    simpler = exprs[0] if not self.q_vars else None
    return self._change(simpler=simpler, sub_exprs=exprs)
AQuantification.update_exprs = update_exprs


# Class AImplication  #######################################################

def update_exprs(self, new_exprs):
    exprs0 = next(new_exprs)
    value, simpler = None, None
    if exprs0.same_as(FALSE):  # (false => p) is true
        # exprs[0] may be false because exprs[1] was false
        exprs1 = self.sub_exprs[1] if self.sub_exprs[1].same_as(FALSE)\
            else FALSE
        value = TRUE
    elif exprs0.same_as(TRUE):  # (true => p) is p
        exprs1 = next(new_exprs)
        simpler = exprs1
    else:
        exprs1 = next(new_exprs)
        if exprs1.same_as(TRUE):  # (p => true) is true
            exprs0 = exprs0 if self.sub_exprs[0].same_as(TRUE) else TRUE
            value = TRUE
        elif exprs1.same_as(FALSE):  # (p => false) is ~p
            simpler = AUnary.make('¬', exprs0)
    return self._change(value=value, simpler=simpler,
                        sub_exprs=[exprs0, exprs1])
AImplication.update_exprs = update_exprs


# Class AEquivalence  #######################################################

def update_exprs(self, new_exprs):
    exprs = list(new_exprs)
    if len(exprs) == 1:
        return self._change(simpler=exprs[1], sub_exprs=exprs)
    for e in exprs:
        if e.same_as(TRUE):  # they must all be true
            return self._change(simpler=AConjunction.make('∧', exprs),
                                sub_exprs=exprs)
        if e.same_as(FALSE):  # they must all be false
            return self._change(simpler=AConjunction.make('∧', [AUnary.make('¬', e) for e in exprs]),
                                sub_exprs=exprs)
    return self._change(sub_exprs=exprs)
AEquivalence.update_exprs = update_exprs


# Class ADisjunction  #######################################################

def update_exprs(self, new_exprs):
    exprs, other = [], []
    value, simpler = None, None
    for i, expr in enumerate(new_exprs):
        if expr.same_as(TRUE):
            # simplify only if one other sub_exprs was unknown
            if any(e.value is None and not i == j for j, e in enumerate(self.sub_exprs)):
                return self._change(value=TRUE, sub_exprs=[expr])
            value = TRUE
        exprs.append(expr)
        if not expr.same_as(FALSE):
            other.append(expr)

    if len(other) == 0:  # all disjuncts are False
        value = FALSE
    if len(other) == 1:
        simpler = other[0]
    return self._change(value=value, simpler=simpler, sub_exprs=exprs)
ADisjunction.update_exprs = update_exprs


# Class AConjunction  #######################################################

# same as ADisjunction, with TRUE and FALSE swapped
def update_exprs(self, new_exprs):
    exprs, other = [], []
    value, simpler = None, None
    for i, expr in enumerate(new_exprs):
        if expr.same_as(FALSE):
            # simplify only if one other sub_exprs was unknown
            if any(e.value is None and not i == j for j, e in enumerate(self.sub_exprs)):
                return self._change(value=FALSE, sub_exprs=[expr])
            value = FALSE
        exprs.append(expr)
        if not expr.same_as(TRUE):
            other.append(expr)

    if len(other) == 0:  # all conjuncts are True
        value = TRUE
    if len(other) == 1:
        simpler = other[0]
    return self._change(value=value, simpler=simpler, sub_exprs=exprs)
AConjunction.update_exprs = update_exprs



# Class AComparison  #######################################################

def update_exprs(self, new_exprs):
    operands = list(new_exprs)
    operands1 = [e.as_rigid() for e in operands]
    if all(e is not None for e in operands1):
        acc, acc1 = operands[0], operands1[0]
        assert len(self.operator) == len(operands1[1:]), "Internal error"
        for op, expr, expr1 in zip(self.operator, operands[1:], operands1[1:]):
            if not (BinaryOperator.MAP[op]) (acc1.py_value, expr1.py_value):
                return self._change(value=FALSE, sub_exprs=[acc, expr], ops=[op])
            acc, acc1 = expr, expr1
        return self._change(value=TRUE, sub_exprs=operands)
    return self._change(sub_exprs=operands)
AComparison.update_exprs = update_exprs

def as_set_condition(self):
    return ((None, None, None) if not self.is_assignment() else
            (self.sub_exprs[0], True,
             Enumeration(tuples=[Tuple(args=[self.sub_exprs[1]])])))
AComparison.as_set_condition = as_set_condition

#############################################################

def update_arith(self, family, operands):
    operands = list(operands)
    operands1 = [e.as_rigid() for e in operands]
    if all(e is not None for e in operands1):
        out = operands1[0].py_value

        for e, op in zip(operands1[1:], self.operator):
            function = BinaryOperator.MAP[op]

            if op == '/' and self.type == INT:  # integer division
                out //= e.py_value
            else:
                out = function(out, e.py_value)
        value = Number(number=str(out))
        return self._change(value=value, sub_exprs=operands)
    return self._change(sub_exprs=operands)


# Class ASumMinus  #######################################################

def update_exprs(self, new_exprs):
    return update_arith(self, '+', new_exprs)
ASumMinus.update_exprs = update_exprs


# Class AMultDiv  #######################################################

def update_exprs(self, new_exprs):
    operands = list(new_exprs)
    if any(op == '%' for op in self.operator):  # special case !
        operands1 = [e.as_rigid() for e in operands]
        if len(operands) == 2 \
           and all(e is not None for e in operands1):
            out = operands1[0].py_value % operands1[1].py_value
            return self._change(value=Number(number=str(out)), sub_exprs=operands)
        else:
            return self._change(sub_exprs=operands)
    return update_arith(self, '*', operands)
AMultDiv.update_exprs = update_exprs


# Class APower  #######################################################

def update_exprs(self, new_exprs):
    operands = list(new_exprs)
    operands1 = [e.as_rigid() for e in operands]
    if len(operands) == 2 \
       and all(e is not None for e in operands1):
        out = operands1[0].py_value ** operands1[1].py_value
        return self._change(value=Number(number=str(out)), sub_exprs=operands)
    else:
        return self._change(sub_exprs=operands)
APower.update_exprs = update_exprs


# Class AUnary  #######################################################

def update_exprs(self, new_exprs):
    operand = list(new_exprs)[0]
    if self.operator == '¬':
        if operand.same_as(TRUE):
            return self._change(value=FALSE, sub_exprs=[operand])
        if operand.same_as(FALSE):
            return self._change(value=TRUE, sub_exprs=[operand])
    else:  # '-'
        a = operand.as_rigid()
        if a is not None:
            if type(a) == Number:
                return self._change(value=Number(number=str(- a.translate())), sub_exprs=[operand])
    return self._change(sub_exprs=[operand])
AUnary.update_exprs = update_exprs

def as_set_condition(self):
    (x, y, z) = self.sub_exprs[0].as_set_condition()
    return ((None, None, None) if x is None else
            (x, not y, z))
AUnary.as_set_condition = as_set_condition


# Class AAggregate  #######################################################

def update_exprs(self, new_exprs):
    operands = list(new_exprs)
    if self.quantifier_is_expanded:
        operands1 = [e.as_rigid() for e in operands]
        if all(e is not None for e in operands1):
            out = sum(e.py_value for e in operands1)
            out = Number(number=str(out))
            return self._change(value=out, sub_exprs=operands)

    return self._change(sub_exprs=operands)
AAggregate.update_exprs = update_exprs


# Class AppliedSymbol  #######################################################

def as_set_condition(self):
    # determine core after substitutions
    core = AppliedSymbol.make(self.s, self.sub_exprs).copy()

    return ((None, None, None) if not self.in_enumeration else
            (core, 'not' not in self.is_enumeration, self.in_enumeration))
AppliedSymbol.as_set_condition = as_set_condition


# Class Brackets  #######################################################

def update_exprs(self, new_exprs):
    expr = list(new_exprs)[0]
    return self._change(sub_exprs=[expr], value=expr.value)
Brackets.update_exprs = update_exprs


# set conditions  #######################################################

def join_set_conditions(assignments: List[Assignment]) -> List[Assignment]:
    """In a list of assignments, merge assignments that are set-conditions on the same term.

    An equality and a membership predicate (`in` operator) are both set-conditions.

    Args:
        assignments (List[Assignment]): the list of assignments to make more compact

    Returns:
        List[Assignment]: the compacted list of assignments
    """
    #
    for i, c in enumerate(assignments):
        (x, belongs, y) = c.as_set_condition()
        if x:
            for j in range(i):
                (x1, belongs1, y1) = assignments[j].as_set_condition()
                if x1 and x.same_as(x1):
                    if belongs and belongs1:
                        new_tuples = (y.tuples & y1.tuples) # intersect
                    elif belongs and not belongs1:
                        new_tuples = (y.tuples ^ y1.tuples) # difference
                    elif not belongs and belongs1:
                        belongs = belongs1
                        new_tuples = (y1.tuples ^ y.tuples)
                    else:
                        new_tuples = y.tuples | y1.tuples # union
                    # sort again
                    new_tuples = list(new_tuples.values())

                    out = AppliedSymbol.make(
                        symbol=x.s, args=x.sub_exprs,
                        is_enumeration='in',
                        in_enumeration=Enumeration(tuples=new_tuples)
                    )

                    core = AppliedSymbol.make(out.s, out.sub_exprs).copy()
                    out.simpler = out.in_enumeration.contains([core], False)

                    out = Assignment(out,
                                        TRUE if belongs else FALSE,
                                        Status.UNKNOWN)

                    assignments[j] = out # keep the first one
                    assignments[i] = Assignment(TRUE, TRUE, Status.UNKNOWN)
    return [c for c in assignments if c.sentence != TRUE]

Done = True

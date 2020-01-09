from goald.config.model.alternative import Alternative
from goald.config.model.context_change import ContextChange, OP
from goald.config.model.context_conditions import ContextCondition
from goald.config.model.dependency_modifier import DependencyModifier, Type
from goald.config.model.goal import Goal


def test_alternative():
    alternative = Alternative()
    assert not alternative.resolved


def test_context_change():
    context_change = ContextChange(op=OP.ADDED, 
                                   label='c1', 
                                   time=1)
    assert context_change.op == OP.ADDED

def test_context_conditions():
    context_conditions = ContextCondition(
        label='c1')
    assert not context_conditions.label == 'c2'

    
def test_dependency_modifier():
    dependency_modifier = DependencyModifier(
        _type= Type.ONE,
        groupId='group 1')
    assert dependency_modifier.type == Type.ONE


def test_goal():
    goal = Goal(
        identification= 'g1'
    )
    assert goal.identification == 'g1'
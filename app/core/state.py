from typing import Annotated, List, Set, Optional, TypedDict
from langgraph.graph.message import AnyMessage, BaseMessage
from operator import add
from langgraph.managed.is_last_step import RemainingSteps


# The MultiAgentState class definition
class MultiAgentState(TypedDict):
    question: Annotated[List[AnyMessage], add]
    question_type: Annotated[List[AnyMessage], add]
    answer: Annotated[List[AnyMessage], add]
    context_question: Annotated[List[AnyMessage], add]
    draft_answer: Annotated[List[AnyMessage], add]
    name: str
    income: str
    expenses: str
    profession: str
    NER: bool
    domain: str
    chat_history: Annotated[List[AnyMessage], add]
    messages: Annotated[List[BaseMessage], add]
    remaining_steps: RemainingSteps
    agent_scratchpad: Annotated[List[AnyMessage], add]

from app.core.state import MultiAgentState
from langgraph.graph import StateGraph, END
from  app.agents import profile, domain, context, router, fintalk, claw, rtd, general, editor
# Routing functions
def route_question(state: MultiAgentState):
    if 'question_type' not in state.keys():
        return 'GENERAL'
    return state['question_type'][-1]

def route_context(state: MultiAgentState):
    if 'NER' not in state.keys():
        return False
    return state['NER']

def route_domain(state: MultiAgentState):
    if 'domain' not in state.keys():
        return 'general'
    return state['domain']

# Main function to build and return the graph
def build_financial_assistant_graph(hf_token=None, tavily_key=None, checkpointer=None):
    
    if hf_token is None:
        raise ValueError("HuggingFace token is required")
    
    if tavily_key is None:
        raise ValueError("TavilyKey is required")
    
    
    # Build the graph
    builder = StateGraph(MultiAgentState)

    builder.add_node("profile", profile.profile_node)
    builder.add_node("domain_node", domain.domain_node)
    builder.add_node("context", context.context_node)
    builder.add_node("router", router.router_node)
    builder.add_node('finTALK', fintalk.financial_terms_node)
    builder.add_node('claw', claw.canadian_rules_node)
    builder.add_node('RTData', rtd.rtd_node)
    builder.add_node('general_assistant', general.general_assistant_node)
    builder.add_node('editor', editor.editor_node)
    
    builder.add_conditional_edges(
        "router",
        route_question,
        {'FINANCE_TERMS': 'finTALK',
         'CANADIAN_RULES': 'claw',
         'RTD': 'RTData',
         'GENERAL': 'general_assistant',}
    )

    builder.add_conditional_edges(
        "context",
        route_context,
        {True: 'router',
         False: 'editor', }
    )
    
    builder.add_conditional_edges(
        "domain_node",
        route_domain,
        {
         'general': 'general_assistant',
         'finance': 'context'
         }
    )

    builder.set_entry_point("profile")
    builder.add_edge('profile', 'domain_node')
    builder.add_edge('finTALK', 'editor')
    builder.add_edge('claw', 'editor')
    builder.add_edge('RTData', 'editor')
    builder.add_edge('general_assistant', 'editor')
    builder.add_edge('editor', END)
    
    return builder.compile(checkpointer=checkpointer)
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langchain_core.runnables import RunnableLambda

from schema import AgentState
from nodes import parse_resume, parse_jd, identify_pros_cons

import re
import json

from schema import AgentState
from nodes import gap_analysis, parse_resume, parse_jd, edit_resume

## --- Nodes of High-Level Agent Graph ---
##
##  START --> parse_resume_node --> identify_pros_cons_node --> make_resume_edits_node --> END
##            parse_jd_node     -------^
##

def parse_resume_node(state: AgentState) -> AgentState:
    '''
    This node is responsible for parsing the latex to identify sections (Education, Experience) and their points
    It has tools comprising of python methods and sub-agents meant to:
    1) Parse and identify points
    2) Language of user, prose
    3) Combine sections with existing info from datasource (excel sheet?)
    '''
    print('parsing resume ...')
    sections = parse_resume.parse_pdf(state['resume'])

    return {**state, 'resume_sections': sections}

def parse_jd_node(state: AgentState) -> AgentState:
    '''
    This node parses string of job description and identifies skills at various strata
    Strata as in:
    - jd summary
    - low-level skills like tools, languages (Hard|Soft)
    - high-level skills like workflows, disciplines
        (data engineering vs data science vs ai engineering vs applied mle)
    - preferred background
    - key responsibilities (can the resume person fulfil them?)
    - keywords

    Next Steps:
    - RAG for company info, uncommon terms, similar job postings
    - use Output for Post Parse Validation (is the llm's output in the jd)
    '''
    print('parsing jd ...')
    chains = parse_jd.get_details_llmchain()

    insights = {target : chain.invoke({
        "job_description": state['jd']#,
        #"schema": output_parser.get_format_instructions()
    }).content for target, chain in chains.items()}

    return {**state, "jd_sections" : insights}


def identify_pros_cons_node(state: AgentState) -> AgentState:
    '''
    This node takes input from previous nodes and identifies high-level changes
    needed for resume to reflect job description
    1) low-level changes: keywords
    2) high-level changes: experiences in building a specific tool, education requirement

    The node returns steps of modification to achieve each needed change
    NOTE: for demo, if changes require info not in resume/datasource, will create new info
        for resume edits (may not be true).
    '''
    print('gap analysis ...')
    chain = gap_analysis.get_suggestions_llmchains()

    insight = chain.invoke({
        "jd_sections" : state['jd_sections'],
        'resume_sections' : state['resume_sections']
    }).content

    output = re.sub(r"^```json|```$", "", insight.strip()).strip()

    return {**state, "suggestions": output}


def make_resume_edits_node(state: AgentState) -> AgentState:
    '''
    This node applies the changes from previous node to latex document
    while maintaining language, structure of original resume.
    '''
    print('making resume edits, rendering ...')
    chain = edit_resume.get_resume_edit_chain()

    pdfstring = chain.invoke({
        "resume" : state['resume'],
        "jd_text" : state["jd"],
        "suggestions_json" : state["suggestions"]
    }).content

    return {**state, "new_resume" : pdfstring}

##
## --- Agent Initialization ---
##

def init_agent() -> CompiledStateGraph:
    '''
    Returns an initialized StateGraph agent
    with the nodes listed above, in the order described in the comment
    '''
    graph = StateGraph(AgentState)

    graph.add_node("parse_resume_node", parse_resume_node)
    graph.add_node("parse_jd_node", parse_jd_node)
    graph.add_node("identify_pros_cons_node", identify_pros_cons_node)
    graph.add_node("make_resume_edits_node", make_resume_edits_node)

    graph.add_edge(START, "parse_resume_node")
    graph.add_edge("parse_resume_node", "parse_jd_node")
    graph.add_edge("parse_jd_node", "identify_pros_cons_node")
    graph.add_edge("identify_pros_cons_node", "make_resume_edits_node")
    graph.add_edge("make_resume_edits_node", END)

    agent_instance = graph.compile()

    return agent_instance

def modify_resume(old_resume: str, jd: str) -> str:
    agent = init_agent()

    try:
        state = { 'resume': old_resume, 'jd': jd }
        final_state = None

        for event in agent.stream(state, stream_mode="values"):
            print("=== Event ===")
            print(json.dumps(event, indent=4, ensure_ascii=False))
            final_state = event

        return final_state['new_resume']
    except Exception as e:
        print("❌ Agent failed:", e, "\n\n")
        print("=== Last Known State === \n\n")
        print(json.dumps(final_state, indent=2, ensure_ascii=False))
        raise


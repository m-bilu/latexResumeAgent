from typing import TypedDict, Dict, List

class AgentState(TypedDict):
    '''
    Defines the universal state of the full Agent
    '''
    ## Objective truth
    resume: str ## latex
    jd: str

    ## Extracted sections
    resume_sections: Dict[str, Dict]
    jd_sections: Dict[str, List[str]]

    new_resume: str ## latex, to return at the end



     
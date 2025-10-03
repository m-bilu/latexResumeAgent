'''
This file contains all tools needed for the parse_resume node. Goal is to extract
Tools can include python methods, LLMChains, independent sub-Agents
'''

import re
from typing import Dict, List, Tuple
from collections import defaultdict
from nodes.config import llm

##
## --- Classical Python Method Tools, no LLM/Agents ---
##

def parse_pdf(pdfstring: str) -> Dict[str, Dict | str]:
    '''
    This method takes the string of all text in a resume, returns a dict of each section
    '''
    lines = [line.strip() for line in pdfstring.split("\n") if line.strip()]

    section_headers = [
        "EDUCATION", "EXPERIENCE", "WORK EXPERIENCE",
        "PROJECTS", "SKILLS", "TECHNICAL SKILLS",
        "PUBLICATIONS", "AWARDS", "CERTIFICATIONS"
    ]

    sections: Dict[str, Dict] = {}
    current_section = "HEADER"
    sections[current_section] = {}

    current_item = None

    for line in lines:
        if any(re.fullmatch(rf"{header}.*", line.upper()) for header in section_headers):
            current_section = line.upper()
            sections[current_section] = {}
            current_item = None
            continue

        if re.match(r"^[-•\u2022]", line):
            if current_item is None:
                current_item = "UNKNOWN"
                sections[current_section][current_item] = []
            bullet = line.lstrip("-•\u2022").strip()
            sections[current_section][current_item].append(bullet)

        else:
            current_item = line
            if current_item not in sections[current_section]:
                sections[current_section][current_item] = []

    return sections


##
## --- LLMChains ---
##

## INCOMING, V1 will only use the structured json parsed from .tex, with no LLM insights
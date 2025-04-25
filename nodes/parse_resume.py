'''
This file contains all tools needed for the parse_resume node
Tools can include python methods, LLMChains, independent sub-Agents
'''

import re
from typing import Dict, List, Tuple
from collections import defaultdict
import nodes.config as config

##
## --- Classical Python Method Tools, no LLM/Agents ---
##

def find_ending_brace(s: str, start: int) -> int:
    # Handles nested braces
    if s[start] not in "{[":
        return -1
    open_brace = s[start]
    close_brace = "}" if open_brace == "{" else "]"
    count = 0
    for i in range(start, len(s)):
        if s[i] == open_brace:
            count += 1
        elif s[i] == close_brace:
            count -= 1
            if count == 0:
                return i
    return -1


def remove_unnecessary_tags(content: str, tag_types: List[Tuple[str, bool]] = config.TAG_TYPES) -> str:
    '''
    Removes specified LaTeX tags from a string.
    Each tag is a tuple (tag_name, remove_inner), where:
    - tag_name is the LaTeX command (without the backslash),
    - remove_inner determines whether to delete the content inside the braces.
    
    In both cases, the surrounding braces are removed.
    '''
    i = 0
    result = ''
    while i < len(content):
        if content[i] == "\\":
            matched = False
            for tag, remove_inner in tag_types:
                if content.startswith(tag, i + 1):
                    matched = True
                    i += len(tag) + 1  # move past the \tag

                    # Optional argument in brackets
                    if i < len(content) and content[i] == "[":
                        end_opt = find_ending_brace(content, i)
                        if end_opt == -1:
                            break
                        i = end_opt + 1

                    # Required argument in braces
                    if i < len(content) and content[i] == "{":
                        end_brace = find_ending_brace(content, i)
                        if end_brace == -1:
                            break
                        inner = content[i+1:end_brace]
                        if not remove_inner:
                            # Clean inner content recursively (but don't keep braces)
                            cleaned_inner = remove_unnecessary_tags(inner, tag_types)
                            result += cleaned_inner
                        # Whether inner is removed or not, skip the entire {...}
                        i = end_brace + 1
                    break
            if not matched:
                result += content[i]
                i += 1
        else:
            result += content[i]
            i += 1
    return result


def parse_sections(content: str) -> Dict[str, str]:
    '''
    This tool is a classical python method. 
    - Reads tex code, identifies \section{...} tags
    - Extracts all content in these tags
    - Returns dict, keys are section names, values are belonging tex code
    '''

    section_pattern =  r'\\section\{((?:[^{}]|\{[^{}]*\})*)\}' ## can handle one-level recursion


    # Find all section headers with their start positions
    matches = list(re.finditer(section_pattern, content))

    sections = {}

    for i, match in enumerate(matches):
        section_title = match.group(1).strip()
        start_pos = match.end()

        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        section_content = content[start_pos:end_pos].strip()
        sections[section_title] = section_content

    return sections

def parse_subheadings(content: str) -> Dict[str, List[Dict]]:
    '''
    parse subheadings of section in 'content' into structured json of segmented latex code
    No llm in this step
    '''
    # Pattern to match \resumeSubHeading{...}
    heading_pattern = r'\\resumeSubheading(.*?)\\resumeItemListStart'
    # Pattern to match \resumeItemListStart followed by any content until \resumeItemListEnd
    item_list_pattern = r'\\resumeItemListStart(.*?)\\resumeItemListEnd'

    # Find all headings and their positions
    headings = [(m.group(1), m.start()) for m in re.finditer(heading_pattern, content, re.DOTALL)]
    # Find all item lists and their positions
    item_lists = [(m.group(1).strip(), m.start()) for m in re.finditer(item_list_pattern, content, re.DOTALL)]
    if len(headings) == 0:
        return parse_resumeitems(content)

    # Organize item_lists under their most recent preceding heading
    result = defaultdict(list)
    heading_idx = 0

    for item_content, item_pos in item_lists:
        # Move to the latest heading that comes before this item list
        while heading_idx + 1 < len(headings) and headings[heading_idx + 1][1] < item_pos:
            heading_idx += 1
        current_heading = headings[heading_idx][0]
        subsection = item_content.strip()
        subsection_resumeitem_split = parse_resumeitems(content=subsection)
        result[current_heading] += subsection_resumeitem_split

    return dict(result)

def parse_resumeitems(content: str) -> List[str]:
    '''
    Takes a block of LaTeX content and returns a list of strings inside each \resumeItem{...} block.
    Ignores all other content.
    '''
    items = []
    tag = "\\resumeItem{"
            
    i = 0

    while i < len(content):
        start = content.find(tag, i)
        if start == -1:
            break
        brace_start = start + len(tag) - 1  # index of the opening {
        brace_end = find_ending_brace(content, brace_start)
        item_content = content[brace_start + 1: brace_end].strip()
        items.append(item_content)
        i = brace_end + 1

    return items
    

##
## --- LLMChains ---
##

## INCOMING, V1 will only use the structured json parsed from .tex, with no LLM insights
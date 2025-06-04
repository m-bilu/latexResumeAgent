'''
This file contains all tools for edit_resume node
Tools can include python methods, LLMChains, independent sub-Agents
'''

import re

def get_latex_no_comments(latex: str) -> str:
    """
    Takes in a LaTeX string, returns the string with all comments removed.

    Removes:
    - Any content from `%` to the end of the line (if no second `%`)
    - Any content between two `%` symbols on the same line
    Ignores escaped percent signs (i.e., \%).
    """
    print('removing comments ...')
    def remove_comment_blocks(line):
        # Skip escaped percent signs
        parts = re.split(r'(?<!\\)%', line)
        result = ""
        i = 0
        while i < len(parts):
            result += parts[i]
            if i + 1 < len(parts):
                # Peek ahead to see if there's a second unescaped %
                if "%" in parts[i + 1]:
                    # Remove up to next %, continue after that
                    next_parts = parts[i + 1].split("%", 1)
                    if len(next_parts) == 2:
                        result += next_parts[1]
                        i += 2
                        continue
                # Otherwise stop at first %
                break
            i += 1
        return result.strip()

    lines = latex.splitlines()
    cleaned = [remove_comment_blocks(line) for line in lines]
    return str("\n".join(cleaned))


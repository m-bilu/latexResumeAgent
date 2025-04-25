'''
holds constants used in nodes .py files
'''
from langchain.prompts import PromptTemplate

##
## --- PARSE_RESUME CONSTANTS --- ##
## 

TAG_TYPES = [
    ('href', True), 
    ('textbf', False), 
    ('textcolor', True), 
    ('large', False), 
    ('medium', False), 
    ('small', False), 
    ('underline', False),
    ('vspace', True),
    ('resumeItemListStart', False)
    ]


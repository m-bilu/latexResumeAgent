'''
holds constants used in nodes .py files
'''
from langchain.prompts import PromptTemplate
from langchain_cohere import ChatCohere

##
## --- LLM INIT --- ##
##

llm = ChatCohere(model="command-a-03-2025", temperature=0)

##
## --- PARSE_JD CONSTANTS --- ##
##

targets = {

    'role_summary' :  ' A short summary of what the role is about. 2-3 sentences. Do not exceed this sentence range.',
    'must_have_skills' :  '(list of words): Technologies, tools, or skills explicitly marked as required or essential. If some resume did not have them, it would be at a disadvantage.',
    'nice_to_have_skills' : '(list of words): Skills that are mentioned as optional, preferred, or bonuses. This skills push a good candidate past other good candidates, and takes probability of interview from high to 100%.',
    'responsibilities' : '(list of words): Key tasks the candidate will be responsible for. Imagine that a given resume is good for this role, then it SHOULD be able to fulfil these responsibilities.',
    'keywords' : '(list of words): Domain-specific phrases, concepts, tools, or responsibilities relevant for tailoring a resume (e.g. "fraud detection", "AWS", "real-time systems").',
    'specific_technologies' :  '(list of words): All the technologies, tools and technical workflows, platforms mentioned in the job description.',
    'general_technologies' : '(list of words): More general technicals things someone should demonstrate, according to this job description. Being able to build a certain type of technical product (data pipeline, web app), solve a certain type of technical problem.',
    'years_of_experience' : 'How many years of experience needed to be reasonably considered for this job. For each type of experience, give a range, with a lower limit and upper limit. Initially mentioned the required, then the preferred.'

}



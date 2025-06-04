'''
Author: Muhammad Bilal Khan
Date: April 20 2025

This script runs an instance of the LatexResumeAgent, passing args for 
    job description (jd) and latex resume
'''
import sys
import json

from graph import init_agent

if __name__ == '__main__':

    print('\nInitiating Agent ...\n <--------------------------------------->')

    with open(sys.argv[1], "r", encoding="utf-8") as tex:
        with open(sys.argv[2], "r", encoding="utf-8") as jdtxt:
            texstring = tex.read()
            jdstring = jdtxt.read()
            
            ## --- Invoking Graph Agent --- ##
            agent = init_agent()
            result = agent.invoke({ 'resume' : texstring, 'jd' : jdstring })
            print(result['new_resume'] if 'new_resume' in result else 'No New Resume')

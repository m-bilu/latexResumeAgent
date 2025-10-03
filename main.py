'''
Author: Muhammad Bilal Khan
Date: April 20 2025

This script runs an instance of the LatexResumeAgent, passing args for
    job description (jd) and latex resume
'''
import sys
import json
import pdfplumber

from graph import modify_resume

if __name__ == '__main__':

    print('\nInitiating Agent ...\n <--------------------------------------->')

    with pdfplumber.open(sys.argv[1]) as resume:
        with open(sys.argv[2], "r", encoding="utf-8") as jdtxt:
            resumestring = resume.pages[0].extract_text()
            jdstring = jdtxt.read()

            ## --- Invoking Graph Agent --- ##
            new_resume=modify_resume(resumestring, jdstring)
            print(new_resume if new_resume else 'No New Resume')

import json
import os.path

from constants import START_PAGE, SAVE_PATH_OF_SOLVABLE_LEVELS
from utils import SoupGetter

if os.path.exists(SAVE_PATH_OF_SOLVABLE_LEVELS):
    with open(SAVE_PATH_OF_SOLVABLE_LEVELS, 'r') as fin:
        solvable_packs = json.load(fin)
else:
    print(f"No solvable level json detected at {SAVE_PATH_OF_SOLVABLE_LEVELS}.\nYou need to run pack_scraper first!")


def scrape_alpha_beta(model, level, get_question=True, get_steps=True, get_explanation=True, get_images=False):
    soup = model(level)[0]
    # Get Question #
    if get_question:
        try:
            question = soup.find_all(name='div', attrs={'class': 'pi-data-value pi-font'})[0].text
        except:
            try:
                question = soup.find(name='div', attrs={'class': 'mw-parser-output'}).find_next('p').text.split('Instruction:')[-1]
                question = question.strip()
                print(question)
            except:
                print(f"Error at level: {level}")
            pass
    else:
        question = None

    # Get Everything Else #
    solutions = []
    sections = soup.find_all('span', attrs={'class': 'mw-headline'})
    tutorial_exists = 0
    solution_exists = 0
    explanation_exists = 0
    for f in sections:
        if 'Tutorial' in f.text:
            tutorial_exists += 1
        if (('Solution' in f.text or 'solution' in f.text) and
                'Solutions' not in f.text and
                'Explanation' not in f.text and
                'Explanations' not in f.text and
                'From' not in f.text and
                'from' not in f.text
        ):
            print("Found a solution!")
            solution_exists += 1
        if 'Explanation' in f.text:
            print("Found an explanation!")
            explanation_exists += 1

    if get_steps:
        text_sections = soup.find_all('ol')
        if len(text_sections) != tutorial_exists + solution_exists:
            print(f"Error at level: {level}")
        if tutorial_exists > 0:
            text_sections = text_sections[tutorial_exists:]

        for i in range(min(solution_exists, len(text_sections))):
            solutions.append(text_sections[i].text)
    else:
        solutions = []

    if get_explanation:
        if explanation_exists > 0:
            explanation = sections[-1].find_next("p")
            if explanation:
                explanation = explanation.text
        else:
            explanation = None
    else:
        explanation = None

    return question, solutions, explanation


def scrape_levels_up_to_theta(model, level, get_question=True, get_steps=True, get_explanation=True, get_images=False):
    soup = model(level)[0]
    # Get Question #
    if get_question:
        try:
            question = soup.find_all(name='div', attrs={'class': 'pi-data-value pi-font'})[0].text
        except:
            # Mobile Only #
            question = None
    else:
        question = None

    # Get Everything Else #
    solutions = []
    sections = soup.find_all('span', attrs={'class': 'mw-headline'})
    tutorial_exists = 0
    solution_exists = 0
    explanation_exists = 0
    for f in sections:
        if 'Tutorial' in f.text:
            tutorial_exists += 1
        if (('Solution' in f.text or 'solution' in f.text) and
                'Solutions' not in f.text and
                'Explanation' not in f.text and
                'Explanations' not in f.text and
                'From' not in f.text and
                'from' not in f.text
        ):
            print("Found a solution!")
            solution_exists += 1
        if 'Explanation' in f.text:
            print("Found an explanation!")
            explanation_exists += 1

    if get_steps:
        text_sections = soup.find_all('ol')
        if len(text_sections) != tutorial_exists + solution_exists:
            print(f"Error at level: {level}")
        if tutorial_exists > 0:
            text_sections = text_sections[tutorial_exists:]

        for i in range(min(solution_exists, len(text_sections))):
            solutions.append(text_sections[i].text)
    else:
        solutions = []

    if get_explanation:
        if explanation_exists > 0:
            explanation = sections[-1].find_next("p")
            if explanation:
                explanation = explanation.text
        else:
            explanation = None
    else:
        explanation = None

    return question, solutions, explanation


model = SoupGetter(post_process_func=None)
#model.load_selenium()
for pack in solvable_packs:
    scrape_index = 0
    max_scrape_index = len(solvable_packs[pack])
    for level in solvable_packs[pack]:
        print(f"Scraping {scrape_index}/{max_scrape_index} levels of pack {pack}...")
        scrape_alpha_beta(model, level)
        scrape_index += 1

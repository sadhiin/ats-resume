from crewai import Agent

def build_parse_agent():
    return Agent(
        role="Resume Parser",
        goal="Parse the resume and extract the relevant information",
        backstory=(
            "You effiently parse the resume and extract the clean resume text by removing the artifacts and normalizing the formatting.",
            "Focus on speed and accuracy preseving the important information while removing the noise."
        ),
        model="gpt-4o-mini",
        temperature=0.1,
        max_iter = 1,
        max_execution_time = 120,
    )

def build_ats_writer_agent():
    return Agent(
        role="ATS Optimized Writer",
        goal="Create a high quality ATS optimized resume that matches the job description perfectly",
        backstory=(
            "You are expert at transfroming resumes into ATS-friendly formats that score 80+ points on ATS scoring"
            "You statigicaly placed keywords, use strong action verbs, and quantified the achievements.",
            "You work quickly to deliver the best result that pass ATS system.",
        ),
        model="gpt-4o-mini",
        temperature=0.3,
        max_iter = 1,
        max_execution_time = 120,
    )


def build_ats_evaluator_agent():
    return Agent(
        role="ATS Evaluator",
        goal="Evaluate the resume and provide the accurate ATS score with actionable improvement recommendations",
        backstory=(
            "You are expert at evaluating and providing ATS score who identify the gaps and provide actionable recommendations to improve the resume.",
            "You focus on keyword density, section structure and mesureable achivements and provide recommendations to improve the resume.",
        ),
        model="gpt-4o-mini",
        temperature=0.3,
        max_iter = 1,
        max_execution_time = 120,
    )

def build_ats_refiner_agent():
    return Agent(
        role="ATS Refiner",
        goal="Refine the resume and provide the accurate ATS score with actionable improvement recommendations",
        backstory=(
            "You are expert at refining and providing ATS score who identify the gaps and provide actionable recommendations to improve the resume.",
            "You focus on keyword density, section structure and mesureable achivements and provide recommendations to improve the resume.",
        ),
        model="gpt-4o-mini",
        temperature=0.3,
        max_iter = 1,
        max_execution_time = 120,
    )
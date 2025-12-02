import os
from crewai import Crew, Process

from .agents import (
    build_ats_evaluator_agent,
    build_ats_writer_agent,
    build_ats_refiner_agent,
    build_parse_agent,
)

from .task import (
    parse_resume_task,
    rewrite_for_ats_task,
    refine_bulet_task,
    evaluation_ats_task,
)
from config import settings

def build_crew(raw_resume_text, job_description, job_title):

    parser = build_parse_agent()
    ats_writer = build_ats_writer_agent()
    ats_refiner = build_ats_refiner_agent()
    ats_evaluator = build_ats_evaluator_agent()


    t_parse = parse_resume_task(parser, raw_resume_text)
    t_ats_writer = rewrite_for_ats_task(ats_writer, t_parse.output, job_description, job_title)
    t_ats_refiner = refine_bulet_task(ats_refiner, t_ats_writer.output)
    t_ats_evaluator = evaluation_ats_task(ats_evaluator, t_ats_refiner.output, job_title, job_description)
    crew = Crew(
        name="ATS Optimizer Crew",
        description="A crew of agents that can optimize a resume for ATS",
        agents=[parser, ats_writer, ats_refiner, ats_evaluator],
        tasks=[t_parse, t_ats_writer, t_ats_refiner, t_ats_evaluator],
        process=Process.sequential,
        verbose=True,
    )

    return crew
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
from .config import settings


def build_crew(raw_resume_text, job_description, job_title):
    parser = build_parse_agent()
    ats_writer = build_ats_writer_agent()
    ats_refiner = build_ats_refiner_agent()
    ats_evaluator = build_ats_evaluator_agent()

    t_parse = parse_resume_task(parser, raw_resume_text)
    t_ats_writer = rewrite_for_ats_task(
        ats_writer, t_parse.output, job_description, job_title)

    t_ats_refiner = refine_bulet_task(ats_refiner, t_ats_writer.output)
    t_ats_evaluator = evaluation_ats_task(
        ats_evaluator, t_ats_refiner.output, job_title, job_description
    )
    crew = Crew(
        name="ATS Optimizer Crew",
        description="A crew of agents that can optimize a resume for ATS",
        agents=[parser, ats_writer, ats_refiner, ats_evaluator],
        tasks=[t_parse, t_ats_writer, t_ats_refiner, t_ats_evaluator],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def run_pipeline(raw_resume_text, job_description, job_title):
    # crew = build_crew(raw_resume_text, job_description, job_title)
    # result = crew.run()
    # return result

    # Build agents
    parser = build_parse_agent()
    writer_agent = build_ats_writer_agent()
    refiner_agent = build_ats_refiner_agent()
    evaluator_agent = build_ats_evaluator_agent()

    # create task
    t_parse = parse_resume_task(parser, raw_resume_text)
    parser_crew = Crew(
        agents=[parser],
        tasks=[t_parse],
        process=Process.sequential,
        verbose=True,
    )
    parser_result = parser_crew.kickoff()
    parser_result = str(parser_result).strip()

    t_re_writer = rewrite_for_ats_task(
        writer_agent, parser_result, job_description, job_title
    )
    rewriter_crew = Crew(
        agents=[writer_agent],
        tasks=[t_re_writer],
        process=Process.sequential,
        verbose=True,
    )
    rewriter_result = rewriter_crew.kickoff()
    rewriter_result = str(rewriter_result).strip()

    t_ats_refiner = refine_bulet_task(refiner_agent, rewriter_result)
    refiner_crew = Crew(
        agents=[refiner_agent],
        tasks=[t_ats_refiner],
        process=Process.sequential,
        verbose=True,
    )
    refiner_result = refiner_crew.kickoff()
    final_resume = str(refiner_result).strip()
    t_ats_evaluator = evaluation_ats_task(
        evaluator_agent, final_resume, job_title, job_description
    )
    evaluator_crew = Crew(
        agents=[evaluator_agent],
        tasks=[t_ats_evaluator],
        process=Process.sequential,
        verbose=True,
    )
    evaluation_result = evaluator_crew.kickoff()
    evaluation_result = str(evaluation_result).strip()

    return {
        "rewritten_resume": rewriter_result,
        "refined_resume": refiner_result,
        "optimized_resume": final_resume,
        "evaluation": evaluation_result,
    }

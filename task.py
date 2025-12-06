from crewai import Task

def parse_resume_task(agent, raw_resume_text):
    
    truncated_resume_text = raw_resume_text[:10000] if len(raw_resume_text) > 1000 else raw_resume_text
    return Task(
        agent=agent,
        description=f"""
            Clear the following text quickly: {truncated_resume_text}

            Remove artifacts, normalized formatting, bulet points to '-' keep all the content be fast and direct
        """,
        expected_output="Clear resume text with proper structure"
    )


def rewrite_for_ats_task(agent, cleaned_resume_text, job_description, job_title):
    truncated_resume_text = cleaned_resume_text[:10000] +"..." if len(cleaned_resume_text) > 1000 else cleaned_resume_text
    truncated_job_description = job_description[:10000] +"..." if len(job_description) > 1000 else job_description
    return Task(
        agent=agent,
        description=f"""
            Rewrite the following resume for job {job_title} with job description \n\n{truncated_job_description}\n\n
            Resume: {truncated_resume_text}\n\n
            Rewrite the resume text for ATS
            Match the keywords use action verbs add metircs, Terget 80+ ATS score. Be direct and fast
        """,
        expected_output="Ats optimized resume with keyword placement and metrics"
    )


def refine_bulet_task(agent, rewritten_resume_text):
    truncated_resume_text = rewritten_resume_text[:10000] +"..." if len(rewritten_resume_text) > 1000 else rewritten_resume_text
    return Task(
        agent=agent,
        description=f"""
            Plished those bulet points with action verbs and metrics: \n\n{truncated_resume_text}\n\n
            Add strong verbs and numbers. Be direct and fast
        """,
        expected_output="Resume with enhanced bullet points and metrics"
    )

def evaluation_ats_task(agent, final_resume_text, job_title, job_description):
    truncated_resume_text = final_resume_text[:10000] +"..." if len(final_resume_text) > 1000 else final_resume_text
    truncated_job_description = job_description[:10000] +"..." if len(job_description) > 1000 else job_description

    return Task(
        agent=agent,
        description=f"""
            Evaluate and score the resume for job {job_title} with job description \n\n{truncated_job_description}\n\n
            Resume: {truncated_resume_text}\n\n
            Evaluate the resume text for ATS and provide the score
            Rate 1-5: keywords, structure, metrics, verbs, format. Return Json with overall score (0-100) breakdown of the gaps
        """,
        expected_output="ATS score and recommendations"
    )
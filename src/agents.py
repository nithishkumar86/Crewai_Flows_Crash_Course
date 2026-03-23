from crewai import Agent,Task,LLM

def agent1(llm)->Agent:
    return Agent(
        role="Senior Research Analyst",
        goal=(
            "Produce accurate, structured, and up-to-date research that can be directly "
            "used by a writer to create a high-quality blog."
        ),
        backstory=(
            "You are a professional research analyst with experience in analyzing complex topics, "
            "fact-checking information, and organizing insights into structured notes."
        ),
        llm=llm,
        max_tokens=500,
        verbose=True,
    )

def agent2(llm)->Agent:
    return Agent(
        role="Expert Blog Writer",
        goal=(
            "Write an engaging, well-structured, and informative blog using provided research. "
            "Ensure clarity, readability, and logical flow."
        ),
        backstory=(
            "You are a professional content writer specializing in long-form blogs. "
            "You write with a clear introduction, strong body sections, and a concise conclusion. "
            "You adapt tone based on audience and incorporate feedback effectively."
        ),
        llm=llm,
        max_tokens=500,
        verbose=True,
    )
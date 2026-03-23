from crewai import Crew, Task, LLM
from crewai.flow.flow import Flow, listen, start
from crewai.flow import (
    Flow,
    start,
    listen,
    human_feedback,
    HumanFeedbackProvider,
    HumanFeedbackPending,
    PendingFeedbackContext,
    HumanFeedbackResult
)
from src.agents import agent1,agent2
from src.webhook import WebhookProvider          # ← clean import
from src.state import BlogState
import os
from dotenv import load_dotenv
load_dotenv()



MAX_ITERATIONS = 3
class BlogFlow(Flow[BlogState]):

    llm = LLM(model="groq/llama-3.3-70b-versatile")

    researcher_agent = agent1(llm=llm) 
    writer_agent = agent2(llm=llm)

    # ── Step 1: Entry point ───────────────────
    @start()
    def get_topic(self):
        print(f"\n📝 Topic: {self.state.topic}\n")
        return self.state.topic

    # ── Step 2: Crew runs here ONLY ───────────
    @listen(get_topic)
    def generate_blog(self, topic):

        self.state.iteration += 1
        print(f"\n🔁 Iteration: {self.state.iteration}\n")

        research_task = Task(
            description=f"""
            Research the topic: {topic}
            Provide key concepts, insights, real-world examples, and trends.
            Output should be well-structured notes.
            """,
            expected_output="Structured research notes",
            agent=self.researcher_agent,
        )

        writer_task = Task(
            description=f"""
            Write a high-quality blog on: {topic}

            Requirements:
            - Clear introduction
            - Sections with headings
            - Simple, engaging explanations
            - Real-world relevance
            - Strong conclusion

            {"Incorporate this revision feedback: " + self.state.feedback if self.state.feedback else ""}

            Iteration: {self.state.iteration}
            """,
            expected_output="Final blog article",
            agent=self.writer_agent,
        )

        crew = Crew(
            agents=[self.researcher_agent, self.writer_agent],
            tasks=[research_task, writer_task],
            verbose=True,
        )
        crew.kickoff()

        self.state.blog = writer_task.output.raw
        print("\n📄 Blog generated\n")
        return self.state.blog

    # ── Step 3: HITL node ONLY ────────────────
    @listen(generate_blog)
    @human_feedback(
        message="Review the blog. Type 'approved' or provide revision feedback:",
        emit=["approved", "needs_revision"],
        llm=llm,
        default_outcome="needs_revision",
        provider=WebhookProvider(),               # ← clean, from provider.py
    )
    def review_blog(self, blog):
        return self.state.blog

    # ── Step 4: Approved ──────────────────────
    @listen("approved")
    def on_approved(self, result: HumanFeedbackResult):
        self.state.approved = True
        print("\n✅ Blog Approved!\n")

    # ── Step 5: Needs revision → loop back ────
    @listen("needs_revision")
    def on_needs_revision(self, result: HumanFeedbackResult):
        self.state.feedback = result.feedback
        self.state.approved = False

        print(f"\n🛠 Feedback: {self.state.feedback}\n")

        if self.state.iteration >= MAX_ITERATIONS:
            print(f"\n⚠ Max revisions reached. Saving last version.\n")
            self.state.approved = True
            return

        print("🔁 Regenerating with feedback...\n")
        return self.generate_blog(self.state.topic)
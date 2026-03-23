from crewai.flow import (
    Flow,
    start,
    listen,
    human_feedback,
    HumanFeedbackProvider,
    HumanFeedbackPending,
    PendingFeedbackContext,
)


class WebhookProvider(HumanFeedbackProvider):

    def request_feedback(self, context: PendingFeedbackContext, flow) -> str:

        raise HumanFeedbackPending(
            context=context,
            callback_info={
                "webhook_url": f"http://localhost:8000/feedback/{context.flow_id}"
            }
        )
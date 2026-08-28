"""
Groq service for communicating with the Groq API.

This module is responsible for:
- Initializing the Groq client
- Managing conversation context
- Sending requests to Groq
- Streaming AI responses
- Handling API errors
"""

from groq import Groq

from config import GROQ_API_KEY
from utils.logger import logger


class GroqService:
    """Handle communication with the Groq API."""

    # =================================================
    # CONTEXT SETTINGS
    # =================================================

    # Groq account currently allows 8000 tokens/minute.
    # We intentionally keep requests below that limit.
    MAX_INPUT_TOKENS = 6000

    # Rough estimation:
    # 1 token ≈ 4 characters for normal English text.
    CHARS_PER_TOKEN = 4

    def __init__(self):
        """Initialize the Groq API client."""

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    # =================================================
    # TOKEN ESTIMATION
    # =================================================

    def estimate_tokens(self, text):
        """
        Estimate the number of tokens in a text.

        This is an approximation, not an exact tokenizer.
        It is used to keep requests safely below the API limit.
        """

        if not text:
            return 0

        return max(
            1,
            len(text) // self.CHARS_PER_TOKEN
        )

    # =================================================
    # BUILD CONTEXT
    # =================================================

    def build_context(
        self,
        messages,
        system_prompt
    ):
        """
        Build a conversation context that fits within
        the configured token budget.

        Recent messages are prioritized.

        The UI still keeps the complete conversation.
        Only the messages sent to Groq are trimmed.
        """

        system_tokens = self.estimate_tokens(
            system_prompt
        )

        available_tokens = (
            self.MAX_INPUT_TOKENS
            - system_tokens
        )

        selected_messages = []
        used_tokens = 0

        # Start from newest message and move backwards.
        for message in reversed(messages):

            content = message.get(
                "content",
                ""
            )

            message_tokens = self.estimate_tokens(
                content
            ) + 4  # small role/message overhead

            # Stop before exceeding budget.
            if (
                used_tokens + message_tokens
                > available_tokens
            ):
                break

            selected_messages.insert(
                0,
                message
            )

            used_tokens += message_tokens

        logger.info(
            "Context prepared: "
            f"{len(selected_messages)}/{len(messages)} messages, "
            f"approximately {used_tokens + system_tokens} tokens."
        )

        return selected_messages

    # =================================================
    # STREAM RESPONSE
    # =================================================

    def stream_response(
        self,
        messages,
        system_prompt,
        model,
        temperature
    ):
        """
        Generate and stream an AI response from Groq.

        Args:
            messages (list):
                Complete conversation history.

            system_prompt (str):
                Instructions defining AI behavior.

            model (str):
                Groq model.

            temperature (float):
                Controls response variability.

        Yields:
            str:
                Individual response chunks.
        """

        # =================================================
        # PREPARE CONTEXT
        # =================================================

        context_messages = self.build_context(
            messages=messages,
            system_prompt=system_prompt
        )

        # =================================================
        # BUILD API MESSAGES
        # =================================================

        api_messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            *context_messages
        ]

        logger.info(
            "Sending request to Groq. "
            f"Model={model}, "
            f"Messages={len(api_messages)}"
        )

        # =================================================
        # API REQUEST + STREAM
        # =================================================

        try:

            response = self.client.chat.completions.create(
                model=model,
                messages=api_messages,
                temperature=temperature,
                stream=True
            )

            for chunk in response:

                if not chunk.choices:
                    continue

                content = (
                    chunk.choices[0]
                    .delta
                    .content
                )

                if content:
                    yield content

            logger.info(
                "AI streaming response completed successfully."
            )

        except Exception as error:

            logger.exception(
                "Groq streaming request failed."
            )

            raise error
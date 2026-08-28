"""
Groq service for communicating with the Groq API.

This module is responsible for:
- Initializing the Groq client
- Sending conversation history to the Groq API
- Streaming AI responses
- Handling API errors
"""

import time

from groq import Groq

from config import GROQ_API_KEY
from utils.logger import logger


class GroqService:
    """Handle communication with the Groq API."""

    def __init__(self):
        """Initialize the Groq API client."""

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing from environment variables."
            )

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

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
                Conversation history.

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

        api_messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            *messages
        ]

        logger.info(
            "Sending request to Groq. "
            f"Model={model}, "
            f"Messages={len(api_messages)}"
        )

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

                content = chunk.choices[0].delta.content

                if content:
                    yield content

                    # Small delay for smoother UI streaming
                    time.sleep(0.01)

            logger.info(
                "AI streaming response completed successfully."
            )

        except Exception as error:

            logger.exception(
                "Groq streaming request failed."
            )

            # IMPORTANT:
            # Raising the error allows app.py to display it.
            raise error
"""
Groq service for communicating with the Groq API.

This module handles AI-related operations for the chatbot.
It keeps API communication separate from the Streamlit UI.
"""

from groq import Groq

from config import GROQ_API_KEY


class GroqService:
    """Handle communication with the Groq API."""

    def __init__(self):
        """Initialize the Groq API client."""

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
        Stream an AI-generated response from Groq.

        Args:
            messages (list): Conversation history.

            system_prompt (str): Instructions defining
                the AI's behavior.

            model (str): Groq model used for generation.

            temperature (float): Controls response variability.

        Yields:
            str: Individual pieces of the AI response.
        """

        api_messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            *messages
        ]

        response = self.client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=temperature,
            stream=True
        )

        for chunk in response:

            content = chunk.choices[0].delta.content

            if content:
                yield content
"""
Application-wide logging configuration.

This module provides a reusable logger for recording
application events, warnings, and errors.
"""

import logging
import os


# =====================================================
# LOG DIRECTORY
# =====================================================

os.makedirs(
    "logs",
    exist_ok=True
)


# =====================================================
# LOGGER
# =====================================================

logger = logging.getLogger(
    "ai_chat_assistant"
)

logger.setLevel(
    logging.INFO
)


# =====================================================
# CONFIGURE LOGGER
# =====================================================

if not logger.handlers:

    file_handler = logging.FileHandler(
        "logs/app.log",
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )
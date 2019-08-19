"""Slack logging."""

import logging

import slack


class SlackLogHandler(logging.Handler):
    """Slack logging handler."""

    def __init__(self, token: str, channel: str) -> None:
        """Construct a Slack logging Handler."""
        super().__init__()
        self.slack = slack.WebClient(token=token)
        self.channel = channel

    def emit(self, record: logging.LogRecord) -> None:
        """Send a log message."""
        self.slack.chat_postMessage(channel=self.channel, text=record.getMessage())

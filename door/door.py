"""Door handler."""

import os
import logging
import threading
from typing import Dict, Optional

import slack

from interface import DoorInterface
from database import CardEntry, database
from slacklog import SlackLogHandler

SlackAPIMessageType = Dict[str, Dict[str, str]]

_DOOR_CHANNEL = "GMHU15PC7"

logging.basicConfig(format="%(asctime)-15s [%(levelname)s %(name)s] %(message)s")
log = logging.getLogger("door")
log.setLevel(logging.DEBUG)

slacklog = SlackLogHandler(os.environ["SLACK_API_TOKEN"], _DOOR_CHANNEL)
slacklog.setLevel(logging.INFO)
log.addHandler(slacklog)


class Door:
    """High-level door code."""

    door: DoorInterface
    add_next_card: Optional[str]
    slack: slack.WebClient

    def __init__(self) -> None:
        """Construct a door."""
        self.door = DoorInterface()
        self.door_thread = threading.Thread(target=self.door_handler, daemon=True)
        self.add_next_card = None
        self.slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    def door_handler(self) -> None:
        """Door checking thread."""
        try:
            door = DoorInterface()
            while True:
                log.debug("Waiting for card")
                card = door.get_card()
                log.debug("Scanned: %s", card)
                entry = database.get(card)
                if entry:
                    log.info("Opening door for: %s", entry.name)
                    door.open()
                elif self.add_next_card:
                    log.info("Adding card %s for %s", card, self.add_next_card)
                    database.add(CardEntry(self.add_next_card, card))
                    database.commit()
                    self.add_next_card = None
                else:
                    log.info("Rejected %s", card)
                    self.door.flash_red()
        except Exception:
            # Blow everything up if we crash
            os._exit(0)
            raise

    def start(self) -> None:
        """Start door thread."""
        self.door_thread.start()

    def handle_message(self, payload: SlackAPIMessageType) -> None:
        """Handle a chat message."""
        if payload["data"]["channel"] == _DOOR_CHANNEL and "text" in payload["data"]:
            text = payload["data"]["text"]
            thread = payload["data"].get("thread_ts") or payload["data"].get("ts")
            if text == "!ping":
                self.slack.chat_postMessage(channel=_DOOR_CHANNEL, text="pong", thread_ts=thread)
            elif text == "!unlock":
                self.door.open()
                self.slack.chat_postMessage(channel=_DOOR_CHANNEL, text="Opened", thread_ts=thread)
                log.debug("Opening from slack")
            elif text.startswith("!add "):
                self.add_next_card = text.split(" ", 1)[1]
                log.debug("Adding next card for %s", self.add_next_card)
                self.slack.chat_postMessage(channel=_DOOR_CHANNEL,
                                            text=f"Adding next card for {self.add_next_card}",
                                            thread_ts=thread)


@slack.RTMClient.run_on(event='message')  # type: ignore
def handle_message(**payload) -> None:  # type: ignore
    """Handle a slack message event."""
    door.handle_message(payload)


def main() -> None:
    """Entrypoint."""
    database.load()
    door.start()
    rtm_client = slack.RTMClient(token=os.environ['SLACK_API_TOKEN'])
    rtm_client.start()


if __name__ == "__main__":
    door = Door()
    main()

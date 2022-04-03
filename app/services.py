import logging
from typing import Optional

from .models import db, Item

session = db.session


def get_counter() -> int:
    return Item.query.count()


def add_record(agent: str, params: Optional[str] = None, length_limit=80) -> None:
    if params and len(params) > length_limit:
        logging.warning(
            "Shortening 'params' from %d to %d characters. Original text: %s",
            len(params), length_limit, params
        )
        params = params[:length_limit]
    if len(agent) > length_limit:
        logging.warning(
            "Shortening 'agent' from %d to %d characters. Original text: %s",
            len(agent), length_limit, agent
        )
        agent = agent[:length_limit]

    item = Item(agent=agent, params=params)
    session.add(item)
    session.commit()

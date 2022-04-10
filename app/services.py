import csv
import logging
from typing import List, Optional, TextIO

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


def clear_all() -> int:
    n_items = get_counter()
    logging.warning("Removing %d entries", n_items)
    Item.query.delete()
    session.commit()
    return n_items


def get_last_record() -> Optional[Item]:
    item = Item.query.order_by(Item.item_id.desc()).first()
    return item


def get_last_records(n_records: Optional[int] = None) -> List[Item]:
    query = Item.query.order_by(Item.item_id.desc())
    if n_records is not None:
        query = query.limit(n_records)
    return query.all()


def dump_records(records: List[Item], file: TextIO) -> None:
    writer = csv.writer(file)
    writer.writerow(("Date", "User-agent", "Parameters"))
    writer.writerows(
        (record.date, record.agent, record.params)
        for record in records
    )

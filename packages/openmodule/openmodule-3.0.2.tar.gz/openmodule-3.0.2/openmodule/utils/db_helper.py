from sqlalchemy.orm import Session


def update_query(session: Session, query, values: dict):
    """
    in order to update via a query in sqlite we have to no synchronize the session
    after this operation all db objects are expired (same as if you access the object
    after the transaction)
    """
    res = query.update(values, synchronize_session=False)
    session.expire_all()
    return res


def delete_query(session: Session, query):
    """
    in order to delete via a query in sqlite we have to not synchronize the session
    after this operation all db objects are expired (same as if you access the object
    after the transaction)
    """
    res = query.delete(synchronize_session=False)
    session.expire_all()
    return res

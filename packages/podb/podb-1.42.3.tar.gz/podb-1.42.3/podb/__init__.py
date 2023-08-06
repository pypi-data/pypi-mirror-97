from podb.DB import DB, DBEntry

get_current_timestamp = DBEntry.get_current_timestamp

__all__ = ["DB", "DBEntry", "get_current_timestamp"]

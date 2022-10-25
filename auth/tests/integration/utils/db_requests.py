def clear_table(con):
    """Очистка базы данных"""

    con.cursor().execute(
        "delete from users;" "delete from devices;" "delete from socials"
    )
    con.commit()

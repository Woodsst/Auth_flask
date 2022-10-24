def clear_table(con):
    con.cursor().execute(
        "delete from users;" "delete from devices;" "delete from socials"
    )
    con.commit()

def columnListForSQL(column_list):
    cols = ",".join([str(i) for i in column_list])
    return cols
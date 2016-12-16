from aspects.DB import DB
from aspects.IdealAspectsDB import IdealAspectsDB


def updater(part):
    if len(part) != 0:
        arr = part.split(";")
        new_aspect = ""
        for item in arr:
            if "http" not in item:
                new_aspect += item + ";"
        new_aspect = new_aspect[0:len(new_aspect) - 1]
        return new_aspect
    return ''


ideal = IdealAspectsDB()  # aspects data base
row_aspect = ideal.cursor_aspects.execute('SELECT * FROM IdealAspects').fetchone()
count = 0
while row_aspect is not None:  # iterate through all reviews
    print(count)
    count += 1
    article = str(row_aspect[0])
    adv = str(row_aspect[1])
    dis = str(row_aspect[2])
    com = str(row_aspect[3])
    new_adv = updater(adv)
    if new_adv != adv:
        ideal.cursor_aspects_update.execute(
            'UPDATE IdealAspects SET advantageAspects = ? WHERE article = ? and advantageAspects = ?',
            (new_adv, article, adv,))
        ideal.conn_aspects.commit()
    new_dis = updater(dis)
    if new_dis != dis:
        ideal.cursor_aspects_update.execute(
            'UPDATE IdealAspects SET disadvantageAspects = ? WHERE article = ? and disadvantageAspects = ?',
            (new_dis, article, dis,))
        ideal.conn_aspects.commit()
    new_com = updater(com)
    if new_com != com:
        ideal.cursor_aspects_update.execute(
            'UPDATE IdealAspects SET commentAspects = ? WHERE article = ? and commentAspects = ?',
            (new_com, article, com,))
        ideal.conn_aspects.commit()
    row_aspect = ideal.cursor_aspects.fetchone()

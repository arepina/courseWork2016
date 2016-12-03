from aspects.AspectsDB import AspectsDB


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

aspect_db = AspectsDB()  # aspects data base
row_aspect = aspect_db.cursor_aspects.execute('SELECT * FROM Aspects').fetchone()
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
        aspect_db.cursor_aspects2.execute(
            'UPDATE Aspects SET advantageAspects = ? WHERE article = ? and advantageAspects = ?',
            (new_adv, article, adv,))
        aspect_db.commit()
    new_dis = updater(dis)
    if new_dis != dis:
        aspect_db.cursor_aspects2.execute(
            'UPDATE Aspects SET disadvantageAspects = ? WHERE article = ? and disadvantageAspects = ?',
            (new_dis, article, dis,))
        aspect_db.commit()
    new_com = updater(com)
    if new_com != com:
        aspect_db.cursor_aspects2.execute(
            'UPDATE Aspects SET commentAspects = ? WHERE article = ? and commentAspects = ?',
            (new_com, article, com,))
        aspect_db.commit()
    row_aspect = aspect_db.cursor_aspects.fetchone()

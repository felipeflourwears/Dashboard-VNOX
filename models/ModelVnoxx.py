class ModelVnoxx():
    @classmethod
    def list_players_vnoxx(cls, db, idCustomer):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idVnnox, playerId, cliente, tienda, iccid, imsi, msisdn, idCustomer
                     FROM vnoxx
                     WHERE idCustomer = %s"""
            cursor.execute(sql, (idCustomer,))
            rows = cursor.fetchall()

            # Transformar los resultados en un array de diccionarios
            array_list_players = []
            for row in rows:
                player = {
                    "idVnnox": row[0],
                    "playerId": row[1],
                    "cliente": row[2],
                    "tienda": row[3],
                    "iccid": row[4],
                    "imsi": row[5],
                    "msisdn": row[6],
                    "idCustomer": row[7]
                }
                array_list_players.append(player)

            return array_list_players
        except Exception as ex:
            raise Exception(ex)

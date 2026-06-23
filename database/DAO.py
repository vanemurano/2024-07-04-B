from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(datetime) as year
                        from sighting 
                        order by year"""
            cursor.execute(query)

            for row in cursor:
                result.append(int(row["year"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_states_for_year(year: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct st.id , st.Name , st.Capital , st.Lat , st.Lng , st.Area , st.Population , st.Neighbors 
                        from state st, sighting si
                        where st.id=si.state 
                        and year(si.datetime)=%s"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result # lista di oggetti State

    @staticmethod
    def get_all_nodes(year, state_id):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                        from sighting 
                        where year(datetime)=%s and state=%s"""

            cursor.execute(query, (year, state_id))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_edges(year, state_id, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1, s2.id as id2
                        from sighting s1
                        join sighting s2 on year(s1.datetime)=year(s2.datetime) 
                        and s1.state=s2.state and s1.id<s2.id and s1.shape=s2.shape
                        where year(s1.datetime)=%s and s1.state=%s"""

            cursor.execute(query, (year, state_id))

            for row in cursor:
                result.append((idMap[row["id1"]], idMap[row["id2"]]))
            cursor.close()
            cnx.close()
        return result # lista di tuple sighting, sighting
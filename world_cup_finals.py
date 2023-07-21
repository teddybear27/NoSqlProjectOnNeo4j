from neo4j import GraphDatabase

# Variables de connexion à la base de données Neo4j
NEO4J_URI = "neo4j+ssc://23d9ba69.databases.neo4j.io"
NEO4J_AUTH_LOGIN = "neo4j"
NEO4J_AUTH_PASSW = "hwHB4I2dkXR3q8CBAvlnjimmNYh1Ol4ezKcrqbhkILY"

URI = NEO4J_URI
LOGIN_AND_PWD = [NEO4J_AUTH_LOGIN, NEO4J_AUTH_PASSW]

# Fonction de connexion à la base de données Neo4j
def connect_to_database():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_AUTH_LOGIN, NEO4J_AUTH_PASSW))
    return driver

# Fonction pour afficher toutes les finales (années, pays, ...)
def display_all_finals(driver):
    with driver.session() as session:
        result = session.run("MATCH (f:Final) RETURN f.year, f.country, f.city")
        finals = result.values()
        for final in finals:
            print(f"Year: {final[0]}, Country: {final[1]}, City: {final[2]}")

# Fonction pour afficher toutes les équipes ayant participé aux finales
def display_all_teams(driver):
    with driver.session() as session:
        result = session.run("MATCH (t:Team)-[:PLAY_FINAL]->(f:Final) RETURN t.name")
        teams = result.values()
        for team in teams:
            print(f"Team: {team[0]}")

# Fonction pour afficher les résultats obtenus pour une équipe donnée toutes années confondues
def display_results_for_team(driver, team_name):
    with driver.session() as session:
        result = session.run(
            "MATCH (t:Team {name: $teamName})-[pf:PLAY_FINAL]->(f:Final) RETURN f.year, pf.winner",
            teamName=team_name,
        )
        results = result.values()
        for res in results:
            print(f"Year: {res[0]}, Result: {res[1]}")

# Fonction pour afficher le pays, la ville, le stade, les 2 équipes finalistes et le résultat pour une finale donnée
def display_final_details(driver, year):
    with driver.session() as session:
        result = session.run(
            "MATCH (f:Final {year: $year})-[:IN_COUNTRY]->(c:Country), (f)-[pf1:PLAY_FINAL]->(t1:Team), "
            "(f)-[pf2:PLAY_FINAL]->(t2:Team) WHERE t1 <> t2 RETURN c.name, f.city, f.stadium, t1.name, t2.name, pf1.winner",
            year=year,
        )
        details = result.values()
        for detail in details:
            print(f"Country: {detail[0]}, City: {detail[1]}, Stadium: {detail[2]}, "
                  f"Team 1: {detail[3]}, Team 2: {detail[4]}, Result: {detail[5]}")

def main():
    driver = connect_to_database()
    
    while True:
        print("Menu:")
        print("1. Afficher toutes les finales")
        print("2. Afficher toutes les équipes ayant participé aux finales")
        print("3. Afficher les résultats pour une équipe donnée")
        print("4. Afficher les détails d'une finale")
        print("5. Quitter")
        
        choice = input("Votre choix (1/2/3/4/5) : ")
        
        if choice == "1":
            display_all_finals(driver)
        elif choice == "2":
            display_all_teams(driver)
        elif choice == "3":
            team_name = input("Nom de l'équipe : ")
            display_results_for_team(driver, team_name)
        elif choice == "4":
            year = input("Année de la finale : ")
            display_final_details(driver, int(year))
        elif choice == "5":
            break
        else:
            print("Choix invalide, veuillez réessayer.")
    
    driver.close()
    print("Bye!")

if __name__ == "__main__":
    main()

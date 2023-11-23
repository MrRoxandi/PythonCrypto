import anonsign
import secrets

candidates = [anonsign.Candidate("John"),
              anonsign.Candidate("Mitch"),
              anonsign.Candidate("Mike"),
              anonsign.Candidate("Vova")]

server = anonsign.MainServerT()
users = [anonsign.User("Alice"),
         anonsign.User("Bob"),
         anonsign.User("Martion"),
         anonsign.User("Ivan"),
         anonsign.User("Vlad"),
         anonsign.User("Valerd"),
         anonsign.User("Max")]

for user in users:
    user.vote = secrets.choice(candidates)
    server.add_vote(user)

print("-" * 20)

res = server.calculate_votes(candidates)

for item in res:
    print(f"{item[0]} : [{item[1]}]")

print("Done")

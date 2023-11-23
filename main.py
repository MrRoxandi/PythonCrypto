import anonsign

candidates = [anonsign.Candidate("John"),
              anonsign.Candidate("Mitch"),
              anonsign.Candidate("Mike"),
              anonsign.Candidate("Vova")]

server = anonsign.MainServerT()
alice = anonsign.User("Alice")
bob = anonsign.User("Bob")
martin = anonsign.User("Martion")

alice.vote = candidates[3]
bob.vote = candidates[2]
martin.vote = candidates[3]
print("-" * 20)

server.add_vote(alice)
server.add_vote(bob)
server.add_vote(martin)

res = server.calculate_votes(candidates)

for item in res:
    print(f"{item[0]} : [{item[1]}]")

print("Done")

import anonsign

candidates = [anonsign.Candidate("John"),
              anonsign.Candidate("Mitch"),
              anonsign.Candidate("Mike"),
              anonsign.Candidate("Vova")]

server = anonsign.MainServerT()
alice = anonsign.User()
bob = anonsign.User()

alice.vote = candidates[3]
bob.vote = candidates[2]

server.add_vote(alice)
server.add_vote(bob)

res = server.calculate_votes([alice, bob], candidates)

for candidate in candidates:
    print(f"{candidate.name}: [{res.count(candidate)}]")

print("Done")

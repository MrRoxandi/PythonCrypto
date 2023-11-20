import anonsign

candidates = [anonsign.Candidate("John"),
              anonsign.Candidate("Mitch"),
              anonsign.Candidate("Mike"),
              anonsign.Candidate("Vova")]

server = anonsign.MainServerT()
alice = anonsign.User()

alice.vote(candidates[3])

server.vote(alice)

print(server.get_votes())
print("Done")

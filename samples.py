from backlog.model import Story, Backlog

# Stories from g27-culrepo.txt
s1 = Story("s1", {"Faculty Member"}, {"Repository", "Collection"}, {"access"},
           "As a faculty member, I want to access a collection within the repository")
s2 = Story("s2", {"Library staff"}, {"Repository", "Material"}, {"upload"},
           "As a library staff member, I want to upload material to the repository")
s3 = Story("s3", {"Library staff"}, {"Metadata"}, {"create"},
           "As a library staff member, I want to create metadata for items")

# Obtaining the empty backlog named b:
b = Backlog.empty().named_as("b")

# Promoting
b1 = ~s1
print(type(s1))
print(type(b1))

b = Backlog.empty()
b += s1
b += s2
b += s3

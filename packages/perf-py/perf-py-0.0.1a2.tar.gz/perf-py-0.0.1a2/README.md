# perf-py

A library that personally helps me understand the performance of common python code (and in turn, it might help you understand it too!)

![Python package](https://github.com/mr-uuid/perfpy/workflows/Python%20package/badge.svg)

# Todo
- [ ] Does mapping over an iterator perform better than using generators?
- [ ] Does chunking a generator affect performance?
- [ ] Does composing generators affect performance? 
- [x] Make a table of the performance of each function ...
    - [x] Open this up in a notebook!

# Personal Reminders
- To publish to pypi w/o an alpha version, push a commit with `Publish To PYPI` in its commit message.


## TODO

# Chunking and garbage collecting simultaneously 

l = list(range(100))

batchsize = 11

while len(l) > 0:
    print(l)
    print(l[:batchsize])
    del l[:batchsize]


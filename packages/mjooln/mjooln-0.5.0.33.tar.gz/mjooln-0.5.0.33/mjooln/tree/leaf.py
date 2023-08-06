from mjooln import File, Atom


class LeafError(Exception):
    pass


class Leaf(File, Atom):
    """ Existing file within a tree that follows atom naming."""

    def __init__(self, file):
        File.__init__(self)
        if not self.exists():
            raise LeafError(f'Leaf path does not exist: {self}')
        if not Atom.is_seed(self.stub()):
            raise LeafError(f'File is not leaf: {self}')
        atom = Atom.from_seed(self.stub())
        Atom.__init__(self,
                      key=atom.key(),
                      identity=atom.identity(),
                      zulu=atom.zulu())

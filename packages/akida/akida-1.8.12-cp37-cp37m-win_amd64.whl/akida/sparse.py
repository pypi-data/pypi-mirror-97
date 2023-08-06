def sparse_repr(self):
    data = "<shape=" + str(self.shape) + ", nnz=" + str(self.nnz)
    data += ", sparsity=" + format(self.sparsity, "0.2f") + ",\n"
    data += "coords=" + str(self.coords) + ",\n"
    data += "data=" + str(self.data) + ">"
    return data

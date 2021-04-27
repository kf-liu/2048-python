import logic

mat = [[0, 1, 2, 0], [4, 6, 6, 0], [8, 0, 6, 11], [12, 13, 0, 15]]
print("origin", mat)

print("reverse", logic.reverse(mat))
print("transpose", logic.transpose(mat))
print("cover_up", logic.cover_up(mat))
print("merge", logic.merge(mat, True))

# output:
# [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
# [[3, 2, 1, 0], [7, 6, 5, 4], [11, 10, 9, 8], [15, 14, 13, 12]]
# [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]
# ([[1, 2, 3, 0], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], True)
# ([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], True, 0, 0)
with open("test.txt", 'r') as test:
    # msg1 = test.readline()
    # msg2 = test.readline()
    msg1, msg2 = test.read().split("\n")

# print("[", msg1, "]")
# print("[", msg2, "]")
print(msg1)
print(msg2)

with open("test.txt", 'w') as test:
    test.write("{}\n{}".format("World", "Hello"))

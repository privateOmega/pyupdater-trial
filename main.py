import sys

total_args = len(sys.argv)
print("Total arguments passed:", total_args)

print("\nArguments passed:", end = " ")
for i in range(1, total_args):
    print(sys.argv[i], end = " ")
print("\n")

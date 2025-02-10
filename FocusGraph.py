import matplotlib.pyplot as pt

def Graph():
    file = open("focus.txt", "r")
    content = file.read()
    file.close()

    content = content.split(",")
    x1 = []
    y1 = []

    for i in range(len(content)):
        try:            
            if content[i].strip():  # Check if the string is not empty
                content[i] = float(content[i])
                y1.append(content[i])
                x1.append(i)
            else:
                print(f"Skipping empty value at index {i}.")
        except ValueError:
            print(f"ValueError: Could not convert '{content[i]}' to float.")

    print("Content:", content)
    print("X values:", x1)
    print("Y values:", y1)

    pt.plot(x1, y1, color="red", marker="o")
    pt.title("YOUR FOCUSED TIME", fontsize=16)
    pt.xlabel("Times (Hrs)", fontsize=14)
    pt.ylabel("Focus Time (Hrs)", fontsize=14)
    pt.grid()
    pt.show()

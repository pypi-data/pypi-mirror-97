import matplotlib.pyplot as plt

class Analyze():
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.time = []
        self.force = []
        self.displacement = []
        self.run = False

    def decode(self):
        if self.run == True:
            print("Data already Decoded")
            return

        self.run=True
        for line in self.file:
            line = line.rstrip().split("\t")
            try:
                line = list(map(float, line))

            except ValueError:
                continue

            self.time.append(line[0])
            self.force.append(line[1])
            self.displacement.append(line[2])


    def plot(self, x, y):
        plt.plot(x, y)
        plt.show()
        
    def plotforcevtime(self):
        if self.run == False:
            self.decode()
        
        plt.plot(self.time, self.force)
        plt.ylabel("Force (N)")
        plt.xlabel("Time (s)")
        plt.title("Force vs. Time")
        plt.show()        

    def plotdisplacementvtime(self):
        if self.run == False:
            self.decode()
        
        plt.plot(self.time, self.displacement)
        plt.ylabel("Displacement (mm)")
        plt.xlabel("Time (s)")
        plt.title("Displacement vs. Time")
        plt.show()        

    def plotforcevdisplacement(self):
        if self.run == False:
            self.decode()
        
        g = plt.figure(1)
        plt.plot(self.displacement, self.force)
        plt.ylabel("Force (N)")
        plt.xlabel("Displacement (mm)")
        plt.title("Force vs. Displacement")
        plt.show()        



#if __name__ == "__main__":
     #data = File("pilot3.dat")
     #data.decode()
     #data.plot(data.time, data.force)
       

import mesa
import random
import matplotlib.pyplot as plt

Tf=301

T=[i for i in range(Tf)]
NourritureCollectée=[0]

class Agent(mesa.Agent):
    def __init__(self,unique_id,model):
        super().__init__(unique_id,model)
        self.nourriture=0
        self.type_agent="Fourmi"
        self.intensite=1
        self.memoire=[]
    def step(self):
        #pos=random.randint(1,self.model.grid.width-1),random.randint(1,self.model.grid.height-1)
        C=self.model.grid.get_cell_list_contents([self.pos])
        for ag in C:
            if ag.type_agent=="Marqueur" and self.nourriture==1:
                ag.intensite+=1
            if ag.type_agent=="Nourriture":
                self.nourriture=1
            if ag.type_agent=="Fourmillière" and self.nourriture==1:
                self.nourriture=0
                self.memoire.append(ag.pos)
                self.model.nourriture_collectée+=1
        N=self.model.grid.get_neighbors(self.pos,True,False,1)
        L=[]
        x,y=self.pos
        if self.nourriture==0:
            for n in N:
                if n.type_agent=="Marqueur":
                    for i in range(n.intensite):
                        L.append(n.pos)
            pos=random.choice(L)
            self.memoire.append(pos)
            print(self.memoire)
            self.model.grid.move_agent(self,pos)
        else:
            pos=self.memoire.pop()
            self.model.grid.move_agent(self,pos)

class Model(mesa.Model):
    def __init__(self,N,width,height):
            self.nourriture_collectée=0
            self.num_agents=N
            self.grid = mesa.space.MultiGrid(width, height, False)
            self.schedule=mesa.time.RandomActivation(self)
            n=width*height
            pos=random.randint(0,self.grid.width-1),random.randint(0,self.grid.height-1)
            a=Agent(n+N+2,self)
            a.type_agent="Nourriture"
            self.grid.place_agent(a,pos)
            a=Agent(n+N+1,self)
            a.type_agent="Fourmillière"
            pos=self.grid.find_empty()
            self.grid.place_agent(a,pos)
            for i in range(width):
                for j in range(height):
                    a=Agent(i*width+j,self)
                    a.type_agent="Marqueur"
                    self.grid.place_agent(a,(i,j))
            for i in range(self.num_agents):
                a=Agent(n+i,self)
                a.intensite=0
                a.memoire=[pos]
                self.schedule.add(a)
                self.grid.place_agent(a,pos)
    def step(self):
        self.schedule.step()
        NourritureCollectée.append(self.nourriture_collectée)
        self.nourriture_collectée=0
        if len(NourritureCollectée)==Tf:
            plt.plot(T,NourritureCollectée)
            plt.show()

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "black",
        "Filled": "true",
        "Layer": 1,
        "r": 0.5
    }

    if agent.type_agent=="Marqueur":
        portrayal["Color"]="grey"
        portrayal["r"]=0.2
        portrayal["Layer"]=2

    if agent.type_agent=="Nourriture":
        portrayal["Shape"]="circle"
        portrayal["Color"]="red"
        portrayal["r"]=0.8
        portrayal["Layer"]=0

    if agent.type_agent=="Fourmillière":
        portrayal["Shape"]="circle"
        portrayal["Color"]="green"
        portrayal["r"]=0.8
        portrayal["Layer"]=0

    if agent.type_agent=="Fourmi" and agent.nourriture==1:
        portrayal["Color"]="blue"

    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 3, 3, 500, 500)

server = mesa.visualization.ModularServer(
    Model, [grid], "Model", {"N": 1, "width": 3, "height": 3}
)

server.port = 8622  # The default
server.launch()
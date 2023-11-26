#采用规范公式计算
import numpy as np
import matplotlib.pyplot as plt
import random
##this script is used by the fifth chapter of my master's thesis to find the optimization
##particle swarm optimization
##the inertia weight factor was modified.
def fit_fun(X):  # 适应函数
    #粒子X=[混凝土强度序号，钢管强度序号，D，t]
    Y=[0,0,0,0]
    C=[3e-7,3.35e-7,3.65e-7,4e-7,4.2e-7,4.85e-7]#候选混凝土不同强度价格C20,30,40,50,60,70
    S=[4.3175e-5,4.4745e-5,4.7100e-5,4.867e-5,5.1025e-5,5.338e-5]#候选钢管不同强度价格5500,5700,6000,6200,6500,6800,密度7.85
    L=30000#构件长度
    Y[0]=int(round(X[0],0))
    Y[1]=int(round(X[1],0))
    Y[2]=int(round(X[2],0))
    Y[3]=int(round(X[3],0))
    return np.pi*L*((Y[2]-2*Y[3])**2*C[Y[0]]/4+(Y[2]-Y[3])*Y[3]*S[Y[1]])
def cons(X): #定义约束条件，满足承载力要求
    Fc=[9.6,14.3,19.1,23.1,27.5,31.8]#C20-C70
    Fs=[235,345,390,420,460]#Q235,345,390,420,460
    Nu=24024000#设计承载力，N
    fc=Fc[int(round(X[0],0))]
    fs=Fs[int(round(X[1],0))]
    D=int(round(X[2],0))
    t=int(round(X[3],0))
    N0=GB50(fc,fs,D,t).axialCap()
    if N0>=Nu :
    #print((theta**2-3*(fl/fc)**2)-fl)
        return True
    else:
        return False
class GB50:
    def __init__(self,fc,fs,D,t):
        self.fc=fc
        self.fs=fs
        self.D=D
        self.t=t
        
        self._Carea=3.14159*(self.D-2*self.t)**2/4
        self._Sarea=3.14159*self.D**2/4-self._Carea

        self._confCo=self.fs*self._Sarea/(self.fc*self._Carea)
        # print(self._confCo)
    def stable(self):#长细比影响
        L=30000
        mu=0.5
        Le=mu*L
        L_D=Le/self.D
        if L_D>30:
            self.psi_l=1-0.115*(L_D-4)**0.5
        elif L_D<=30 and L_D>4 :
            self.psi_l=1-0.0226*(L_D-4)
        else:
            self.psi_l=1
        return self.psi_l

    def axialCap(self):
        self.stable()
        if self.fc<=50:
            alpha=2.0
        else:
            alpha=1.8
        if self._confCo<=1/(alpha-1)**2:
            N0=0.9*self._Carea*self.fc*(1+alpha*self._confCo)
            #print(N0*self.psi_l)
        else:
            N0=0.9*self._Carea*self.fc*(1+self._confCo**0.5+self._confCo)
            #print(N0*self.psi_l)
        
        return N0*self.psi_l

class Particle:
    # 初始化
    def __init__(self, x_max, max_vel, dim):
        self.__pos = [random.uniform(0, x_max[j]) for j in range(dim)]  # 粒子的位置
        self.__vel = [random.uniform(-max_vel[j], max_vel[j]) for j in range(dim)]  # 粒子的速度]
        self.__bestPos = [0.0 for i in range(dim)]  # 粒子最好的位置
        self.__fitnessValue = fit_fun(self.__pos)  # 适应度函数值

    def set_pos(self, i, value):
        self.__pos[i] = value

    def get_pos(self):
        return self.__pos

    def set_best_pos(self, i, value):
        self.__bestPos[i] = value

    def get_best_pos(self):
        return self.__bestPos

    def set_vel(self, i, value):
        self.__vel[i] = value

    def get_vel(self):
        return self.__vel

    def set_fitness_value(self, value):
        self.__fitnessValue = value

    def get_fitness_value(self):
        return self.__fitnessValue


class PSO:
    def __init__(self, dim, size, iter_num, x_max, max_vel, best_fitness_value=float('Inf'), C1=2, C2=2, W=0.8):
        self.C1 = C1
        self.C2 = C2
        self.W = W
        self.dim = dim  # 粒子的维度
        self.size = size  # 粒子个数
        self.iter_num = iter_num  # 迭代次数
        self.x_max = x_max
        self.max_vel = max_vel  # 粒子最大速度
        self.best_fitness_value = best_fitness_value
        self.best_position = [0.0 for i in range(dim)]  # 种群最优位置
        self.fitness_val_list = []  # 每次迭代最优适应值

        # 对种群进行初始化
        self.Particle_list = [Particle(self.x_max, self.max_vel, self.dim) for i in range(self.size)]

    def set_bestFitnessValue(self, value):
        self.best_fitness_value = value

    def get_bestFitnessValue(self):
        return self.best_fitness_value

    def set_bestPosition(self, i, value):
        self.best_position[i] = value

    def get_bestPosition(self):
        return self.best_position

    # 更新速度
    def update_vel(self, part):
        for i in range(self.dim):
            #print(self.W)
            vel_value = self.W * part.get_vel()[i] + self.C1 * random.random() * (part.get_best_pos()[i] - part.get_pos()[i]) \
                        + self.C2 * random.random() * (self.get_bestPosition()[i] - part.get_pos()[i])
            if vel_value > self.max_vel[i]:
                vel_value = self.max_vel[i]
            elif vel_value < -self.max_vel[i]:
                vel_value = -self.max_vel[i]
            part.set_vel(i, vel_value)

    # 更新位置
    def update_pos(self, part):
        for i in range(self.dim):
            pos_value = part.get_pos()[i] + part.get_vel()[i]
            if pos_value < 0:
                pos_value = 0
            if pos_value > x_max[i]:
                pos_value = x_max[i]

            part.set_pos(i, pos_value)
        #print(part.get_pos())
        if part.get_pos()[2]>=15*part.get_pos()[3] and part.get_pos()[2]<=130*part.get_pos()[3] :
            if cons(part.get_pos()):
                value = fit_fun(part.get_pos())
            else:
                value = 10**10
        else:
            value = 10**10
        if value < part.get_fitness_value():
            part.set_fitness_value(value)
            for i in range(self.dim):
                part.set_best_pos(i, part.get_pos()[i])
        if value < self.get_bestFitnessValue():
            self.set_bestFitnessValue(value)
            for i in range(self.dim):
                self.set_bestPosition(i, part.get_pos()[i])


    def update(self,Wi=1,We=0.4):
        for i in range(self.iter_num):
            for part in self.Particle_list:
                self.update_vel(part)  # 更新速度
                self.update_pos(part)  # 更新位置
                self.W=(Wi-We)*((iter_num-i)/iter_num)**2+We
                # print(self.W)
            self.fitness_val_list.append(self.get_bestFitnessValue())  # 每次迭代完把当前的最优适应度存到列表
        
        return self.fitness_val_list, self.get_bestPosition()
    

dim = 4
size = 200
iter_num = 1000
x_max = [5,4,1000,30]
max_vel = [1,1,10,0.5]
best_history_pos=[]
fit_var_history_list=[]
best_final_fit_var=10**10
for k in range(10):
    pso = PSO(dim, size, iter_num, x_max, max_vel)
    fit_var_list, best_pos = pso.update()
    #print(best_pos)
    for ii in range(len(best_pos)):
        best_pos[ii]=int(round(best_pos[ii]))
    print("第"+str(k+1)+"次运行最优位置:" + str(best_pos[0])+","+str(best_pos[1])+","+str(best_pos[2])+","+str(best_pos[3]))
    print("第"+str(k+1)+"次运行最优解:" + str(fit_var_list[-1]))
    if fit_var_list[-1]<best_final_fit_var:
        best_final_fit_var=fit_var_list[-1]
        best_final_pos=str(k+1)+"次运行最优位置:" + str(best_pos[0])+","+str(best_pos[1])+","+str(best_pos[2])+","+str(best_pos[3])
        fit_var_list_200=[]
        for i in range(200):
            fit_var_list_200.append(fit_var_list[i])
        plt.clf()
        plt.scatter(np.linspace(0, 200, 200), fit_var_list_200, c="black", s=10)
print(str(k+1)+"次运行后最优位置为第"+best_final_pos)
print("最终最优解为"+str(best_final_fit_var))
plt.show()

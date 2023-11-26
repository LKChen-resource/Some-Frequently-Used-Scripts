function f=hntbg(x) %������������ϵ 
global As Ac fc ecu fys;
etu=-0.0003; %������������Ӧ��
et0=-0.00015; %��������ֵ��Ӧ��
ec0=0.002; %��������ֵѹӦ��
ft=-0.26*fc^(2/3); %��������������ǿ��
x=x*1e6;
alpha=As/Ac;
xi=alpha*fys/fc;
k=0.1*(xi^0.745);
A=2-k;
B=1-k;
epslcc=1300+14.93*fc;
epsl0=epslcc+0.95*(1400+800*(fc-20)/20)*(xi^0.2);
eta=1.6+1.5*epsl0/x; 
sigma0=fc*(1.194+0.25*((13/fc)^0.45)*(-0.07845*xi*xi+0.5789*xi));
if xi<=3.0
	beta=0.75/((1+xi)^0.5)*(fc^0.1);
else
	beta=0.75/((1+xi)^0.5*(xi-2)^2)*(fc^0.1);
end

if   x<etu
	f=0;
elseif x<=et0
	f=ft;
elseif x<=0
	f=2*x*ft/(x+et0); %�첮���Ƽ�ģ��
elseif x<=epsl0
	f=sigma0*(A*x/epsl0-B*(x/epsl0)^2);
else
	f=sigma0*(x/epsl0)/(beta*(x/epsl0-1)^eta+x/epsl0);
end

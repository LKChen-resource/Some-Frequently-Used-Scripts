%%%%本程序功能为计算钢管混凝土柱压弯承载力%%%%
%%%计算假设及参考本构主要来自《钢管混凝土》韩林海等%%%
%%%试验数据为《Experimental studies on the ultimate moment of concrete filled square steel》
%%%和《Elasto-plastic behavior of concrete filled square steel tubular beam-columns》
%%%中的Ⅲ-2。
%%%参数输入%%%
%%%无特殊说明，以下长度单位为mm，强度单位为Mpa。
clear;
clc;
%%%%几何尺寸参数
B=100;  %截面宽度
H=B;    %截面高度
t=2.98; %钢板厚度
b=B-2*t;     %核心混凝土截面宽度
h=H-2*t;    %核心混凝土截面高度
as1=H-1.5*t;   %受拉侧钢板形心至核心混凝土受压边缘距离
as2=0.5*t;      %受压侧钢板形心至核心混凝土受压边缘距离
Ast=B*t;    %受拉钢管底板截面面积
Asc=B*t;    %受压钢管底板截面面积
Ac=b*h;     %核心混凝土截面面积
As=Asc+Ast+(H-2*t)*t*2;%钢管截面面积
%%%%材料参数
global fc fys Es ecu Ac As;
fc=26.5;        %混凝土轴心抗压强度
fys=289;        %钢材屈服强度
Es=215000;      %钢材弹性模量
eys=fys/Es;     %钢材屈服应变
ecu=0.015;       %受压极限应变
n=60;           %截面划分条带个数
N0=520000;      %柱轴向承载力
Nk=0.2*N0;       %总轴压力

%%%%判断轴力合理性
Nky=hntbg(eys)*Ac+ggbg(eys)*As;%钢材屈服取为柱子屈服，此即为屈服轴力
if Nk>=Nky
    disp('总轴力过大');
    return
end

%%%%初始轴向压应变，二分法
ecdie1=0;
ecdie2=Nk/Nky*eys;
ec0=0;
Nkg1=0;
%%%%%求解轴力下的受压侧初始应变
while abs(Nkg1-Nk)>(0.001*Nk+1)
    ec0=(ecdie1+ecdie2)/2;
    Nkg1=hntbg(ec0)*Ac+ggbg(ec0)*As;
    if Nkg1>Nk
        ecdie2=ec0;
    else
        ecdie1=ec0;
    end
end

%%%%曲率控制加载的控制参数
phi(1)=0;
phiy=2.5*eys/H;
dphi=phiy/25;
m(1)=0;
x0(1)=0;
ec=ec0;     %暂时等于初始压应变，如果不变程序就有问题
times=2;
%%%%曲率控制加载，每次大循环增加一个曲率步长，应变达到极限压应变作为退出条件
while ec-ecu<=-0.01*ecu
    ec1=ec0;
    ec2=ecu;
    phi(times)=phi(times-1)+dphi;
    Ns=0;
    %%%利用轴力求解应变，小循环，求解每步曲率下对应的弯矩
    while (abs(Ns-Nk)>Nk*0.001+1)||(ec1==0&&ec2==ecu)
        ec=(ec1+ec2)/2;
        esc=ec+phi(times)*as2;
        est=ec-phi(times)*as1;
        %受压钢板
        Nsc=ggbg(esc)*Asc;%受压钢板轴力
        Myc=Nsc*(H/2-as2);%受压钢板弯矩
        %受拉钢板
        Nst=ggbg(est)*Ast;
        Myt=Nst*(H/2-as1);%此处为正弯矩，因此两个负数相乘
        %混凝土产生的轴力弯矩
       Nc1=0;
       Mc1=0;
       for i=1:1:n
           dx=h/n;
           xi=i*dx-dx/2;%条带形心至边缘距离
           eci=ec-phi(times)*xi;%第i条带的应变
           stressci=hntbg(eci);%第i条带的应力
           Nc1=Nc1+stressci*b*dx;
           Mc1=Mc1+stressci*b*dx*(h/2-xi);
       end
       %钢管中间段产生的轴力和弯矩
       Ns1=0;
       Ms1=0;
       for i=1:n
           dx=h/n;
           xi=i*dx-dx/2;
           esi=ec-phi(times)*xi;
           stresssi=ggbg(esi);
           Ns1=Ns1+stresssi*dx*t;
           Ms1=Ms1+stresssi*t*dx*(h/2-xi)*2;
       end
       Ns=Nsc+Nst+Nc1+Ns1;
       if (Ns>Nk)
           ec2=ec;
       else
           ec1=ec;
       end
    end
    m(times)=Myc+Myt+Mc1+Ms1;%记录每一步曲率下的弯矩
    m(times)=m(times)/1e5;
    x0(times)=ec/phi(times);%计算受压区高度
    Ns0(times)=Ns;
    times=times+1;
    
end
%%%%%绘出此轴力下的弯矩曲率关系曲线%%%%%
phi=phi*1e3;
plot(phi/10,m);
title('矩形钢管混凝土截面在轴力作用下的弯矩曲率关系');
xlabel('曲率φ/m-1');
ylabel('弯矩（KN*m）');
y=[phi;m]';%%phi，M参数便于取值
%%%%%%结束%%%%%%
    
           
        








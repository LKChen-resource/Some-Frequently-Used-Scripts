%%%%��������Ϊ����ֹܻ�������ѹ�������%%%%
%%%������輰�ο�������Ҫ���ԡ��ֹܻ����������ֺ���%%%
%%%��������Ϊ��Experimental studies on the ultimate moment of concrete filled square steel��
%%%�͡�Elasto-plastic behavior of concrete filled square steel tubular beam-columns��
%%%�еĢ�-2��
%%%��������%%%
%%%������˵�������³��ȵ�λΪmm��ǿ�ȵ�λΪMpa��
clear;
clc;
%%%%���γߴ����
B=100;  %������
H=B;    %����߶�
t=2.98; %�ְ���
b=B-2*t;     %���Ļ�����������
h=H-2*t;    %���Ļ���������߶�
as1=H-1.5*t;   %������ְ����������Ļ�������ѹ��Ե����
as2=0.5*t;      %��ѹ��ְ����������Ļ�������ѹ��Ե����
Ast=B*t;    %�����ֹܵװ�������
Asc=B*t;    %��ѹ�ֹܵװ�������
Ac=b*h;     %���Ļ������������
As=Asc+Ast+(H-2*t)*t*2;%�ֹܽ������
%%%%���ϲ���
global fc fys Es ecu Ac As;
fc=26.5;        %���������Ŀ�ѹǿ��
fys=289;        %�ֲ�����ǿ��
Es=215000;      %�ֲĵ���ģ��
eys=fys/Es;     %�ֲ�����Ӧ��
ecu=0.015;       %��ѹ����Ӧ��
n=60;           %���滮����������
N0=520000;      %�����������
Nk=0.2*N0;       %����ѹ��

%%%%�ж�����������
Nky=hntbg(eys)*Ac+ggbg(eys)*As;%�ֲ�����ȡΪ�����������˼�Ϊ��������
if Nk>=Nky
    disp('����������');
    return
end

%%%%��ʼ����ѹӦ�䣬���ַ�
ecdie1=0;
ecdie2=Nk/Nky*eys;
ec0=0;
Nkg1=0;
%%%%%��������µ���ѹ���ʼӦ��
while abs(Nkg1-Nk)>(0.001*Nk+1)
    ec0=(ecdie1+ecdie2)/2;
    Nkg1=hntbg(ec0)*Ac+ggbg(ec0)*As;
    if Nkg1>Nk
        ecdie2=ec0;
    else
        ecdie1=ec0;
    end
end

%%%%���ʿ��Ƽ��صĿ��Ʋ���
phi(1)=0;
phiy=2.5*eys/H;
dphi=phiy/25;
m(1)=0;
x0(1)=0;
ec=ec0;     %��ʱ���ڳ�ʼѹӦ�䣬�����������������
times=2;
%%%%���ʿ��Ƽ��أ�ÿ�δ�ѭ������һ�����ʲ�����Ӧ��ﵽ����ѹӦ����Ϊ�˳�����
while ec-ecu<=-0.01*ecu
    ec1=ec0;
    ec2=ecu;
    phi(times)=phi(times-1)+dphi;
    Ns=0;
    %%%�����������Ӧ�䣬Сѭ�������ÿ�������¶�Ӧ�����
    while (abs(Ns-Nk)>Nk*0.001+1)||(ec1==0&&ec2==ecu)
        ec=(ec1+ec2)/2;
        esc=ec+phi(times)*as2;
        est=ec-phi(times)*as1;
        %��ѹ�ְ�
        Nsc=ggbg(esc)*Asc;%��ѹ�ְ�����
        Myc=Nsc*(H/2-as2);%��ѹ�ְ����
        %�����ְ�
        Nst=ggbg(est)*Ast;
        Myt=Nst*(H/2-as1);%�˴�Ϊ����أ���������������
        %�������������������
       Nc1=0;
       Mc1=0;
       for i=1:1:n
           dx=h/n;
           xi=i*dx-dx/2;%������������Ե����
           eci=ec-phi(times)*xi;%��i������Ӧ��
           stressci=hntbg(eci);%��i������Ӧ��
           Nc1=Nc1+stressci*b*dx;
           Mc1=Mc1+stressci*b*dx*(h/2-xi);
       end
       %�ֹ��м�β��������������
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
    m(times)=Myc+Myt+Mc1+Ms1;%��¼ÿһ�������µ����
    m(times)=m(times)/1e5;
    x0(times)=ec/phi(times);%������ѹ���߶�
    Ns0(times)=Ns;
    times=times+1;
    
end
%%%%%����������µ�������ʹ�ϵ����%%%%%
phi=phi*1e3;
plot(phi/10,m);
title('���θֹܻ��������������������µ�������ʹ�ϵ');
xlabel('���ʦ�/m-1');
ylabel('��أ�KN*m��');
y=[phi;m]';%%phi��M��������ȡֵ
%%%%%%����%%%%%%
    
           
        








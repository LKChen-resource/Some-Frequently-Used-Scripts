function f=ggbg(x) %�ֲı�����ϵ 
global fys Es;
fyc=fys; %�ֲ���ѹ����ǿ��
fyt=-fys; %�ֲ���������ǿ��
eyc0=fyc/Es; %�ֲ���ѹ����Ӧ��
eyt0=fyt/Es; %�ֲ���������Ӧ��
if x<eyt0
    f=fyt;
elseif x<eyc0
    f=Es*x;
else
    f=fyc; %���뵯����ģ��
end

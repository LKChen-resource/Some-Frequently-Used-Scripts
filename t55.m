clear;
clc;
%This script converts the axial strain volume strain relationship in the paper into an axial stress lateral strain relationship,
%and interpolates as well smooths the data
%导入excel数据
filename=xlsread('0.55.xlsx','Sheet1');%文件名，表名称
fl=[0,2.1,4.3,8.6,17.2,30.1,43];%围压
num1=length(fl);%循环次数
for j=0:num1-1
%j=6
 ec=0;
 fc=0;
 ec2=0;
 vl=0;
%分别轴向应变-轴向应力，轴向应变-体积应变
ec=filename(:,1+j*6);
ec(isnan(ec(:,1))==1)=[];%删除nan
fc=filename(:,2+j*6);
fc(isnan(fc(:,1))==1)=[];%删除nan

ec2=filename(:,3+j*6);
ec2(isnan(ec2(:,1))==1)=[];
vl=filename(:,4+j*6);
vl(isnan(vl(:,1))==1)=[];
%数据处理时，记得加轴向应变的负号
el=(vl+ec2)/2;

%均匀插值
%num=floor(max(ec)/0.0002)
ec_AI=0:0.0002:max(ec);
fc_AI=interp1(ec,fc,ec_AI,'linear');
%plot(ec,fc,'o',ec_AI,fc_AI,'o')
ec2_AI=0:0.0002:max(ec2);
%plot(ec2,el,'o')
el_AI=interp1(ec2,el,ec2_AI,'linear');
%plot(ec2,el,'o');
%plot(ec2_AI,el_AI,'o');

%关联侧向应变与轴向应力
num=min(length(ec_AI),length(ec2_AI));
for i=1: num
    result(i,1+j*3)=fc_AI(i);
    result(i,2+j*3)=el_AI(i);
    result(i,3+j*3)=-ec2_AI(i);

end
end
col=['k.','b.', 'g.', 'r.', 'c.', 'm.', 'y.', 'k.','b.'];


for i=0:8
%plot(result(:,1+i*3),result(:,2+i*3),'o');
plot(result(:,2+i*3),result(:,1+i*3),[col(2*i+1),col(2*i+2)]);
hold on;
%plot(result(:,1+i*3),result(:,3+i*3),'o');
plot(result(:,3+i*3),result(:,1+i*3),[col(2*i+1),col(2*i+2)]);
hold on
end
hold off;


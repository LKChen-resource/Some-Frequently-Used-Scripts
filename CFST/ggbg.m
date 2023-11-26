function f=ggbg(x) %钢材本构关系 
global fys Es;
fyc=fys; %钢材受压屈服强度
fyt=-fys; %钢材受拉屈服强度
eyc0=fyc/Es; %钢材受压屈服应变
eyt0=fyt/Es; %钢材受拉屈服应变
if x<eyt0
    f=fyt;
elseif x<eyc0
    f=Es*x;
else
    f=fyc; %理想弹塑性模型
end

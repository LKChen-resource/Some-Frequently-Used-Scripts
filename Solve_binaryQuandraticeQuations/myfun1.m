

function q=myfun1(p)
global i k1 k2
x=p(1);
y=p(2);
q(1)=pi*(x-2*y)^2/4-k1(i);
q(2)=pi*(x-y)*y-k2(i);
end
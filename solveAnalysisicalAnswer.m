syms N A fc theta d t alpha fs pc fc0

k=(d-2*t)*(pc*N/A-fc0)/(2*alpha*t*fs);
q1=A*fc*(1+theta*sqrt((3+((d-2*t)*(pc*N/A-fc)/(2*alpha*t*fs)-1)^2)/3))==N;
sol1=solve(q1,N)
syms N Ac fc As d t alpha fs pc fc fr blo
q2= Ac*fc*(1+((pc*N/Ac-fc)/fr-1)*fr/fc+blo)==N;
sol2=solve(q2,N)
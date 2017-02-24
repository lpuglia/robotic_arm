function [] = testIntegration()
    L1 = Link([0,0,0,pi/2]);
    L2 = Link([0,0,104.5,0]);
    L3 = Link([0,0,97.5,0]);
    L4 = Link([0,20.5,27,-pi/2]);
    L5 = Link([0,160.5,0,0]);
    rob = SerialLink([L1, L2, L3, L4, L5],'name','Robottino');

    [res, err, flag] = ikconnorot(rob, transl([220.6,-151,43]), zeros(1,5));

    res = fixRange(res)

    if (res(2) < 0)
        q0 = res;
        q0(2:3) = -q0(2:3);
        q0(4) = -(q0(4)+pi/4)-pi/4;
        q0 = fixRange(q0);
        [res, err, flag] = ikconnorot(rob, transl([220.6,-151,43]), q0);
        res = fixRange(res)
    end
end

function x = fixRange(res)
    x = mod(res + pi, 2*pi) - pi;
end
function [res, err, flag, robDegrees, intDegrees, intErr] = testIntegrationCon(x, y, port, max_it)
    L1 = Link([0,0,0,pi/2]);
    L2 = Link([0,0,104.5,0]);
    L3 = Link([0,0,97.5,0]);
    L4 = Link([0,20.5,27,-pi/2]);
    L5 = Link([0,160.5,0,0]);
    rob = SerialLink([L1, L2, L3, L4, L5],'name','Robottino');

    lims = rob.qlim;
    lims(2,1) = -30;
    lims(3,1) = deg2rad(-90);
    lims(4,1) = deg2rad(-160);
    rob.qlim = lims;

    dest = [x, y, -35];
    
    it = 0;
    err = Inf;
    while it < max_it && err > 1
        q0(1) = 0;
        q0(2) = 45 + rand() * 40;
        q0(3) = -(rand() * 70);
        q0(4) = 0 -(rand() * 90);
        q0(5) = 0;
        [res, err, flag] = ikconnorot(rob, transl(dest), deg2rad(q0));

        if flag < 0
            error('È zumpat tutte cose');
        end
        it = it + 1;
        disp(it);
    end
    
    if err > 1
        error('Convergence not reached');
    end
    disp(q0);
    res = mod(res + pi, 2*pi) - pi;
    topass = rad2deg(res);
    topass(6) = 90;
    %[robDegrees, intDegrees, intErr] = moveRobotDH(topass,port);
end
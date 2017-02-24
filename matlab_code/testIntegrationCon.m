function [res, err, flag, robDegrees, intDegrees, intErr] = testIntegrationCon(x, y, port)
    L1 = Link([0,0,0,pi/2]);
    L2 = Link([0,0,104.5,0]);
    L3 = Link([0,0,97.5,0]);
    L4 = Link([0,20.5,27,-pi/2]);
    L5 = Link([0,160.5,0,0]);
    rob = SerialLink([L1, L2, L3, L4, L5],'name','Robottino');

    lims = rob.qlim;
    lims(2,1) = 0;
    rob.qlim = lims;

    dest = [x, y, -35];
    
    [res, err, flag] = ikconnorot(rob, transl(dest), zeros(1,5));

    if flag < 0
        error('È zumpat tutte cose');
    end

    res = mod(res + pi, 2*pi) - pi;

    [robDegrees, intDegrees, intErr] = moveRobotDH(rad2deg(res),port);
end
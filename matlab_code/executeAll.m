function [] = executeAll(port, waitBetweenMoves)
    L1 = Link([0,0,0,pi/2]);
    L2 = Link([0,0,104.5,0]);
    L3 = Link([0,0,97.5,0]);
    L4 = Link([0,20.5,27,-pi/2]);
    L5 = Link([0,160.5,0,0]);
    rob = SerialLink([L1, L2, L3, L4, L5],'name','Robottino');

    lims = rob.qlim;
    lims(1,1) = deg2rad(-50);
    lims(1,2) = deg2rad(50);
    lims(2,1) = deg2rad(60);
    lims(2,2) = deg2rad(120);
    lims(3,1) = deg2rad(-90);
    lims(4,1) = deg2rad(-160);
    rob.qlim = lims;
    
    [robDegrees, intDegrees, intErr] = moveRobotDH([NaN, NaN, NaN, NaN, NaN, NaN], port);
    q0 = generateRandomPosition();
    q0(6) = NaN;
    [robDegrees, intDegrees, intErr] = moveRobotDH(q0, port);
    pause(waitBetweenMoves);
    
    [x, y] = getSpiderPosition('172.16.69.175', 8089, 60);
    
    [res, err, flag, num_it, topass, robDegrees, intDegrees, intErr] = moveToPositionXY(x*0.8, y*0.8, port, 200, q0(1:5));
    
    pause(waitBetweenMoves);
    
    [res, err, flag, num_it, topass, robDegrees, intDegrees, intErr] = moveToPositionXY(x, y, port, 200, topass(1:5));
    
    pause(waitBetweenMoves);
    
    [robDegrees, intDegrees, intErr] = moveRobotDH([NaN, NaN, NaN, NaN, NaN, 130], port);
    
    pause(waitBetweenMoves);
    
    [robDegrees, intDegrees, intErr] = moveRobotDH([-60, NaN, NaN, NaN, NaN, NaN], port);
    
    pause(waitBetweenMoves);
    
    [robDegrees, intDegrees, intErr] = moveRobotDH([NaN, NaN, NaN, NaN, NaN, 90], port);
    
    pause(waitBetweenMoves);
    
    [robDegrees, intDegrees, intErr] = moveRobotDH(q0, port);
end

function [x, y] = getSpiderPosition(ip, port, timeout)
    t = udp(ip, 'LocalPort', port, 'Timeout', timeout);
    
    fopen(t);
    try
        data = fgetl(t);
        res = textscan(data, '%f,%f');
        res = [res{1:2}];
        disp(res);
        x = res(1);
        y = res(2);
    catch exc
        getReport(exc)
    end
    fclose(t);
end

function [res, err, flag, num_it, topass, robDegrees, intDegrees, intErr] = moveToPositionXY(x, y, port, max_it, q0)
    dest = [x, y, -35];
    
    it = 0;
    err = Inf;
    
    if nargin > 4
        it = it + 1;
        [res, err, flag] = ikconnorot(rob, transl(dest), deg2rad(q0));

        if flag < 0
            error('Negative flag, probable error');
        end
    end
    
    while it < max_it && err > 1
        q0 = generateRandomPosition();
        [res, err, flag] = ikconnorot(rob, transl(dest), deg2rad(q0));

        if flag < 0
            error('Negative flag, probable error');
        end
        it = it + 1;
        %disp(it);
    end
    
    if err > 1
        error('Convergence not reached');
    end
    num_it = it;
    %disp(q0);
    res = mod(res + pi, 2*pi) - pi;
    topass = rad2deg(res);
    topass(5) = 90;
    topass(6) = 85;
    
    %moveRobotDH([NaN, NaN, NaN, NaN, NaN, NaN], port);
    [robDegrees, intDegrees, intErr] = moveRobotDH(topass, port);
end

function q = generateRandomPosition()
    q(1) = 0;
    q(2) = 60 + rand() * 25;
    q(3) = -(rand() * 70);
    q(4) = 20 -(rand() * 70);
    q(5) = 90;
end

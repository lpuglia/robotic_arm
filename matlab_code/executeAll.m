function [] = executeAll(port, waitKey, waitBetweenMoves)
    if nargin < 3
       waitBetweenMoves = 0; 
    end

    L1 = Link([0,0,0,pi/2]);
    L2 = Link([0,0,104.5,0]);
    L3 = Link([0,0,97.5,0]);
    L4 = Link([0,20.5,27,-pi/2]);
    L5 = Link([0,160.5,0,0]);
    rob = SerialLink([L1, L2, L3, L4, L5],'name','Robottino');

    lims = rob.qlim;
    lims(1,1) = deg2rad(-50);
    lims(1,2) = deg2rad(50);
    lims(2,1) = deg2rad(45);
    lims(2,2) = deg2rad(120);
    lims(3,1) = deg2rad(-100);
    lims(4,1) = deg2rad(-160);
    rob.qlim = lims;
    
    condWait(waitKey, waitBetweenMoves);
    disp('Move 1');
    [robDegrees, intDegrees, intErr] = moveRobotDH([NaN, NaN, NaN, NaN, NaN, NaN], port);
    %q0 = generateRandomPosition();
    q0(1) = 0;
    q0(2) = 90;
    q0(3) = -70;
    q0(4) = -150;
    q0(5) = 90;
    q0(6) = NaN;
    disp('Move 2');
    [robDegrees, intDegrees, intErr] = moveRobotDH(q0, port);
    
    condWait(waitKey, waitBetweenMoves);
    
    [x, y] = getSpiderPosition('172.16.69.175', 8089, 60);
    
    [res, err, flag, num_it, topass, robDegrees, intDegrees, intErr] = moveToPositionXY(rob, x*0.7, y*0.7, 40, port, 200, q0(1:5))
    disp('Move 3');
    condWait(waitKey, waitBetweenMoves);
    
    [res, err, flag, num_it, topass, robDegrees, intDegrees, intErr] = moveToPositionXY(rob, x, y, 40, port, 200, topass(1:5));
    q1 = topass;
    disp('Move 4');
    condWait(waitKey, waitBetweenMoves);
    
    [robDegrees, intDegrees, intErr] = moveRobotDH([NaN, NaN, NaN, NaN, NaN, 130], port);
    disp('Move 5');
    condWait(waitKey, waitBetweenMoves);
    
    if q1(1) > 0
        finalDeg = -60;
    else
        finalDeg = 50;
    end
    [robDegrees, intDegrees, intErr] = moveRobotDH([finalDeg, NaN, NaN, NaN, NaN, NaN], port);
    disp('Move 6');
    condWait(waitKey, waitBetweenMoves);
    
    [robDegrees, intDegrees, intErr] = moveRobotDH([NaN, NaN, NaN, NaN, NaN, 75], port);
    disp('Move 7');
    condWait(waitKey, waitBetweenMoves);
    
    q1(1) = finalDeg;
    %pos = transl(rob.fkine(deg2rad(q1(1:5))));
    %disp('Move 8');
    %[res, err, flag, num_it, topass, robDegrees, intDegrees, intErr] = moveToPositionXY(rob, pos(1)*0.65, pos(2)*0.65, 15, port, 200, q1(1:5));
    %condWait(waitKey, waitBetweenMoves);
    
    %[robDegrees, intDegrees, intErr] = moveRobotDH(q0, port);
    [robDegrees, intDegrees, intErr] = moveRobotDH(q1, port);
    disp('Move 8');
    condWait(waitKey, waitBetweenMoves);
    
    [robDegrees, intDegrees, intErr] = moveRobotDH(q0, port);
    disp('Move 8');
end

function [] = condWait(waitKey, waitBetweenMoves)
    disp('Waiting...');
    if waitKey
        waitforbuttonpress;
        disp('Key pressed');
    else
        pause(waitBetweenMoves);
        disp('Wait ended.');
    end
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

function [res, err, flag, num_it, topass, robDegrees, intDegrees, intErr] = moveToPositionXY(rob, x, y, z, port, max_it, q0)
    dest = [x, y, z];
    
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
    topass(6) = 75;
    
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

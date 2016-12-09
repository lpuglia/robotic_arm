L1 = Link([0,0,0,pi/2]);
L2 = Link([0,0,104.5,0]);
L3 = Link([0,0,97.5,0]);
L4 = Link([0,20.5,27,-pi/2]);
L5 = Link([0,160.5,0,0]);
rob = SerialLink([L1, L2, L3, L4, L5],'name','Robottino');
rob.plot([0,0,0,-pi/2,0],'workspace',[-30,570,-300,300,-300,300],'noa')
rob.teach()
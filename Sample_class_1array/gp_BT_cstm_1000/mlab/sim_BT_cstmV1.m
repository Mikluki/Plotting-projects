% sim_BowTie_v1(100, 20e9, 190e9,    3e-05, 1e-3, 0.001)
function [ReZ,ImZ] = ...
    sim_BT_cstm(Nf, fmin, fmax, ...
                fD, R, H)
    %% ==== Define frequency range ====
    freqRange = linspace(fmin, fmax, Nf);

    %% ==== Define constants ====
    xc              = 0;
    yc              = 0;
    dd              = fD;

    Gold_Thick      = 1e-6;
    boardLength     = 3.5e-3;
    boardWidth      = 3.5e-3;

    %% ===== Merge polygons =====
    circ0 = antenna.Circle('Center',[xc yc],'Radius',R);
    trR = antenna.Polygon('Vertices',...
                          [xc +dd; +H +R; -H +R]);
    trL = antenna.Polygon('Vertices',...
                          [xc -dd; +H -R; -H -R]);

    feedMetal = circ0 - trR - trL;
    % figure('Position', [0 550 470 440]);
    % plot(feedMetal)
    % hold on
    % plot(boardShape)

    %%  ===== Stack Design =====
    ant                = pcbStack;
    boardShape = antenna.Rectangle('Center',[xc yc],...
                        'Width',boardWidth,...
                        'Length',boardLength);

    ant.BoardShape     = boardShape;
    ant.BoardThickness = Gold_Thick;
    ant.Layers         = {feedMetal};
    ant.FeedDiameter   = fD;

    ant.FeedLocations  = [xc yc 1];
    ant.FeedViaModel   = 'octagon';
    ant.Conductor      = metal('PEC');

    %% ===== calc Impedance =====
    Z = impedance(ant, freqRange);
    ReZ = real(Z);
    ImZ = imag(Z);

end

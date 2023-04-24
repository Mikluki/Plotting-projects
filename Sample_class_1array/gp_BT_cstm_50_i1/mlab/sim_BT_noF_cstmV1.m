clc, clearvars
tic
close all


%% define vars
Nf              = 60;
fmin            = 20e9;
fmax            = 190e9;
fmain           = 100e9;
fD              = 3.05e-5;

z0              = 50;

R               = 0.0006011675373315565;
phi             = 143;
% H               = 0.004146944039238999;

angle_          = 90 - phi/2;
H               = R * tan(angle_*pi/180);

xc              = 0;
yc              = 0;
dd              = fD;

boardLength     = 3.2e-3;
boardWidth      = 3.2e-3;
Gold_Thick      = 1e-6;

%% ===== Merge polygons =====
freqRange = linspace(fmin, fmax, Nf);

circ0 = antenna.Circle('Center',[xc yc],'Radius',R);
trR = antenna.Polygon('Vertices',...
      [xc +dd; +H +R; -H +R]);
trL = antenna.Polygon('Vertices',...
      [xc -dd; +H -R; -H -R]);

feedMetal = circ0 - trR - trL;
% fig = figure('Position', [0 550 470 440]);
% axis equal; grid on; hold on;
% plot(feedMetal)
% feedCirc = antenna.Circle('Center',[xc yc],'Radius',feedDiam/2);
% plot(feedCirc)
% exportgraphics(fig,'mlabProfile.png','Resolution',400);

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


%% ===== Show Mesh / Current =====
figure('Position', [480 550 470 440]);
current(ant, fmain)


%% ===== calc Impedance =====
disp('    [mlab]: calculating Impedance')
Z = impedance(ant, freqRange);
figure('Position', [0 550 470 440]);
mesh(ant)
ReZ = real(Z);
ImZ = imag(Z);


%% ==== S parameter ====
S11db = calcS11(Z, z0);

% ==== Re(Z) @ Im(Z)=0 ====
fcross = @(x) find(diff(sign(x)));
idxCross = fcross(ImZ);

% ===== Plotting Stack Analysis =====
saveName = 'Nf'+string(Nf)+'Poly_Z_S11.png';
titleName = 'Stack characteristics';
plot_Ant(ReZ = ReZ, ImZ = ImZ,...
         freqRange = freqRange,...
         idxCross = idxCross,...
         S11db = S11db,...
         saveName = saveName, title = titleName)
disp('    [mlab]: simulation compelete')
toc



% ===== Calc S11 function =====
function S11db = calcS11(Z, z0)
    S11db = 20*log10(abs((Z - z0) ./ (Z + z0)));
end

% ===== Plot Obj function =====
function plot_Ant(Args)
    arguments
        Args.ReZ
        Args.ImZ
        Args.freqRange
        Args.idxCross
        Args.S11db
        Args.saveName
        Args.title
    end
    lw = 2;
    fig = figure;
    fig.Position = [0 0 950 450];
    t = tiledlayout(fig,1,2,'TileSpacing','Compact','Padding','Compact',...
        'OuterPosition',[0 0 0.8 1]);
    title(t, Args.title)

    % ==== Plot 1 ====
    ax1 = nexttile;
    ax1.FontSize = 18;
    ax1.LineWidth = 2;
    plot(ax1,Args.freqRange.*1e-9, Args.ReZ,...
         'b','LineWidth',lw,'DisplayName','Re(Z)');
    hold on
    plot(ax1,Args.freqRange.*1e-9, Args.ImZ,...
         'r','LineWidth',lw,'DisplayName','Im(Z)');
    hold off
    yline(ax1,0,'LineWidth',1.5,'linestyle','-',...
        'HandleVisibility','off')
    if ~isempty(Args.idxCross)
        xline(ax1,Args.freqRange(Args.idxCross)*1e-9,...
            'LineWidth',1.0,'Color','#29353b',...
            'linestyle','--','HandleVisibility','off');
    end

    % ylim([-200 300]);
    strTitle = 'Z';
                % ', angle = ' + strAngle +...
                % ', length = ' + strLength;
    title(ax1, strTitle);
    xlabel(ax1, 'Frequency (GHz)')
    ylabel(ax1, 'Z (Ohms)')
    % ylim(ax1, [-200 200]);
    grid(ax1)
    legend(ax1)

    dim = [0.77 0.62 .3 .3];
    strPeaks = 'Re(Z)@[Im(Z)=0] = ' +...
                string(round(Args.ReZ(Args.idxCross),1));
    annotation('textbox',dim,'String',strPeaks,'FitBoxToText','on');

    % ==== Plot 2 ====
    ax2 = nexttile;
    plot(ax2,Args.freqRange.*1e-9, Args.S11db,...
         'Color','#0071ff','LineWidth',lw,...
         'DisplayName','S_1_1');
    if ~isempty(Args.idxCross)
        xline(ax1,Args.freqRange(Args.idxCross)*1e-9,...
            'LineWidth',1.0,'Color','#29353b',...
            'linestyle','--','HandleVisibility','off');
    end

    % ylim([-15,0]);
    strTitle = 'S_1_1';
                % ', angle = ' + strAngle +...
                % ', length = ' + strLength;
    title(ax2, strTitle);
    xlabel(ax2, 'Frequency (GHz)')
    ylabel(ax2, 'Magnitude (dB)')
    grid(ax2)
    legend(ax2)
    % figure(3);
    % rfplot(Args.sParam,1,1,'r');
    % ==== Save pic ====
    % saveName = Args.saveName;
    % exportgraphics(fig,saveName,'Resolution',500);
end

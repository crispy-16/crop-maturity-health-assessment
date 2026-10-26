% matlab/classify_leaf.m
% Turn the 41 features into a verdict.
%
% If matlab/leaf_model.mat exists (created by run_training.m) the
% trained classifier is used. Otherwise a transparent rule-based fallback
% runs, so the dashboard works before the model has been trained.
function R = classify_leaf(f, names, M)

v = @(nm) f(strcmp(names, nm));

fracLesion = v('frac_lesion');
affected   = 100 * fracLesion;

% ---- Severity from the percentage of leaf area affected --------------
% Standard plant-pathology disease-severity bands.
if     affected <  2, severity = 'None';        sevIdx = 0;
elseif affected <  10, severity = 'Mild';       sevIdx = 1;
elseif affected <  25, severity = 'Moderate';   sevIdx = 2;
elseif affected <  50, severity = 'Severe';     sevIdx = 3;
else                   severity = 'Very severe'; sevIdx = 4;
end

% ---- Disease class ----------------------------------------------------
modelFile = fullfile(fileparts(mfilename('fullpath')), 'leaf_model.mat');
label = '';  conf = NaN;  src = 'rules';

if isfile(modelFile)
    try
        S = load(modelFile);                   % S.mdl, S.featNames
        x = zeros(1, numel(S.featNames));
        for k = 1:numel(S.featNames)
            idx = strcmp(names, S.featNames{k});
            if any(idx), x(k) = f(idx); end
        end
        [lab, score] = predict(S.mdl, x);
        label = char(string(lab));
        src   = 'model';
        s = double(score);
        s = exp(s - max(s));  s = s / sum(s);  % soft-max over SVM scores
        conf = max(s) * 100;
    catch
        label = '';
    end
end

if isempty(label)
    label = rule_label(v, affected);
end

% ---- Dominant visible symptom ----------------------------------------
fr  = [v('frac_chlorotic'), v('frac_necrotic'), v('frac_powdery'), v('frac_sooty')];
nms = {'Chlorosis (yellowing)', 'Necrosis (dead tissue)', ...
       'Powdery coating', 'Sooty deposit'};
[fmax, imax] = max(fr);
if fmax < 0.02
    symptom = 'No visible symptom';
else
    symptom = nms{imax};
end

R = struct('condition', label, 'severity', severity, 'severity_index', sevIdx, ...
           'affected_area', affected, 'symptom', symptom, ...
           'confidence', conf, 'source', src, ...
           'frac_chlorotic', fr(1), 'frac_necrotic', fr(2), ...
           'frac_powdery',   fr(3), 'frac_sooty',    fr(4), ...
           'frac_healthy',   v('frac_healthy'));
end


% ---------------------------------------------------------------------
function label = rule_label(v, affected)
% Transparent fallback. Uses the features that the trained model also
% ranks highest: a* statistics, lesion fractions and leaf shape.
if affected < 3 && v('mean_a') < -10
    label = 'Healthy';
elseif v('convex_deficiency') > 0.18 || v('solidity') < 0.80
    label = 'Cutting Weevil (chewed margins)';
elseif v('frac_necrotic') > 0.45 && v('mean_a') > -5
    label = 'Die Back';
elseif v('frac_sooty') > 0.08 && v('speck_count') > 0.3
    label = 'Sooty Mould';
elseif v('frac_powdery') > 0.12
    label = 'Powdery Mildew';
elseif v('lesion_count') > 0.25 && v('lesion_mean_area') < 0.01
    label = 'Bacterial Canker';
elseif v('frac_chlorotic') > 0.35
    label = 'Anthracnose';
else
    label = 'Diseased (unspecified)';
end
end

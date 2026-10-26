%% run_training.m  --  press Run. Builds the feature table AND trains the model.
%
% Step 1: runs the pipeline over the dataset -> leaf_features.csv
% Step 2: trains a linear SVM on it          -> leaf_model.mat
%
% Both files are written next to this script. classify_leaf.m picks up
% leaf_model.mat automatically, so after this run_leaf.m will say
% "Decided by: model" instead of "rules".
%
% Takes roughly 20-30 min at PER_CLASS = 150. Start with 20 to check it runs.

DATASET   = 'E:\DIP\DIP - mini project\MangoLeafBD Dataset\MangoLeafBD Dataset';
PER_CLASS = 150;      % images per class. 20 for a quick test, 500 for everything.

%% ------------------------------------------------------------------------
clc;
here = fileparts(mfilename('fullpath'));
if isempty(here), here = pwd; end
addpath(here);

CLASSES = {'Healthy', 'Anthracnose', 'Bacterial Canker', 'Cutting Weevil', ...
           'Die Back', 'Gall Midge', 'Powdery Mildew', 'Sooty Mould'};

% ---- Resolve the dataset folder (handles the nested-folder case) --------
assert(isfolder(DATASET), 'DATASET folder does not exist:\n  %s', DATASET);
for depth = 1:3
    if any(cellfun(@(c) isfolder(fullfile(DATASET, c)), CLASSES)), break; end
    subs = dir(DATASET);
    subs = subs([subs.isdir] & ~startsWith({subs.name}, '.'));
    moved = false;
    for s = 1:numel(subs)
        cand = fullfile(DATASET, subs(s).name);
        if any(cellfun(@(c) isfolder(fullfile(cand, c)), CLASSES))
            DATASET = cand;  moved = true;  break
        end
    end
    if ~moved
        if numel(subs) == 1, DATASET = fullfile(DATASET, subs(1).name); else, break; end
    end
end

avail = CLASSES(cellfun(@(c) isfolder(fullfile(DATASET, c)), CLASSES));
assert(~isempty(avail), 'No class folders found inside:\n  %s', DATASET);
fprintf('Dataset: %s\n', DATASET);
fprintf('Classes: %s\n\n', strjoin(avail, ', '));

%% ===================== STEP 1: extract features =========================
csvPath = fullfile(here, 'leaf_features.csv');

rows = {}; labels = {}; names = {}; failed = 0; total = 0;
t0 = tic;

for k = 1:numel(avail)
    classDir = fullfile(DATASET, avail{k});
    files = [dir(fullfile(classDir, '*.jpg')); ...
             dir(fullfile(classDir, '*.jpeg')); ...
             dir(fullfile(classDir, '*.png'))];
    if isempty(files)
        fprintf('  %-18s no images, skipped\n', avail{k});
        continue
    end

    % Spread the sample over the WHOLE folder, do not take the first N.
    % Images sit in capture order, so the first N are one photo session.
    % Training on one session and testing on another measured 61% accuracy
    % instead of 96%. linspace avoids that.
    n = min(PER_CLASS, numel(files));
    idx = unique(round(linspace(1, numel(files), n)));

    okCount = 0;
    for i = idx
        total = total + 1;
        try
            img = imread(fullfile(files(i).folder, files(i).name));
            [den, ~, ~] = leaf_preprocess(img);
            % refine=false: skip the active contour, too slow for a batch
            [mask, ok] = segment_leaf(den, false, 'auto');
            if ~ok, failed = failed + 1; continue; end
            M = leaf_lesions(den, mask);
            [f, names] = leaf_features(den, mask, M);
            rows{end+1}   = f;           %#ok<SAGROW>
            labels{end+1} = avail{k};    %#ok<SAGROW>
            okCount = okCount + 1;
        catch
            failed = failed + 1;
        end
    end
    fprintf('  %-18s %3d ok  (%.0f s elapsed)\n', avail{k}, okCount, toc(t0));
end

assert(~isempty(rows), 'No images processed successfully.');

T = array2table(vertcat(rows{:}), 'VariableNames', names);
T.label = categorical(string(labels(:)));
writetable(T, csvPath);
fprintf('\nStep 1 done: %d rows, %d failed segmentation.\n', height(T), failed);
fprintf('Saved %s\n\n', csvPath);

%% ===================== STEP 2: train the classifier =====================
X = T{:, 1:end-1};
y = T.label;
featNames = T.Properties.VariableNames(1:end-1);

fprintf('Training on %d samples, %d features, %d classes...\n', ...
        size(X,1), size(X,2), numel(categories(y)));

t = templateSVM('KernelFunction', 'linear', 'Standardize', true);
mdl = fitcecoc(X, y, 'Learners', t, 'Coding', 'onevsone');

cvm = crossval(mdl, 'KFold', 5);
acc = 1 - kfoldLoss(cvm);
fprintf('5-fold cross-validated accuracy: %.1f%%\n', acc * 100);

pred = kfoldPredict(cvm);
figure('Name', 'Leaf classifier - confusion matrix');
confusionchart(y, pred);
title(sprintf('Leaf disease classifier (%.1f%% CV accuracy)', acc * 100));

save(fullfile(here, 'leaf_model.mat'), 'mdl', 'featNames', 'acc');
fprintf('\nSaved %s\n', fullfile(here, 'leaf_model.mat'));
fprintf('Run run_leaf.m again - it will now say "Decided by: model".\n');

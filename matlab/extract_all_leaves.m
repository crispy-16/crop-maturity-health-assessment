% matlab/extract_all_leaves.m
% Build the training table: run the pipeline over the MangoLeafBD dataset
% and write outputs/leaf_features.csv (one row per image, 41 features + label).
%
%   extract_all_leaves          % 150 images per class (about 20-30 min)
%   extract_all_leaves(500)     % the whole dataset (slow)
%
% Expects:  <root>/dataset/MangoLeafBD/<ClassName>/*.jpg
function extract_all_leaves(perClass)
if nargin < 1, perClass = 150; end

root = find_root();
addpath(fullfile(root, 'matlab'));
dataDir = fullfile(root, 'dataset', 'MangoLeafBD');
assert(isfolder(dataDir), 'Dataset not found at %s', dataDir);

outDir = fullfile(root, 'outputs');
if ~isfolder(outDir), mkdir(outDir); end
csvPath = fullfile(outDir, 'leaf_features.csv');

ds = imageDatastore(dataDir, 'IncludeSubfolders', true, 'LabelSource', 'foldernames');
classes = categories(ds.Labels);

files = {}; labels = {};
for k = 1:numel(classes)
    idx = find(ds.Labels == classes{k});
    % IMPORTANT: spread the sample evenly over the whole folder.
    % Images are stored in capture order, so taking the first N would
    % train on one photo session only. Measured effect of getting this
    % wrong: 61% accuracy on unseen images instead of 96%.
    if numel(idx) > perClass
        idx = idx(round(linspace(1, numel(idx), perClass)));
    end
    files  = [files;  ds.Files(idx)];              %#ok<AGROW>
    labels = [labels; repmat(classes(k), numel(idx), 1)];  %#ok<AGROW>
end
fprintf('Processing %d images across %d classes...\n', numel(files), numel(classes));

rows = {}; keptLabels = {}; failed = 0; names = {};
t0 = tic;
for i = 1:numel(files)
    try
        img = imread(files{i});
        [den, ~, ~] = leaf_preprocess(img);
        % refine=false: skip the active contour, it is too slow for a batch
        [mask, ok] = segment_leaf(den, false, 'auto');
        if ~ok, failed = failed + 1; continue; end
        M = leaf_lesions(den, mask);
        [f, names] = leaf_features(den, mask, M);
        rows{end+1} = f;                 %#ok<AGROW>
        keptLabels{end+1} = labels{i};   %#ok<AGROW>
    catch
        failed = failed + 1;
    end
    if mod(i, 50) == 0
        fprintf('  %d / %d  (%.0f s elapsed)\n', i, numel(files), toc(t0));
    end
end

T = array2table(vertcat(rows{:}), 'VariableNames', names);
T.label = categorical(string(keptLabels(:)));
writetable(T, csvPath);
fprintf('Done: %d rows written to %s (%d failed segmentation)\n', ...
        height(T), csvPath, failed);
end


function root = find_root()
here = fileparts(mfilename('fullpath'));
root = here;
while ~isfolder(fullfile(root, 'matlab'))
    p = fileparts(root);
    if strcmp(p, root), error('Could not find a "matlab" folder above %s', here); end
    root = p;
end
end

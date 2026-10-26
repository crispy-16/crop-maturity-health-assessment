% matlab/train_leaf_model.m
% Train the disease classifier on outputs/leaf_features.csv and save it to
% matlab/leaf_model.mat, which classify_leaf.m picks up automatically.
%
% Run extract_all_leaves first.
%
%   train_leaf_model            % linear SVM (one-vs-one), 5-fold CV
function train_leaf_model()

root = find_root();
csvPath = fullfile(root, 'outputs', 'leaf_features.csv');
assert(isfile(csvPath), 'Run extract_all_leaves first (%s not found).', csvPath);

T = readtable(csvPath);
featNames = T.Properties.VariableNames(1:end-1);
X = T{:, 1:end-1};
y = categorical(string(T.label));

fprintf('Training on %d samples, %d features, %d classes.\n', ...
        size(X,1), size(X,2), numel(categories(y)));

t = templateSVM('KernelFunction', 'linear', 'Standardize', true);
mdl = fitcecoc(X, y, 'Learners', t, 'Coding', 'onevsone');

% ---- Honest estimate of accuracy -------------------------------------
cvm = crossval(mdl, 'KFold', 5);
acc = 1 - kfoldLoss(cvm);
fprintf('5-fold cross-validated accuracy: %.1f%%\n', acc * 100);

pred = kfoldPredict(cvm);
figure('Name', 'Leaf classifier - confusion matrix');
confusionchart(y, pred);
title(sprintf('Leaf disease classifier (%.1f%% CV accuracy)', acc*100));

save(fullfile(root, 'matlab', 'leaf_model.mat'), 'mdl', 'featNames', 'acc');
fprintf('Saved %s\n', fullfile(root, 'matlab', 'leaf_model.mat'));
fprintf('classify_leaf.m will now use the trained model instead of the rules.\n');
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

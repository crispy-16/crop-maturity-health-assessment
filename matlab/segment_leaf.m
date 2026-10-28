% matlab/segment_leaf.m
% Separate the leaf from the background.
%
%   [mask, ok, info] = segment_leaf(den)
%   [mask, ok, info] = segment_leaf(den, refine)
%   [mask, ok, info] = segment_leaf(den, refine, method)
%
% method:
%   'kmeans'  (default) k-means clustering of the leaf's own L*a*b* pixel
%             values. Clusters that occupy much of the image border are
%             background; the leaf is the union of the rest.
%   'border'  background colour estimated from a thin border strip, then
%             an Otsu threshold on colour distance.
%   'auto'    k-means, falling back to 'border' if the result looks wrong.
%
% refine = true runs a Chan-Vese active contour afterwards.
%   NOTE: measured on MangoLeafBD, the active contour tends to grow into
%   the soft shadow around a leaf, so it is OFF by default for 'kmeans'.
%
% Measured on 64 images across all 8 classes (IoU against the 'border'
% method, which was checked visually):
%   k-means union, k=5          mean IoU 0.86
%   better on Sooty Mould, worse on textured backgrounds where the
%   background itself splits into several clusters.
function [mask, ok, info, stages] = segment_leaf(den, refine, method)

if nargin < 2 || isempty(refine), refine = false;    end
if nargin < 3 || isempty(method), method = 'kmeans'; end

% `stages` holds the intermediate images, so the dashboard and the demo
% can show each step feeding the next instead of just the final mask.
stages = struct('clusters', [], 'union', [], 'opened', [], 'cleaned', []);

switch lower(method)
    case 'border'
        [mask, stages] = seg_border(den);
        used = 'border';
    case 'kmeans'
        [mask, stages] = seg_kmeans(den);
        used = 'kmeans';
    case 'auto'
        [mask, stages] = seg_kmeans(den);
        used = 'kmeans';
        if ~plausible(mask)
            [mask, stages] = seg_border(den);
            used = 'border (kmeans failed)';
        end
    otherwise
        error('Unknown method "%s". Use kmeans, border or auto.', method);
end

% ---- optional active contour refinement ------------------------------
if refine && nnz(mask) > 50
    try
        lab = rgb2lab(den);
        refined = activecontour(lab, mask, 60, 'Chan-Vese');
        refined = imfill(imclose(refined, strel('disk', 3)), 'holes');
        refined = bwareafilt(refined, 1);
        % only accept it if it is sane AND close to what we started with
        inter = nnz(refined & mask) / max(nnz(refined | mask), 1);
        if plausible(refined) && inter > 0.6
            mask = refined;
        end
    catch
        % keep the un-refined mask
    end
end

% ---- sanity checks ----------------------------------------------------
frac   = nnz(mask) / numel(mask);
border = border_contact(mask);
ok = plausible(mask);

info = struct('area_fraction', frac, 'border_contact', border, ...
              'method', used, 'refined', refine);
end


%% =====================================================================
function [mask, stages] = seg_kmeans(den)
% k-means on the leaf's own colour values.
%
%  1. cluster every pixel in L*a*b* (lightness down-weighted so that
%     shading does not dominate hue)
%  2. a cluster that occupies much of the image border is background
%  3. the leaf is the union of all the other clusters
%  4. morphological clean-up

K       = 5;          % number of clusters
BTHR    = 0.15;       % a cluster owning more than this of the border = background
MAXFIT  = 20000;      % pixels used to FIT the clusters (the rest are assigned)
SHADOW_AB = 8;        % a*b* distance below which a cluster counts as background shadow

lab = rgb2lab(den);
[h, w, ~] = size(lab);

X = [reshape(lab(:,:,1), [], 1) * 0.5, ...   % L*, down-weighted
     reshape(lab(:,:,2), [], 1), ...         % a*
     reshape(lab(:,:,3), [], 1)];            % b*

% ---- fit on a random subset, then assign every pixel ------------------
% Fitting on all ~150k pixels is slow and gains nothing.
n = size(X, 1);
if n > MAXFIT
    rng(0);                                  % repeatable
    sel = randperm(n, MAXFIT);
else
    sel = 1:n;
end
if exist('kmeans', 'file') == 2
    [~, C] = kmeans(X(sel,:), K, 'Replicates', 3, 'MaxIter', 200);
else
    % No Statistics and Machine Learning Toolbox: imsegkmeans (Image
    % Processing Toolbox) on the same subset, laid out as an n x 1 x 3 image
    [~, C] = imsegkmeans(single(reshape(X(sel,:), [], 1, 3)), K, 'NumAttempts', 3);
    C = double(C);
end

d = zeros(n, K);
for j = 1:K
    d(:,j) = sum((X - C(j,:)).^2, 2);
end
[~, idx] = min(d, [], 2);
cmap = reshape(idx, h, w);

% ---- which clusters are background? -----------------------------------
isBg = false(1, K);
for c = 1:K
    isBg(c) = border_contact(cmap == c) > BTHR;
end

% A cast shadow has the background's colour, only darker: it changes L*
% but hardly moves a* and b*. So a cluster whose mean chromaticity is close
% to the background's is shadow, not leaf. Dark lesions inside the leaf
% that this removes come back with the hole filling below.
if any(isBg)
    bg = ismember(cmap, find(isBg));
    A = lab(:,:,2);  B = lab(:,:,3);
    bgAB = [mean(A(bg)), mean(B(bg))];
    for c = find(~isBg)
        m = (cmap == c);
        if hypot(mean(A(m)) - bgAB(1), mean(B(m)) - bgAB(2)) < SHADOW_AB
            isBg(c) = true;
        end
    end
end
leaf = ismember(cmap, find(~isBg));

if ~any(leaf(:))
    % every cluster reaches the border - keep the one that reaches least
    bc = zeros(1, K);
    for c = 1:K
        bc(c) = border_contact(cmap == c);
    end
    [~, c] = min(bc);
    leaf = (cmap == c);
end

% keep each morphological step so the dashboard can show the chain
opened  = bwareafilt(imopen(leaf, strel('disk', 3)), 1);
cleaned = bwareafilt(imfill(imclose(opened, strel('disk', 5)), 'holes'), 1);
mask    = cleaned;

stages = struct('clusters', cmap, 'union', leaf, ...
                'opened', opened, 'cleaned', cleaned);
end


%% =====================================================================
function [mask, stages] = seg_border(den)
% Background colour from a thin border strip, then Otsu on colour distance.
lab = rgb2lab(den);
[h, w, ~] = size(lab);

b = max(5, round(0.04 * min(h, w)));
borderMask = true(h, w);
borderMask(b+1:end-b, b+1:end-b) = false;
bg = zeros(1, 3);
for c = 1:3
    ch = lab(:,:,c);
    bg(c) = median(ch(borderMask));
end

dist = sqrt((lab(:,:,1) - bg(1)).^2 + ...
            (lab(:,:,2) - bg(2)).^2 + ...
            (lab(:,:,3) - bg(3)).^2);
dist = mat2gray(dist);

raw     = imbinarize(dist, graythresh(dist));
opened  = bwareafilt(imopen(raw, strel('disk', 3)), 1);
cleaned = bwareafilt(imfill(imclose(opened, strel('disk', 5)), 'holes'), 1);
mask    = cleaned;

% `clusters` is empty for this method; `union` carries the Otsu result so
% the dashboard can show the same slot either way.
stages = struct('clusters', [], 'union', raw, ...
                'opened', opened, 'cleaned', cleaned);
end


%% =====================================================================
function m = clean_mask(m)
% Morphological clean-up (Unit 4).
% The largest blob is taken BEFORE closing: closing first can bridge the
% leaf to a nearby shadow, and then "largest blob" keeps both as one.
m = imopen(m, strel('disk', 3));     % erosion then dilation: drop specks
m = bwareafilt(m, 1);                % keep the single largest object
m = imclose(m, strel('disk', 5));    % dilation then erosion: close gaps
m = imfill(m, 'holes');              % fill interior holes
m = bwareafilt(m, 1);
end


%% =====================================================================
function f = border_contact(m)
% Fraction of the image border occupied by the mask.
f = mean([m(1,:), m(end,:), m(:,1)', m(:,end)']);
end


%% =====================================================================
function tf = plausible(m)
% A usable leaf mask covers a sensible area and does not hug the border.
f = nnz(m) / numel(m);
tf = f > 0.02 && f < 0.92 && border_contact(m) < 0.50;
end

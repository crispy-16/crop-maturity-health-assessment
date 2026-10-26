% matlab/leaf_features.m
% 41 numbers describing one segmented leaf.
% Measured on `den` (median filtered, NOT contrast equalised).
%
% Groups: colour (10) | lesion area (6) | lesion geometry (3) |
%         texture (6) | leaf shape (6) | granulometry (5) |
%         specks (2) | frequency (3)
function [f, names] = leaf_features(den, mask, M)

f = [];  names = {};
    function add(nm, v)
        f(end+1) = double(v);  names{end+1} = nm;  %#ok<AGROW>
    end

lab = rgb2lab(den);  hsv = rgb2hsv(den);
area = max(nnz(mask), 1);

% ---- Colour: mean and std of each channel inside the leaf ------------
chans = {lab(:,:,1), lab(:,:,2), lab(:,:,3), hsv(:,:,2), hsv(:,:,3)};
cn    = {'L', 'a', 'b', 'S', 'V'};
for k = 1:5
    v = chans{k}(mask);
    add(['mean_' cn{k}], mean(v));
    add(['std_'  cn{k}], std(v));
end

% ---- Lesion area fractions -------------------------------------------
add('frac_healthy',   nnz(M.healthy)   / area);
add('frac_chlorotic', nnz(M.chlorotic) / area);
add('frac_necrotic',  nnz(M.necrotic)  / area);
add('frac_powdery',   nnz(M.powdery)   / area);
add('frac_sooty',     nnz(M.sooty)     / area);
add('frac_lesion',    nnz(M.lesion)    / area);

% ---- Lesion geometry: how many blobs and how big ---------------------
cc = bwconncomp(M.lesion);
blobAreas = cellfun(@numel, cc.PixelIdxList);
blobAreas = blobAreas(blobAreas > 15);        % ignore single-pixel noise
add('lesion_count',     min(numel(blobAreas), 500) / 100);
if isempty(blobAreas)
    add('lesion_mean_area', 0);  add('lesion_max_area', 0);
else
    add('lesion_mean_area', mean(blobAreas) / area);
    add('lesion_max_area',  max(blobAreas)  / area);
end

% ---- Texture: local entropy + GLCM ------------------------------------
gray = rgb2gray(den);
ent  = entropyfilt(gray, true(11));
add('mean_entropy', mean(ent(mask)));
add('std_entropy',  std(ent(mask)));

st = regionprops(mask, 'BoundingBox', 'Area', 'Eccentricity', 'Solidity', ...
                       'Extent', 'Perimeter', 'ConvexArea');
bb = round(st(1).BoundingBox);
r1 = max(bb(2), 1);  r2 = min(bb(2) + bb(4) - 1, size(gray, 1));
c1 = max(bb(1), 1);  c2 = min(bb(1) + bb(3) - 1, size(gray, 2));
crop = gray(r1:r2, c1:c2);
cm   = mask(r1:r2, c1:c2);
crop(~cm) = uint8(mean(crop(cm)));            % neutral fill outside the leaf
glcm = graycomatrix(crop, 'NumLevels', 32, 'Offset', [0 1; -1 1; -1 0; -1 -1]);
gp = graycoprops(glcm, {'Contrast', 'Homogeneity', 'Energy', 'Correlation'});
add('glcm_contrast',    mean(gp.Contrast));
add('glcm_homogeneity', mean(gp.Homogeneity));
add('glcm_energy',      mean(gp.Energy));
add('glcm_correlation', mean(gp.Correlation));

% ---- Leaf shape: chewed margins lower solidity and circularity -------
add('area_fraction', st(1).Area / numel(mask));
add('eccentricity',  st(1).Eccentricity);
add('solidity',      st(1).Solidity);
add('extent',        st(1).Extent);
add('circularity',   4 * pi * st(1).Area / (st(1).Perimeter^2 + eps));
add('convex_deficiency', 1 - st(1).Area / max(st(1).ConvexArea, 1));

% ---- Granulometry: lesion size distribution via successive openings --
% Fraction of lesion area destroyed by an opening of radius r. Many tiny
% specks lose area at small r; a few big blotches lose area at large r.
radii = [1 2 4 8 16];
total = nnz(M.lesion);
prev  = total;
for r = radii
    if total == 0
        add(sprintf('gran_%d', r), 0);
    else
        aLeft = nnz(imopen(M.lesion, strel('disk', r)));
        add(sprintf('gran_%d', r), (prev - aLeft) / total);
        prev = aLeft;
    end
end

% ---- Specks: black top-hat finds small dark spots on a lighter leaf --
bh = imbothat(gray, strel('disk', 5));
v  = double(bh(mask));
if isempty(v)
    sp = false(size(mask));
else
    sv  = sort(v);
    p99 = sv(max(1, ceil(0.99 * numel(sv))));      % 99th percentile
    thr = max(0.05 * 255, p99 * 0.5);
    sp  = imopen(bh > thr & mask, strel('disk', 1));
end
add('speck_frac',  nnz(sp) / area);
nSp = bwconncomp(sp).NumObjects;
add('speck_count', min(nSp, 500) / 100);

% ---- Frequency: Unit 2, fraction of DFT energy in 3 radial bands -----
% Computed on the LEAF, not the whole frame: `crop` is the bounding box
% with everything outside the mask replaced by the leaf's mean grey level
% (the same neutral fill used for the GLCM above).
%
% Measured on 946 images: taking the DFT over the whole frame made these
% features look useful (random-forest rank 13 of 44) but they were partly
% reading the photo's BACKGROUND, which differs between capture sessions.
% Masked, they rank 41 of 44 - the leaf's own frequency content adds
% nothing beyond the entropy and GLCM features. Accuracy is the same
% either way (97.0%), so the masked version is kept because it measures
% what it claims to.
gf = im2double(imresize(crop, [256 256]));
F = fftshift(fft2(gf));
P = abs(F).^2;
P(129, 129) = 0;                       % remove the DC term
[X, Y] = meshgrid(1:256, 1:256);
R = hypot(X - 129, Y - 129);
tot = sum(P(:));
if tot <= 0, tot = 1; end
add('dft_low',  sum(P(R <= 16))             / tot);
add('dft_mid',  sum(P(R > 16 & R <= 48))    / tot);
add('dft_high', sum(P(R > 48))              / tot);
end

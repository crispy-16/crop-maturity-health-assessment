% matlab/leaf_lesions.m
% Unit 4: colour image processing + morphological image processing.
%
% Every pixel inside the leaf mask is put into one of five classes using
% L*a*b* (perceptually uniform, so one threshold works on the white, grey
% and blue backgrounds in the dataset) plus HSV saturation:
%
%   healthy    a* <= -8 and S >= 0.20      chlorophyll green
%   sooty      L* < 22                     black deposit / deep necrosis
%   powdery    S < 0.20 and L* >= 40       whitish-grey coating
%   chlorotic  -8 < a* < 8 and b* >= 14    yellowing
%   necrotic   everything else             brown dead tissue
%
% Each lesion class is then cleaned with an opening (removes isolated
% pixels) followed by a closing (joins neighbouring lesion pixels).
function M = leaf_lesions(den, mask)

A_GREEN  = -8;    S_MIN = 0.20;
L_SOOTY  = 22;    L_POWDER = 40;   B_YELLOW = 14;

lab = rgb2lab(den);
hsv = rgb2hsv(den);
L = lab(:,:,1);  a = lab(:,:,2);  b = lab(:,:,3);
S = hsv(:,:,2);

healthy   = mask & a <= A_GREEN & S >= S_MIN & L >= L_SOOTY;
sooty     = mask & L < L_SOOTY;
powdery   = mask & S < S_MIN & L >= L_POWDER & ~sooty;
chlorotic = mask & ~healthy & ~sooty & ~powdery & ...
            a > A_GREEN & a < 8 & b >= B_YELLOW & S >= S_MIN;
necrotic  = mask & ~(healthy | sooty | powdery | chlorotic);

% ---- morphological clean-up of each lesion class ---------------------
se = strel('disk', 2);
chlorotic = imclose(imopen(chlorotic, se), se) & mask;
necrotic  = imclose(imopen(necrotic,  se), se) & mask;
powdery   = imclose(imopen(powdery,   se), se) & mask;
sooty     = imclose(imopen(sooty,     se), se) & mask;

lesion  = (chlorotic | necrotic | powdery | sooty) & mask;
healthy = mask & ~lesion;

M = struct('healthy', healthy, 'chlorotic', chlorotic, 'necrotic', necrotic, ...
           'powdery', powdery, 'sooty', sooty, 'lesion', lesion, 'mask', mask);
end

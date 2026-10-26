# CropVision: Crop Maturity and Health Assessment

A Digital Image Processing mini project. Classical image processing in MATLAB
does the analysis; a Streamlit dashboard shows every step.

The app has two sections:

| Section | MATLAB entry point | Question answered |
|---|---|---|
| **Mango ripeness** | `matlab/crop_pipeline.m` | How ripe is this mango? |
| **Leaf disease** | `matlab/run_leaf_dashboard.m` | Is this mango leaf diseased, which disease, how badly? |

Each section's **Image Processing** page has two tabs:
*Pipeline* shows only the images passed from one stage to the next, and
*Other transforms* shows the remaining outputs (difference views, colour
channels, edges and so on), each captioned with the transform that made it.

## Pipelines

**Mango ripeness** (`crop_pipeline.m`): resize → 3×3 median filter →
histogram equalisation of V → k-means on a\*, b\* and distance from centre →
initial mask → Chan-Vese active contour → morphological clean-up →
segmented fruit → colour, texture, shape and DFT features.

**Leaf disease** (`run_leaf_dashboard.m`): resize → 3×3 median filter →
k-means in L\*a\*b\* (border clusters = background) → opening, closing,
hole fill → five tissue classes (healthy, chlorotic, necrotic, powdery,
sooty) → 41 features → condition, affected area and severity.
Details: [docs/LEAF_PIPELINE.md](docs/LEAF_PIPELINE.md).

## Repository layout

```
app.py                      Streamlit entry point (home screen + routing)
src/ui/                     pages, components, theme and animations
src/backend/matlab_bridge.py runs the MATLAB pipelines, reads results.json
matlab/                     all MATLAB code
  crop_pipeline.m           mango pipeline (also runs stand-alone with one argument)
  run_leaf_dashboard.m      leaf pipeline entry point for the app
  leaf_preprocess.m  segment_leaf.m  leaf_lesions.m  leaf_features.m  classify_leaf.m
  watch_leaf.m              folder watcher: lets the app reach MATLAB without the Engine
  run_leaf.m                leaf pipeline on one image, with figures
  run_transforms.m          quantisation, 2-D DFT and frequency-domain filter figures
  run_training.m            builds leaf_features.csv and trains leaf_model.mat
  run_cnn.m  leaf_cnn_demo.m  check_cnn.m  cnn_setup.m  cnn_activations.m
                            optional CNN comparison (Deep Learning Toolbox)
docs/LEAF_PIPELINE.md       leaf pipeline design notes
outputs/                    results written by the app (not committed)
```

## Requirements

- MATLAB with the Image Processing Toolbox. The Statistics and Machine
  Learning Toolbox is needed only to train the leaf classifier
  (`run_training.m`); without it the leaf condition comes from a rule-based
  fallback and k-means uses `imsegkmeans`.
- Python 3.10+.

## Running

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The app reaches MATLAB in one of two ways, picked automatically:

1. **MATLAB Engine for Python** (`pip install matlabengine` matching your
   MATLAB version). Nothing else to start.
2. **Folder watcher** (no Engine needed). In MATLAB:
   ```matlab
   cd <this repo>\matlab
   watch_leaf
   ```
   and leave it running.

Then start the app:

```powershell
python -m streamlit run app.py
```

Choose a section on the home screen, upload an image and click
**Analyze image**. The sidebar shows whether MATLAB is reachable.
Results are cached per image in `outputs/dashboard/<mode>-<id>/`.

Optional: put MangoLeafBD in `dataset/MangoLeafBD/<Class>/` and run
`run_training.m` in MATLAB to train the leaf classifier.

## Scope

Image-based assessment of visible characteristics only. No treatment advice.

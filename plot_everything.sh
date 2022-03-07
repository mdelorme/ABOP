#!/bin/bash

# 1.3
echo "Section 1.3"
for e in 0 1 2 3 4 5 6 7 8 9; do
  echo " . Case $e"
  python3 ch1/1.3.py $e
done
montage img_1.3_*png -geometry '800x800' mosaic_1.3.png
echo " - Mosaic stored in mosaic_1.3.png"
rm img_1.3*

# 1.4
echo "Section 1.4"
for e in 0 1 2 3 4 5 6 7 8; do
  echo " . Case $e"
  python3 ch1/1.4.py $e
done
montage img_1.4_*png -geometry '800x800' mosaic_1.4.png
echo " - Mosaic stored in mosaic_1.4.png"
rm img_1.4*

# 1.5
echo "Section 1.5"
python3 ch1/1.5.py
echo " - Saved to 1_5.png"

# 1.6
echo "Section 1.6"
for e in 0 1 2 3 4 5; do
  echo " . Case $e"
  python3 ch1/1.6.py $e
done
montage img_1.6_*png -geometry '800x800' mosaic_1.6.png
echo " - Mosaic stored in mosaic_1.6.png"
rm img_1.6*

# 1.7
echo "Section 1.7"
for e in 32376 23984 27283 12398 27384 99938; do
  echo " . Seed $e"
  python3 ch1/1.7.py $e
done
montage img_1.7_*png -geometry '800x800' mosaic_1.7.png
echo " - Mosaic stored in mosaic_1.7.png"
rm img_1.7*

# 1.8
echo "Section 1.8"
for e in 0 1 2 3 4; do
  echo " . Case $e"
  python3 ch1/1.8.py $e
done
montage img_1.8_*png -geometry '800x800' mosaic_1.8.png
echo " - Mosaic stored in mosaic_1.8.png"
rm img_1.8*
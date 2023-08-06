make clean
make -j CXXFLAGS="-std=c++11" sift_roi
cp sift_roi sift_roi_noflags
make clean
make -j sift_roi

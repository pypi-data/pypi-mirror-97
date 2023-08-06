import svox

t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/nerf_synthetic_v2/lego_v2.npz")
print(t)
t.quantize_median_cut(8)
print(t)
t.save('quant_exp_8.npz', compress=True, strip=True)

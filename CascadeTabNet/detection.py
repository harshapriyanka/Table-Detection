import numpy as np

score_thr = 0.85

for i, arr in enumerate(result[0]):
    bboxes = []
    if arr.shape[1] == 5 and len(arr)!=0:
        print(len(arr))
        scores = arr[:, -1]
        inds = scores > score_thr
        bboxes.append(arr[inds, :])
        path = 'output'+str(i)+'.npy'
        np.save(path, bboxes)
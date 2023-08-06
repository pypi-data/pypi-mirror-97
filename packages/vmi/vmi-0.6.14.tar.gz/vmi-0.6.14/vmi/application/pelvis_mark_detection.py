import segmentation_models as sm
from tensorflow.python.keras.optimizers import Nadam
from tensorflow.python.keras.losses import categorical_crossentropy
import numpy as np


def get_pts(img):
    model = sm.Unet('resnet34', classes=6,
                    input_shape=(512, 512, 3),
                    activation='sigmoid')
    model.compile(optimizer=Nadam(), loss=categorical_crossentropy, metrics=[categorical_crossentropy])
    img = img.swapaxes(0, 2)
    img[img < 100] = 100
    img[img > 400] = 400

    x_f = img.sum(axis=1)
    x_t = img.sum(axis=2)

    if x_f.shape[0] <= 512 and x_f.shape[1] <= 512 and x_t.shape[0] <= 512 and x_t.shape[1] <= 512:

        x_start_f = (512 - x_f.shape[0]) // 2
        y_start_f = (512 - x_f.shape[1]) // 2
        x_start_t = (512 - x_t.shape[0]) // 2
        y_start_t = (512 - x_t.shape[1]) // 2
        x_input_f = np.zeros((1, 512, 512, 3))
        x_input_t = np.zeros((1, 512, 512, 3))

        x_input_f[0, x_start_f:x_start_f + x_f.shape[0], y_start_f:y_start_f + x_f.shape[1], 0] = x_f
        x_input_f[0, x_start_f:x_start_f + x_f.shape[0], y_start_f:y_start_f + x_f.shape[1], 1] = x_f
        x_input_f[0, x_start_f:x_start_f + x_f.shape[0], y_start_f:y_start_f + x_f.shape[1], 2] = x_f

        x_input_t[0, x_start_t:x_start_t + x_t.shape[0], y_start_t:y_start_t + x_t.shape[1], 0] = x_t
        x_input_t[0, x_start_t:x_start_t + x_t.shape[0], y_start_t:y_start_t + x_t.shape[1], 1] = x_t
        x_input_t[0, x_start_t:x_start_t + x_t.shape[0], y_start_t:y_start_t + x_t.shape[1], 2] = x_t

        x_input_f = x_input_f / x_input_f.max()
        x_input_t = x_input_t / x_input_t.max()

        model.load_weights('mark_locate_f.h5py')
        pre_f = model.predict(x_input_f)[0]
        model.load_weights('mark_locate_t.h5py')
        pre_t = model.predict(x_input_t)[0]

        pts_dict = {}
        arr_pair = []
        for layer in range(6):
            img_layer_f = pre_f[:, :, layer]
            img_layer_t = pre_t[:, :, layer]
            pts_pos_f = np.where(img_layer_f > 0.9)
            pts_pos_t = np.where(img_layer_t > 0.9)

            x = pts_pos_f[0].mean() - x_start_f
            z = pts_pos_f[1].mean() - y_start_f
            y = pts_pos_t[1].mean() - y_start_t

            arr = np.array([x, y, z])
            arr_pair.append(arr)
        for i in range(3):
            pts_dict['泪滴'] = np.array([arr_pair[0], arr_pair[1]])
            pts_dict['耻骨结节'] = np.array([arr_pair[2], arr_pair[3]])
            pts_dict['髂前上棘'] = np.array([arr_pair[4], arr_pair[5]])
        return pts_dict
    else:
        print('输入图像大于512pix')

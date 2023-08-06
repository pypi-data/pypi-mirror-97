import os.path
import unittest

import numpy as np

import dito


class TestCase(unittest.TestCase):
    """
    Base class for test cases.
    """
    
    def assertNumpyShape(self, image, shape):
        self.assertIsInstance(image, np.ndarray)
        self.assertEqual(image.shape, shape)
    
    def assertIsImage(self, x):
        self.assertTrue(dito.is_image(image=x))
    
    def assertEqualImageContainers(self, x, y):
        self.assertIsImage(x)
        self.assertIsImage(y)
        self.assertEqual(x.dtype, y.dtype)
        self.assertEqual(x.shape, y.shape)
    
    def assertEqualImages(self, x, y):
        self.assertEqualImageContainers(x, y)
        if np.issubdtype(x.dtype, np.floating):
            self.assertTrue(np.allclose(x, y))
        else:
            self.assertTrue(np.all(x == y))


class clip_Tests(TestCase):
    def test_clip_01(self):
        image = np.array([[-2.0, -1.0, 0.0, 1.0, 2.0]], dtype=np.float32)
        image_clipped = dito.clip_01(image=image)
        image_expected = np.array([[0.0, 0.0, 0.0, 1.0, 1.0]], dtype=np.float32)
        self.assertEqualImages(image_clipped, image_expected)

    def test_clip_input_unchanged(self):
        image = np.array([[-2.0, -1.0, 0.0, 1.0, 2.0]], dtype=np.float32)
        image_copy = image.copy()
        image_clipped = dito.clip_01(image=image)
        self.assertEqualImages(image, image_copy)


class colorize_Tests(TestCase):
    def test_colorize_colormap(self):
        image = dito.xslope(height=32, width=256)
        self.assertTrue(dito.is_gray(image=image))
        image_colorized = dito.colorize(image=image, colormap=dito.get_colormap(name="jet"))
        self.assertTrue(dito.is_color(image=image_colorized))

    def test_colorize_name(self):
        image = dito.xslope(height=32, width=256)
        self.assertTrue(dito.is_gray(image=image))
        image_colorized = dito.colorize(image=image, colormap="jet")
        self.assertTrue(dito.is_color(image=image_colorized))


class convert_Tests(TestCase):
    def test_convert_identical(self):
        image = dito.xslope(height=32, width=256)
        image_converted = dito.convert(image=image, dtype=np.uint8)
        self.assertEqualImages(image, image_converted)

    def test_convert_loop(self):
        image = dito.xslope(height=32, width=256)
        image_converted = dito.convert(image=image, dtype=np.float32)
        image_converted_2 = dito.convert(image=image_converted, dtype=np.uint8)
        self.assertEqualImages(image, image_converted_2)

    def test_convert_uint8_float32(self):
        image = dito.xslope(height=32, width=256)
        image_converted = dito.convert(image=image, dtype=np.float32)
        self.assertAlmostEqual(np.min(image_converted), 0.0)
        self.assertAlmostEqual(np.max(image_converted), 1.0)

    def test_convert_bool_uint8(self):
        image = np.array([[False, True]], dtype=np.bool_)
        image_converted = dito.convert(image=image, dtype=np.uint8)
        self.assertEqual(image_converted[0, 0], 0)
        self.assertEqual(image_converted[0, 1], 255)

    def test_convert_color(self):
        image_gray = dito.xslope(height=32, width=256)
        image_color = dito.as_color(image=image_gray.copy())
        image_gray_converted = dito.convert(image=image_gray, dtype=np.float32)
        image_color_converted = dito.convert(image=image_color, dtype=np.float32)
        self.assertEqualImages(image_gray_converted, dito.as_gray(image=image_color_converted))

    def test_convert_input_unchanged(self):
        image = np.array([[-2.0, -1.0, 0.0, 1.0, 2.0]], dtype=np.float32)
        image_copy = image.copy()
        dito.convert(image=image, dtype=np.uint8)
        self.assertEqualImages(image, image_copy)

    def test_convert_float_clipped(self):
        image = np.array([[-2.0, -1.0, 0.0, 1.0, 2.0]], dtype=np.float32)
        image_clipped = dito.convert(image=image, dtype=np.float32)
        self.assertAlmostEqual(np.min(image_clipped), 0.0)
        self.assertAlmostEqual(np.max(image_clipped), 1.0)


class dtype_common_Test(TestCase):
    def test_dtype_common_cases(self):
        cases = [
            {"arg": ["uint8"], "expected_result": np.uint8},
            {"arg": ["uint8", "uint8"], "expected_result": np.uint8},
            {"arg": ["uint8", "bool"], "expected_result": np.uint8},
            {"arg": ["bool", "uint8"], "expected_result": np.uint8},
            {"arg": ["bool", "uint8", "uint16"], "expected_result": np.uint16},
            {"arg": ["uint8", "uint16"], "expected_result": np.uint16},
            {"arg": ["uint8", "float32"], "expected_result": np.float32},
            {"arg": ["uint8", "float64"], "expected_result": np.float64},
            {"arg": ["float32", "float64"], "expected_result": np.float64},
            {"arg": ["double"], "expected_result": np.float64},
            {"arg": [np.uint8], "expected_result": np.uint8},
            {"arg": [np.bool_, "uint8", np.uint16], "expected_result": np.uint16},
        ]
        for case in cases:
            result = dito.dtype_common(dtypes=case["arg"])
            self.assertEqual(result, case["expected_result"])

    def test_dtype_common_raise(self):
        self.assertRaises(ValueError, lambda: dito.dtype_common(dtypes=["__non-existing-dtype__"]))


class dtype_range_Tests(TestCase):
    def test_dtype_range_uint8(self):
        range_ = dito.dtype_range(dtype=np.uint8)
        self.assertEqual(range_, (0, 2**8 - 1))
        
    def test_dtype_range_uint16(self):
        range_ = dito.dtype_range(dtype=np.uint16)
        self.assertEqual(range_, (0, 2**16 - 1))
    
    def test_dtype_range_uint32(self):
        range_ = dito.dtype_range(dtype=np.uint32)
        self.assertEqual(range_, (0, 2**32 - 1))
    
    def test_dtype_range_int8(self):
        range_ = dito.dtype_range(dtype=np.int8)
        self.assertEqual(range_, (-2**7, 2**7 - 1))
    
    def test_dtype_range_int16(self):
        range_ = dito.dtype_range(dtype=np.int16)
        self.assertEqual(range_, (-2**15, 2**15 - 1))
    
    def test_dtype_range_int32(self):
        range_ = dito.dtype_range(dtype=np.int32)
        self.assertEqual(range_, (-2**31, 2**31 - 1))
    
    def test_dtype_range_float(self):
        range_ = dito.dtype_range(dtype=np.float)
        self.assertEqual(range_, (0, 1.0))
    
    def test_dtype_range_float32(self):
        range_ = dito.dtype_range(dtype=np.float32)
        self.assertEqual(range_, (0, 1.0))
        
    def test_dtype_range_float64(self):
        range_ = dito.dtype_range(dtype=np.float64)
        self.assertEqual(range_, (0, 1.0))
        
    def test_dtype_range_bool(self):
        range_ = dito.dtype_range(dtype=np.bool_)
        self.assertEqual(range_, (False, True))


class get_colormap_Tests(TestCase):
    def test_get_colormap_plot(self):
        result = dito.get_colormap("plot")
        self.assertTrue(dito.is_colormap(result))
        self.assertEqual(result[0, 0, :].tolist(), [0, 0, 0])
        self.assertEqual(result[1, 0, :].tolist(), [0, 0, 255])
        self.assertEqual(result[2, 0, :].tolist(), [0, 255, 0])
        self.assertEqual(result[3, 0, :].tolist(), [255, 0, 0])
        self.assertEqual(result[255, 0, :].tolist(), [255, 255, 255])

    def test_get_colormap_jet(self):
        result = dito.get_colormap("jet")
        self.assertTrue(dito.is_colormap(result))

    def test_get_colormap_raise(self):
        self.assertRaises(ValueError, lambda: dito.get_colormap("__!?-non-existing_colormap-name-!?__"))


class normalize_Tests(TestCase):
    def run_in_out_test(self, image_in, image_out, **kwargs):
        image_normalized = dito.normalize(image=image_in, **kwargs)
        self.assertEqualImages(image_normalized, image_out)
    
    def test_normalize_none_uint8(self):
        self.run_in_out_test(
            image_in=np.array([[0, 1, 2]], dtype=np.uint8),
            image_out=np.array([[0, 1, 2]], dtype=np.uint8),
            mode="none",
        )
    
    def test_normalize_minmax_uint8(self):
        self.run_in_out_test(
            image_in=np.array([[0, 1, 2]], dtype=np.uint8),
            image_out=np.array([[0, 127, 255]], dtype=np.uint8),
            mode="minmax",
        )
    
    def test_normalize_minmax_int8(self):
        self.run_in_out_test(
            image_in=np.array([[0, 1, 2]], dtype=np.int8),
            image_out=np.array([[-128, 0, 127]], dtype=np.int8),
            mode="minmax",
        )
    
    def test_normalize_minmax_float32(self):
        self.run_in_out_test(
            image_in=np.array([[-1.0, 0.0, 1.0]], dtype=np.float32),
            image_out=np.array([[0.0, 0.5, 1.0]], dtype=np.float32),
            mode="minmax",
        )
    
    def test_normalize_zminmax_float32(self):
        self.run_in_out_test(
            image_in=np.array([[-1.0, 0.0, 1.0, 2.0]], dtype=np.float32),
            image_out=np.array([[0.25, 0.5, 0.75, 1.0]], dtype=np.float32),
            mode="zminmax",
        )
    
    def test_normalize_percentile_uint8_q(self):
        self.run_in_out_test(
            image_in=np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], dtype=np.uint8),
            image_out=np.array([[0, 0, 31, 63, 95, 127, 159, 191, 223, 255, 255]], dtype=np.uint8),
            mode="percentile",
            q=10.0,
        )
    
    def test_normalize_percentile_uint8_p(self):
        self.run_in_out_test(
            image_in=np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], dtype=np.uint8),
            image_out=np.array([[0, 0, 31, 63, 95, 127, 159, 191, 223, 255, 255]], dtype=np.uint8),
            mode="percentile",
            p=10.0,
        )
    
    def test_normalize_raise_invalid_mode(self):
        image = np.array([[0, 1, 2]], dtype=np.uint8)
        self.assertRaises(ValueError, lambda: dito.normalize(image=image, mode="__NON-EXISTING-MODE__"))


class stack_Tests(TestCase):
    def test_stack_mixed(self):
        # TODO: create more individual tests
        rows = [
            [
                dito.xslope(height=32, width=256),
                dito.as_color(image=dito.xslope(height=64, width=128)),
            ],
            [
                np.ones(shape=(100, 100), dtype=np.bool_),
            ],
        ]
        image_stacked = dito.stack(rows, padding=8, background_color=127)
        self.assertTrue(image_stacked.dtype == np.uint8)
        self.assertTrue(dito.is_color(image=image_stacked))
        self.assertEqual(image_stacked.shape, (188, 408, 3))
        self.assertEqual(image_stacked[0, 0, 0], 127)
        self.assertEqual(image_stacked[90, 10, 0], 255)

    def test_stack_single_row(self):
        row = [
            dito.xslope(height=32, width=256),
            dito.as_color(image=dito.xslope(height=64, width=128)),
        ]
        image_stacked = dito.stack(images=row)
        image_stacked_2 = dito.stack(images=[row])
        self.assertEqualImages(image_stacked, image_stacked_2)

    def test_stack_raise_on_single_image(self):
        image = dito.xslope(height=32, width=256)
        self.assertRaises(ValueError, lambda: dito.stack(images=image))

    def test_stack_raise_on_non_image(self):
        rows = [[0, 1, 2], [3, 4, 5]]
        self.assertRaises(ValueError, lambda: dito.stack(images=rows))


class text_Tests(TestCase):
    def test_text_input_unchanged(self):
        image = dito.pm5544()
        image_copy = image.copy()
        dito.text(image=image, message="Hello World", position=(0.5, 0.5), anchor="cc")
        self.assertEqualImages(image, image_copy)


####
#%%% TODO: refactor
####


class aliases_Tests(TestCase):
    def test_otsu_raise(self):
        image = dito.pm5544()
        self.assertRaises(ValueError, lambda: dito.otsu(image=image))
        
    def test_otsu_return(self):
        image = dito.pm5544()
        image_gray = dito.as_gray(image)
        result = dito.otsu(image=image_gray)
        self.assertIsInstance(result, tuple)
        self.assertTrue(len(result) == 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], np.ndarray)
    
    def test_otsu_theta(self):
        image = dito.pm5544()
        image_gray = dito.as_gray(image)
        theta = dito.otsu_theta(image=image_gray)
        self.assertIsInstance(theta, float)
        self.assertAlmostEqual(theta, 89.0)


class core_Tests(TestCase):
    def test_is_gray(self):
        image = dito.pm5544()
        self.assertFalse(dito.is_gray(image))
        self.assertTrue(dito.is_gray(image[:, :, 0]))
        self.assertTrue(dito.is_gray(image[:, :, 0:1]))
        self.assertFalse(dito.is_gray(image[:, :, 0:2]))
    
    def test_is_color(self):
        image = dito.pm5544()
        self.assertTrue(dito.is_color(image))
        self.assertFalse(dito.is_color(image[:, :, 0]))
        self.assertFalse(dito.is_color(image[:, :, 0:1]))
        self.assertFalse(dito.is_color(image[:, :, 0:2]))
    
    def test_as_gray(self):
        image = dito.pm5544()
        self.assertTrue(dito.is_color(image))
        image_g = dito.as_gray(image)
        self.assertTrue(dito.is_gray(image_g))
        self.assertEqual(image_g.shape, image.shape[:2])
    
    def test_as_gray_noop(self):
        image = dito.pm5544()
        image_b = image[:, :, 0]
        self.assertEqualImages(image_b, dito.as_gray(image_b))
        
    def test_as_color(self):
        image = dito.pm5544()
        image_b = image[:, :, 0]
        image_c = dito.as_color(image_b)
        self.assertTrue(dito.is_color(image_c))
        self.assertEqual(image_c.shape, image_b.shape + (3,))
        for n_channel in range(3):
            self.assertEqualImages(image_c[:, :, n_channel], image_b)
    
    def test_as_color_noop(self):
        image = dito.pm5544()
        self.assertEqualImages(image, dito.as_color(image))
    
    def test_flip_channels_values(self):
        image = dito.pm5544()
        image_flipped = dito.flip_channels(image=image)
        for n_channel in range(3):
            self.assertEqualImages(image[:, :, n_channel], image_flipped[:, :, 2 - n_channel])
        
    def test_flip_channels_once_neq(self):
        image = dito.pm5544()
        image_flipped = dito.flip_channels(image=image)
        self.assertEqualImageContainers(image, image_flipped)
        self.assertFalse(np.all(image == image_flipped))
        
    def test_flip_channels_twice(self):
        image = dito.pm5544()
        image_flipped = dito.flip_channels(image=image)
        image_flipped_flipped = dito.flip_channels(image=image_flipped)
        self.assertEqualImages(image, image_flipped_flipped)


class data_Tests(TestCase):
    def test_data_dir_exists(self):
        self.assertTrue(os.path.exists(dito.DATA_DIR))
    
    def test_data_files_exists(self):
        for filename in dito.DATA_FILENAMES.values():
            self.assertTrue(os.path.exists(filename), "Data file '{}' does not exist".format(filename))



    def test_pm5544_load(self):
        image = dito.pm5544()
        self.assertIsImage(image)
        self.assertEqual(image.shape, (576, 768, 3))
    
    def test_xslope_width256(self):
        for height in (1, 32):
            slope = dito.xslope(height=height, width=256)
            self.assertIsImage(slope)
            self.assertEqual(slope.dtype, np.uint8)
            self.assertEqual(slope.shape, (height, 256))
            for x in range(256):
                for y in range(height):
                    self.assertEqual(slope[y, x], x)
    
    def test_xslope_widthNot256(self):
        height = 1
        for width in (2, 32, 256, 1000):
            slope = dito.xslope(height=height, width=width)
            self.assertIsImage(slope)
            self.assertEqual(slope.dtype, np.uint8)
            self.assertEqual(slope.shape, (height, width))
            for y in range(height):
                self.assertEqual(slope[y, 0], 0)
                self.assertEqual(slope[y, width - 1], 255)

    def test_yslope(self):
        height = 256
        width = 32
        slope = dito.yslope(width=width, height=height)
        self.assertIsImage(slope)
        self.assertEqual(slope.dtype, np.uint8)
        self.assertEqual(slope.shape, (height, width))
        for x in range(width):
            for y in range(height):
                self.assertEqual(slope[y, x], y)


class geometry_Tests(TestCase):
    def test_size(self):
        image = dito.pm5544()
        self.assertEqual(dito.size(image), (768, 576))

    def test_resize_scale(self):
        image = dito.pm5544()
        image2 = dito.resize(image, 0.5)
        self.assertEqual(image2.shape, (288, 384, 3))
        
    def test_resize_size(self):
        image = dito.pm5544()
        image2 = dito.resize(image, (384, 288))
        self.assertEqual(image2.shape, (288, 384, 3))


class infos_Tests(TestCase):
    def test_info(self):
        image = dito.pm5544()
        info = dito.info(image)
        self.assertEqual(info["shape"], (576, 768, 3))
        self.assertAlmostEqual(info["mean"], 121.3680261682581)
        self.assertAlmostEqual(info["std"], 91.194048489528782)
        self.assertEqual(info["min"], 0)
        self.assertAlmostEqual(info["3rd quartile"], 191.0)
        self.assertEqual(info["max"], 255)
        
    def test_hist_color(self):
        image = dito.pm5544()
        h = dito.hist(image, bin_count=256)
        self.assertAlmostEqual(h[0], 328389.0)
        self.assertAlmostEqual(h[6], 1512.0)
        self.assertAlmostEqual(h[86], 0.0)
        self.assertAlmostEqual(h[122], 330802.0)
        self.assertAlmostEqual(h[134], 7.0)
        self.assertAlmostEqual(h[191], 112044.0)
        self.assertAlmostEqual(h[195], 3.0)
        self.assertAlmostEqual(h[255], 212526.0)
        
    def test_hist_gray(self):
        image = dito.pm5544()
        image_b = image[:, :, 0]
        h = dito.hist(image_b, bin_count=256)
        self.assertAlmostEqual(h[11], 18036.0)
        self.assertAlmostEqual(h[73], 88.0)
        self.assertAlmostEqual(h[170], 2528.0)
        self.assertAlmostEqual(h[255], 70842.0)
    
    def test_hist_gray_2dim_vs_3dim(self):
        image = dito.pm5544()
        
        image_2dim = image[:, :, 0]
        h_2dim = dito.hist(image_2dim, bin_count=256)
        
        image_3dim = image_2dim.copy()
        image_3dim.shape = image_3dim.shape + (1,)
        h_3dim = dito.hist(image_3dim, bin_count=256)
        
        self.assertEqual(len(h_2dim), len(h_3dim))
        for (value_2dim, value_3dim) in zip(h_2dim, h_3dim):
            self.assertAlmostEqual(value_2dim, value_3dim)
            
    def test_hist_gray_vs_color(self):
        image = dito.pm5544()
        
        image_b = image[:, :, 0]
        image_g = image[:, :, 1]
        image_r = image[:, :, 2]

        h_sum = dito.hist(image_b, bin_count=256) + dito.hist(image_g, bin_count=256) + dito.hist(image_r, bin_count=256)
        h_color = dito.hist(image, bin_count=256)
        
        self.assertEqual(len(h_sum), len(h_color))
        for (value_sum, value_color) in zip(h_sum, h_color):
            self.assertAlmostEqual(value_sum, value_color)


class io_Tests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_filename = os.path.join(dito.DATA_FILENAMES["image:PM5544"])
        self.shape = (576, 768, 3)
    
    def test_load_default(self):
        image = dito.load(filename=self.image_filename)
        self.assertNumpyShape(image, self.shape)
        self.assertAlmostEqual(np.mean(image), 121.3680261682581)
        
    def test_load_grayscale(self):
        image = dito.load(filename=self.image_filename, color=False)
        self.assertNumpyShape(image, self.shape[:2])
        
    def test_decode_default(self):
        with open(self.image_filename, "rb") as f:
            image = dito.decode(b=f.read())
        self.assertNumpyShape(image, self.shape)
        self.assertAlmostEqual(np.mean(image), 121.3680261682581)
        
    def test_decode_grayscale(self):
        with open(self.image_filename, "rb") as f:
            image = dito.decode(b=f.read(), color=False)
        self.assertNumpyShape(image, self.shape[:2])
        
    def test_load_and_decode_equal(self):
        image_load = dito.load(filename=self.image_filename)
        with open(self.image_filename, "rb") as f:
            image_decode = dito.decode(b=f.read())
        self.assertNumpyShape(image_load, self.shape)    
        self.assertNumpyShape(image_decode, self.shape)
        self.assertTrue(np.all(image_load == image_decode))


class transforms_Tests(TestCase):
    pass

        
class utils_Tests(TestCase):
    def test_tir_args(self):
        items = (1.24, -1.87)
        self.assertEqual(dito.tir(*items), (1, -2))
        self.assertEqual(dito.tir(items), (1, -2))
        self.assertEqual(dito.tir(list(items)), (1, -2))

        
if __name__ == "__main__":
    unittest.main()
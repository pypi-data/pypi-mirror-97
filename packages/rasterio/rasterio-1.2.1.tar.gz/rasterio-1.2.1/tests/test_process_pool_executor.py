"""Tests for correct behavior of Rasterio's GDALEnv in concurrent programs"""

from concurrent.futures import ProcessPoolExecutor

import rasterio


def get_data(path):
    """Return all raster bands as an ndarray"""
    with rasterio.open(path, sharing=False) as src:
        return src.read()


def test_mp_main_env():
    """Get raster data using ProcessPoolExecutor with main thread Env"""
    with rasterio.Env(), ProcessPoolExecutor() as pool:
        for res in pool.map(get_data, ['tests/data/RGB.byte.tif'] * 10):
            assert res.any()


def test_mp_no_main_env():
    """Get raster data using ProcessPoolExecutor with main thread Env"""
    with ProcessPoolExecutor() as pool:
        for res in pool.map(get_data, ['tests/data/RGB.byte.tif'] * 10):
            assert res.any()

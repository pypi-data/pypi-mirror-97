"""
Extends functionality of np.ndarray for hyperspectral data
"""
import numpy as np
from typing import Union
from scipy.signal import savgol_filter

from hypers.exceptions import DimensionError
from hypers.learning.abundance import abundance
from hypers.learning.decomposition import vca
from hypers.plotting.view import hsiPlot


class hparray(np.ndarray):
    """
    Extend functionality of a numpy array for hyperspectral data

    The usual `numpy.ndarray` attributes and methods are available
    as well as some additional ones that extend functionality.

    Parameters
    ----------
    input_array: Union[list, np.ndarray]
        The array to convert. This should either be a 2d/3d/4d
        numpy array (type `np.ndarray`) or list.

    Attributes
    ----------
    mean_image: np.ndarray
        Provides the mean image by averaging across the spectral
        dimension. e.g. if the shape of the original array is
        (100, 100, 512), then the image dimension shape is (100, 100)
        and the spectral dimension shape is (512,). So the mean
        image will be an array of shape (100, 100).

    mean_spectrum: np.ndarray
        Provides the mean spectrum by averaging across the image
        dimensions. e.g. if the shape of the original array is
        (100, 100, 512), then the image dimension shape is (100, 100)
        and the spectral dimension shape is (512,). So the mean
        spectrum will be an array of shape (512,).
    """
    def __new__(cls, input_array: Union[list, np.ndarray, 'hparray']):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        else:
            if self.ndim > 1:
                self._data_mean()
                self._data_learning()
                self._data_access()

    def __array_wrap__(self, output_array, context=None):
        return np.ndarray.__array_wrap__(self, output_array, context)

    def _data_mean(self):
        """
        Generates `mean_image` and `mean_spectrum` attributes if the
        number of dimensions of the array is greater than 1.
        """
        if self.ndim > 1:
            self.mean_image = np.asarray(np.squeeze(np.mean(self, self.ndim - 1)))
            self.mean_spectrum = np.asarray(np.squeeze(np.mean(self, tuple(range(self.ndim - 1)))))

    def _data_learning(self):
        if self.ndim > 2:
            self.abundance = abundance(self)
            self.unmix = vca(self)

    def _data_access(self):
        self.image = _AccessImage(self)
        self.spectrum = _AccessSpectrum(self)

    def _dimension_error(self):
        raise DimensionError('Number of dimensions must be greater than 2')

    def collapse(self) -> np.ndarray:
        """
        Collapse the array into a 2d array

        Collapses the array into a 2d array, where the first dimension
        is the collapsed image dimensions and the second dimension is
        the spectral dimension.

        Returns
        -------
        np.ndarray
            The collapsed 2d numpy array.

        Examples
        --------
        >>> import numpy as np
        >>> import hypers as hp
        >>> data = np.random.rand(40, 30, 1000)
        >>> x = hp.hparray(data)
        >>> collapsed = x.collapse()
        >>> collapsed.shape
        (1200, 1000)
        """
        if self.ndim > 1:
            return np.asarray(np.reshape(self, (np.prod(self.shape[:-1]), self.shape[-1])))
        else:
            self._dimension_error()

    def smoothen(self, method: str = 'savgol', **kwargs) -> 'hparray':
        """
        Returns smoothened hp.hparray

        Parameters
        ----------
        method: str
            Method to use to smooth the array. Default is 'savgol'.
            + 'savgol': Savitzky-Golay filter.

        **kwargs
            Keyword arguments for the relevant method used.
            + method='savgol'
                kwargs for the `scipy.signal.savgol_filter` implementation

        Returns
        -------
        hp.hparray
            The smoothened array with the same dimensions as the original
            array.
        """
        smooth_array = self.copy()
        for index in np.ndindex(self.shape[:-1]):
            if method == 'savgol':
                smooth_array[index] = savgol_filter(smooth_array[index], **kwargs)
            else:
                raise ValueError
        return smooth_array

    def plot(self, backend: str = 'pyqt'):
        """
        Interactive plotting to interact with hyperspectral data

        Note that at the moment only the 'pyqt' backend has been implemented. This means that
        PyQt is required to be installed and when this method is called, a separate window generated
        by PyQt will pop up. It is still possible to use this in a Jupyter environment, however the
        cell that calls this method will remain frozen until the window is closed.

        Parameters
        ----------
        backend: str
            Backend to use. Default is 'pyqt'.
        """
        if backend == 'pyqt':
            if self.ndim > 2:
                hsiPlot(self)
            else:
                self._dimension_error()

    @property
    def nsamples(self):
        """
        Returns the number of samples (total number of spatial pixels) in the dataset

        Returns
        -------
        int:
            Total number of samples
        """
        if self.ndim > 1:
            return np.prod(self.shape[:-1])
        else:
            self._dimension_error()

    @property
    def nspatial(self):
        """
        Returns the shape of the spatial dimensions

        Returns
        -------
        tuple:
            Tuple of the shape of the spatial dimensions
        """
        if self.ndim > 1:
            return self.shape[:-1]
        else:
            self._dimension_error()

    @property
    def nfeatures(self):
        """
        Returns the number of features (size of the spectral dimension) in the dataset

        Returns
        -------
        int:
            Size of the spectral dimension
        """
        if self.ndim > 1:
            return self.shape[-1]
        else:
            self._dimension_error()


class _AccessImage:
    def __init__(self, X):
        self.data = X

    def __getitem__(self, item):
        if isinstance(item, tuple):
            raise IndexError('Can only pass in 1 index (same as number of spectral dimension)')

        if isinstance(item, int):
            return np.squeeze(self.data[..., item])
        elif isinstance(item, slice):
            return np.squeeze(np.mean(self.data[..., item], self.data.ndim - 1))


class _AccessSpectrum:
    def __init__(self, X):
        self.data = X

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            item = (item,)
        elif not len(item) == self.data.ndim - 1:
            raise IndexError('Must pass in the same number of indicies as number of image dimensions')

        if isinstance(item, tuple) and all(isinstance(nitem, int) for nitem in item):
            return np.squeeze(self.data[item])
        elif isinstance(item, tuple) and all(isinstance(nitem, slice) for nitem in item):
            return np.squeeze(np.mean(self.data[item], tuple(range(self.data.ndim - 1))))

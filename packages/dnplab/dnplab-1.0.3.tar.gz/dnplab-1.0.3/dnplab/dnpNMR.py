import warnings

import numpy as _np
from scipy.optimize import curve_fit

from . import dnpdata, dnpdata_collection
from . import dnpTools

import re
import copy


def return_data(all_data):

    is_workspace = False
    if isinstance(all_data, dnpdata):
        data = all_data.copy()
    elif isinstance(all_data, dict):
        raise ValueError("Type dict is not supported")
    elif isinstance(all_data, dnpdata_collection):
        is_workspace = True
        if all_data.processing_buffer in all_data.keys():
            data = all_data[all_data.processing_buffer]
        else:
            raise ValueError("No data in processing buffer")
    else:
        raise ValueError("Data type not supported")

    return data, is_workspace


def update_parameters(proc_parameters, requiredList, default_parameters):
    """Add default parameter to processing parameters if a processing parameter is missing

    Args:
        proc_parameters (dict): Dictionary of initial processing parameters
        requiredList (list): List of requrired processing parameters
        default_parameters (dict): Dictionary of default processing parameters

    Returns:
        dict: Updated processing parameters dictionary
    """
    updatedProc_parameters = proc_parameters
    for requiredParameter in requiredList:
        if not requiredParameter in updatedProc_parameters:
            updatedProc_parameters[requiredParameter] = default_parameters[
                requiredParameter
            ]

    return updatedProc_parameters


def align(all_data, dim="f2", dim2=None):
    """Alignment of NMR spectra down given dimension or dimensions

    Args:
        all_data (object) : dnpdata object
        dim (str) : dimension to align along
        dim2 (str) : second dimension to align along

    returns:
        dnpdata: Aligned data in container
    """

    data, isDict = return_data(all_data)

    if len(_np.shape(data.values)) > 3:
        raise ValueError("Greater than 3-dimensional data is currently not supported")

    proc_parameters = {"dim": dim, "dim2": dim2}
    originalAxesOrder = data.dims

    if (dim2 is None) or (len(data.shape) == 2):
        if len(data.shape) > 2:
            raise ValueError(
                "data has more than 2 dimensions, 2nd dimension is ambiguous"
            )
        dim2 = None
        data.reorder([dim])
        dimIter = data.dims[-1]

    else:
        data.reorder([dim, dim2])
        dimIter = data.dims[-1]

    if dim2 == None:
        refData = data[dimIter, 0].values.reshape(-1)

        for ix in range(len(data.coords[dimIter])):
            tempData = data[dimIter, ix].values.reshape(-1)

            corrData = _np.correlate(_np.abs(tempData), _np.abs(refData), mode="same")
            shiftIx = _np.argmax(corrData) - (
                len(corrData) / 2
            )  # subtract half length so spectrum is shifted relative to center, not edge
            shiftData = _np.roll(tempData, -1 * int(_np.round(shiftIx, 0)))
            data.values[:, ix] = shiftData
    else:

        for ix1 in range(len(data.coords[-1])):
            refData = data.values[:, 0, ix1]
            for ix2 in range(len(data.coords[dim2])):
                tempData = data.values[:, ix2, ix1]

                corrData = _np.correlate(
                    _np.abs(tempData), _np.abs(refData), mode="same"
                )
                shiftIx = _np.argmax(corrData) - (
                    len(corrData) / 2
                )  # subtract half length so spectrum is shifted relative to center, not edge
                shiftData = _np.roll(tempData, -1 * int(_np.round(shiftIx, 0)))
                data.values[:, ix2, ix1] = shiftData

    data.reorder(originalAxesOrder)

    proc_attr_name = "align"
    data.add_proc_attrs(proc_attr_name, proc_parameters)

    if isDict:
        all_data[all_data.processing_buffer] = data
        return all_data
    else:
        return data


def autophase(
    all_data,
    method="search",
    order="zero",
    pivot=0,
    delta=0,
    phase=0,
    reference_slice=None,
    force_positive=False,
):
    """Automatically phase correct data, or apply manual phase correction

    .. math::

        \mathrm{data}         &= \exp(-1j * \mathrm{phase}) &

        \mathrm{phase(arctan)} &= \mathrm{arctan}(\mathrm{sum}(\mathrm{data.imag}) / \mathrm{sum}(\mathrm{data.real})) &

        \mathrm{phase(search)} &= \mathrm{argmax}(\mathrm{sum}(phased\_real^{2}) / \mathrm{sum}(phased\_imag^{2})) &

        phased\_real          &= \mathrm{data.real} * \exp(-1j * \mathrm{phase}) &

        phased\_imag          &= \mathrm{data.imag} * \exp(-1j * \mathrm{phase}) &

    Args:
        all_data (dnpdata_collection, dnpdata): Data object to autophase

    +-----------------+--------------+---------------+---------------------------------------------------+
    | parameter       | type         | default       | description                                       |
    +=================+==============+===============+===================================================+
    | method          | str          | 'search'      | method of searching for the best phase            |
    +-----------------+--------------+---------------+---------------------------------------------------+
    | order           | str          | 'zero'        | order of phase correction                         |
    +-----------------+--------------+---------------+---------------------------------------------------+
    | pivot           | int          | 0             | pivot point for first order correction            |
    +-----------------+--------------+---------------+---------------------------------------------------+
    | delta           | float        | 0             | total change in phase magnitude for first order   |
    +-----------------+--------------+---------------+---------------------------------------------------+
    | phase           | float        | 0             | manual phase correction                           |
    +-----------------+--------------+---------------+---------------------------------------------------+
    | reference_slice | int, or None | None          | slice of 2D data used to define the phase         |
    +-----------------+--------------+---------------+---------------------------------------------------+
    | force_positive  | boolean      | False         | force the entire spectrum to positive magnitude   |
    +-----------------+--------------+---------------+---------------------------------------------------+

    Returns:
        dnpdata: Autophased data, including attrs "phase_0" for order="zero", and "phase_1" if order="first"

    """

    data, isDict = return_data(all_data)
    shape_data = _np.shape(data.values)

    if method == "manual":
        if order == "zero" and isinstance(phase, float):
            data.attrs["phase_0"] = phase
        elif order == "zero" and not isinstance(phase, float):
            raise ValueError(
                "for a zero order phase correction you must supply a single phase"
            )
        elif order == "first" and isinstance(phase, float):
            data.attrs["phase_0"] = phase
            order = "zero"
            warnings.warn(
                "method=manual and order=first but only a single phase was given, switching to order=zero"
            )
        elif (
            order == "first"
            and isinstance(phase, _np.ndarray)
            and len(phase) == shape_data[0]
        ):
            data.attrs["phase_1"] = phase
        elif (
            order == "first" and isinstance(phase, list) and len(phase) == shape_data[0]
        ):
            data.attrs["phase_1"] = _np.array(phase)
        else:
            raise ValueError(
                "Invalid combination of phase order and phase value(s). Supply float for zero order, array or list for first order"
            )
    else:

        if reference_slice is not None:
            if len(shape_data) == 1:
                reference_slice = None
                temp_data = data.values
                warnings.warn("ignoring reference_slice, this is 1D data")
            else:
                reference_slice -= 1
                temp_data = data.values[:, reference_slice]
        else:
            temp_data = data.values

        if method == "arctan":
            data.attrs["phase_0"] = _np.arctan(
                _np.sum(_np.imag(temp_data.reshape(-1, 1)))
                / _np.sum(_np.real(temp_data.reshape(-1, 1)))
            )
        elif method == "search":
            phases_0 = _np.linspace(-_np.pi / 2, _np.pi / 2, 180).reshape(-1)
            rotated_data = (temp_data.reshape(-1, 1)) * _np.exp(-1j * phases_0)
            real_imag_ratio = (_np.real(rotated_data) ** 2).sum(axis=0) / (
                (_np.imag(rotated_data) ** 2).sum(axis=0)
            )
            data.attrs["phase_0"] = phases_0[_np.argmax(real_imag_ratio)]
        else:
            raise TypeError("Invalid autophase method")

    if order == "zero":
        data.values *= _np.exp(-1j * data.attrs["phase_0"])
    elif order == "first":
        if method == "manual":
            data.attrs["phase_1"] = phase
        else:
            pivot_ratio = pivot / len(data.values)
            data.attrs["phase_1"] = _np.linspace(
                data.attrs["phase_0"] - delta * pivot_ratio,
                data.attrs["phase_0"] + delta * (1 - pivot_ratio),
                len(data.values),
            )
        if len(shape_data) == 2:
            for ix in range(shape_data[1]):
                data.values[:, ix] *= _np.exp(-1j * data.attrs["phase_1"])
        else:
            data.values *= _np.exp(-1j * data.attrs["phase_1"])
    else:
        raise TypeError("Invalid order or order & phase pair")

    if force_positive:
        if len(shape_data) == 2:
            for ix in range(shape_data[1]):
                if _np.sum(_np.real(data.values[:, ix])) < 0:
                    data.values[:, ix] *= -1.0
                else:
                    pass
        elif len(_np.shape(data.values)) == 1:
            if _np.sum(_np.real(data.values)) < 0:
                data.values *= -1.0
        else:
            raise ValueError("only 1D or 2D data are currently supported")

    proc_parameters = {
        "method": method,
        "reference_slice": reference_slice,
        "force_positive": force_positive,
        "order": order,
        "pivot": pivot,
        "delta": delta,
    }
    proc_attr_name = "autophase"
    data.add_proc_attrs(proc_attr_name, proc_parameters)

    if isDict:
        all_data[all_data.processing_buffer] = data
        return all_data
    else:
        return data


def calculate_enhancement(
    all_data,
    off_spectrum=1,
    on_spectra="all",
    integrate_center=0,
    integrate_width="full",
    method="integrate",
    dim="f2",
    indirect_dim=None,
):
    """Calculate enhancement from DNP data

    Args:
        all_data (dnpdata, dict): data container

    +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    | parameter        | type                       | default     | description                                                          |
    +==================+============================+=============+======================================================================+
    | off_spectrum     | int or dnpdata             | 1           | slice of 2D data to be used as p = 0 spectrum, or dnpdata            |
    +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    | on_spectra       | str or dnpdata             | "all"       | "all"  unless dnpdata given                                          |
    +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    | integrate_center | str, int, list, or ndarray | 0           | "max", center of integration window, or index used to find amplitude |
    +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    | integrate_width  | str, int, list, or ndarray | "full"      | "full" or width of integration window                                |
    +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    | method           | str                        | "integrate" | either "integrate" or "ampltiude"                                    |
    +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    | dim              | str                        | "f2"        | dimension to integrate down or search down for max                   |
    +------------------+----------------------------+-------------+----------------------------------------------------------------------+
    | indirect_dim     | str                        | None        | indirect dimension                                                   |
    +------------------+----------------------------+-------------+----------------------------------------------------------------------+

    Returns:
        dnpdata: data object with "enhancement" key added

    """

    orig_data, isDict = return_data(all_data)

    if (
        isinstance(off_spectrum, dnpdata)
        or isinstance(off_spectrum, dnpdata_collection)
    ) and (
        isinstance(on_spectra, dnpdata) or isinstance(on_spectra, dnpdata_collection)
    ):

        data_off, is_ws_off = return_data(off_spectrum)
        data_on, is_ws_on = return_data(on_spectra)
        if not indirect_dim:
            if len(data_on.dims) == 2:
                ind_dim = list(set(data_on.dims) - set([dim]))[0]
            elif len(data_on.dims) == 1:
                ind_dim = data_on.dims[0]
            else:
                raise ValueError(
                    "you must specify the indirect dimension, use argument indirect_dim= "
                )
        else:
            ind_dim = indirect_dim

        if integrate_width == "full":
            int_width_off = "full"
            int_width_on = "full"
        elif (
            isinstance(integrate_width, list)
            or isinstance(integrate_width, _np.ndarray)
        ) and len(integrate_width) == 2:
            int_width_off = integrate_width[0]
            int_width_on = integrate_width[1]
        elif isinstance(integrate_width, int):
            int_width_off = integrate_width
            int_width_on = integrate_width
        else:
            raise ValueError(
                "integrate_width must be an integer, a list/array with len = 2, or 'full'"
            )

        if integrate_center == "max":
            pass
        elif (
            isinstance(integrate_center, list)
            or isinstance(integrate_center, _np.ndarray)
        ) and len(integrate_center) == 2:
            int_center_off = integrate_center[0]
            int_center_on = integrate_center[1]
        elif isinstance(integrate_center, int):
            int_center_off = integrate_center
            int_center_on = integrate_center
        else:
            raise ValueError(
                "integrate_center must be an integer, a list/array with len = 2, or 'max'"
            )

        if method == "integrate":
            off_data1 = dnpTools.integrate(
                data_off,
                dim=dim,
                integrate_center=int_center_off,
                integrate_width=int_width_off,
            )
            off_data = off_data1.values

            on_data1 = dnpTools.integrate(
                data_on,
                dim=dim,
                integrate_center=int_center_on,
                integrate_width=int_width_on,
            )
            on_data = on_data1.values

        elif method == "amplitude":
            on_data = []
            if integrate_center == "max":
                off_data = data_off.values[_np.argmax(abs(data_off.values))]
                if len(data_on.shape) == 1:
                    on_data.append(data_on.values[_np.argmax(abs(data_on.values))])
                else:
                    for indx in range(data_on.shape[-1]):
                        on_data.append(
                            data_on.values[_np.argmax(abs(data_on.values[indx])), indx]
                        )
            else:
                off_data = data_off.values[int_center_off]
                if len(data_on.shape) == 1:
                    on_data.append(data_on.values[int_center_on])
                else:
                    for indx in range(data_on.shape[-1]):
                        on_data.append(data_on.values[int_center_on, indx])

        if data_on.ndim == 2:
            enh_coords_on = data_on.coords[ind_dim]
        else:
            enh_coords_on = _np.array(range(on_data.shape[-1]))

    elif isinstance(off_spectrum, int) and on_spectra == "all":

        if not indirect_dim:
            if len(orig_data.dims) == 2:
                ind_dim = list(set(orig_data.dims) - set([dim]))[0]
            elif len(orig_data.dims) == 1:
                ind_dim = orig_data.dims[0]
            else:
                raise ValueError(
                    "you must specify the indirect dimension, use argument indirect_dim= "
                )
        else:
            ind_dim = indirect_dim

        enh_data = copy.deepcopy(all_data)
        if orig_data.ndim == 1:
            raise ValueError("data is 1D, enhancement will be equal to 1 !!")

        if (
            isinstance(integrate_width, list)
            or isinstance(integrate_width, _np.ndarray)
        ) and len(integrate_width) > 1:
            raise ValueError("supply a single value for integrate_width, or use 'full'")
        elif isinstance(integrate_width, str) and integrate_width != "full":
            raise ValueError("the only allowed integrate_width string is 'full'")

        if (
            isinstance(integrate_center, list)
            or isinstance(integrate_center, _np.ndarray)
        ) and len(integrate_center) > 1:
            raise ValueError("supply a single value for integrate_center, or use 'max'")
        elif isinstance(integrate_center, str) and integrate_center != "max":
            raise ValueError("the only allowed integrate_center string is 'max'")

        if off_spectrum == 0:
            off_spectrum = 1

        if method == "integrate":

            dnpTools.integrate(
                enh_data,
                dim=dim,
                integrate_center=integrate_center,
                integrate_width=integrate_width,
            )
            data, _isDict = return_data(enh_data)
            data_1 = data.values

        elif method == "amplitude":
            data_1 = []
            if integrate_center == "max":
                for indx in range(orig_data.shape[-1]):
                    data_1.append(
                        orig_data.values[_np.argmax(abs(orig_data.values[indx])), indx]
                    )
            else:
                for indx in range(orig_data.shape[-1]):
                    data_1.append(orig_data.values[integrate_center, indx])

        off_data = data_1[off_spectrum - 1]
        if off_spectrum == 1:
            on_data = data_1[1:]
            enh_coords_on = orig_data.coords[ind_dim][1:]
        elif off_spectrum > 1:
            on_data_1 = data_1[: off_spectrum - 1]
            on_coords_1 = orig_data.coords[ind_dim][: off_spectrum - 1]
            on_data_2 = data_1[off_spectrum:]
            on_coords_2 = orig_data.coords[ind_dim][off_spectrum:]
            on_data = _np.concatenate((on_data_1, on_data_2))
            enh_coords_on = _np.concatenate((on_coords_1, on_coords_2))
    else:
        raise TypeError(
            "the given combination of data, off_spectrum, and on_spectra is not valid"
        )

    enh = _np.real(_np.array(on_data) / _np.array(off_data))
    enhancementData = dnpdata(enh, [enh_coords_on], [ind_dim])

    if isDict:
        all_data["enhancement"] = enhancementData
        return all_data
    else:
        return enhancementData


def fourier_transform(
    all_data, dim="t2", zero_fill_factor=2, shift=True, convert_to_ppm=True
):
    """Perform Fourier Transform down dim dimension given in proc_parameters

    .. Note::
        Assumes dt = t[1] - t[0]

    Args:
        all_data (dnpdata, dict): Data container

    +------------------+------+---------+--------------------------------------------------+
    | parameter        | type | default | description                                      |
    +==================+======+=========+==================================================+
    | dim              | str  | 't2'    | dimension to Fourier transform                   |
    +------------------+------+---------+--------------------------------------------------+
    | zero_fill_factor | int  | 2       | factor to increase dim with zeros                |
    +------------------+------+---------+--------------------------------------------------+
    | shift            | bool | True    | Perform fftshift to set zero frequency to center |
    +------------------+------+---------+--------------------------------------------------+
    | convert_to_ppm   | bool | True    | Convert dim from Hz to ppm                       |
    +------------------+------+---------+--------------------------------------------------+

    Returns:
        dnpdata: data object after FT
    """

    # Determine if data is dictionary or dnpdata object
    data, isDict = return_data(all_data)

    # handle zero_fill_factor
    zero_fill_factor = int(zero_fill_factor)
    if zero_fill_factor <= 0:
        zero_fill_factor = 1

    proc_parameters = {
        "dim": dim,
        "zero_fill_factor": zero_fill_factor,
        "shift": shift,
        "convert_to_ppm": convert_to_ppm,
    }

    index = data.dims.index(dim)
    dt = data.coords[dim][1] - data.coords[dim][0]
    n_pts = zero_fill_factor * len(data.coords[dim])
    f = (1.0 / (n_pts * dt)) * _np.r_[0:n_pts]
    if shift == True:
        f -= 1.0 / (2 * dt)

    if convert_to_ppm:
        nmr_frequency = data.attrs["nmr_frequency"]
        f /= -1 * nmr_frequency / 1.0e6

    data.values = _np.fft.fft(data.values, n=n_pts, axis=index)
    if shift:
        data.values = _np.fft.fftshift(data.values, axes=index)
    data.coords[dim] = f

    if re.fullmatch("t[0-9]*", dim) is not None:
        new_dim = dim.replace("t", "f")
        data.rename(dim, new_dim)

    proc_attr_name = "fourier_transform"
    data.add_proc_attrs(proc_attr_name, proc_parameters)

    if isDict:
        all_data[all_data.processing_buffer] = data
        return all_data
    else:
        return data


def inverse_fourier_transform(
    all_data, dim="f2", zero_fill_factor=1, shift=True, convert_from_ppm=True
):
    """Perform Fourier Transform down dim dimension given in proc_parameters

    .. Note::
        Assumes dt = t[1] - t[0]

    Args:
        all_data (dnpdata, dict): Data container

    +------------------+------+---------+--------------------------------------------------+
    | parameter        | type | default | description                                      |
    +==================+======+=========+==================================================+
    | dim              | str  | 'f2'    | dimension to Fourier transform                   |
    +------------------+------+---------+--------------------------------------------------+
    | zero_fill_factor | int  | 2       | factor to increase dim with zeros                |
    +------------------+------+---------+--------------------------------------------------+
    | shift            | bool | True    | Perform fftshift to set zero frequency to center |
    +------------------+------+---------+--------------------------------------------------+
    | convert_to_ppm   | bool | True    | Convert dim from Hz to ppm                       |
    +------------------+------+---------+--------------------------------------------------+

    Returns:
        dnpdata: data object after inverse FT
    """

    # Determine if data is dictionary or dnpdata object
    data, isDict = return_data(all_data)

    # handle zero_fill_factor
    zero_fill_factor = int(zero_fill_factor)
    if zero_fill_factor <= 0:
        zero_fill_factor = 1

    proc_parameters = {
        "dim": dim,
        "zero_fill_factor": zero_fill_factor,
        "shift": shift,
        "convert_from_ppm": convert_from_ppm,
    }

    index = data.dims.index(dim)
    df = data.coords[dim][1] - data.coords[dim][0]

    if convert_from_ppm:
        nmr_frequency = data.attrs["nmr_frequency"]
        df /= -1 / (nmr_frequency / 1.0e6)

    n_pts = zero_fill_factor * len(data.coords[dim])
    t = (1.0 / (n_pts * df)) * _np.r_[0:n_pts]

    if shift:
        data.values = _np.fft.fftshift(data.values, axes=index)

    data.values = _np.fft.ifft(data.values, n=n_pts, axis=index)
    data.coords[dim] = t

    if re.fullmatch("f[0-9]*", dim) is not None:
        new_dim = dim.replace("f", "t")
        data.rename(dim, new_dim)

    proc_attr_name = "inverse_fourier_transform"
    data.add_proc_attrs(proc_attr_name, proc_parameters)

    if isDict:
        all_data[all_data.processing_buffer] = data
        return all_data
    else:
        return data


def left_shift(all_data, dim="t2", shift_points=0):
    """Remove points from the left of data

    Args:
        all_data (dnpdata, dict): Data container for data

    +---------------+------+---------+--------------------------------------------------+
    | parameter     | type | default | description                                      |
    +===============+======+=========+==================================================+
    | dim           | str  | "t2"    | dimension to shift                               |
    +---------------+------+---------+--------------------------------------------------+
    | shift_points  | int  | 0       | Number of points to remove from left of data     |
    +---------------+------+---------+--------------------------------------------------+

    Returns:
        dnpdata: data object with left-shifted data
    """

    data, isDict = return_data(all_data)

    shifted_data = data[dim, shift_points:]

    proc_attr_name = "left_shift"
    proc_parameters = {
        "dim": dim,
        "points": shift_points,
    }
    shifted_data.add_proc_attrs(proc_attr_name, proc_parameters)

    if isDict:
        all_data[all_data.processing_buffer] = shifted_data
        return all_data
    else:
        return shifted_data


def remove_offset(all_data, dim="t2", offset_points=10):
    """Remove DC offset from FID by averaging the last few data points and subtracting the average

    Args:
        all_data (dnpdata, dict): Data container for data

    +---------------+------+---------+----------------------------------------------------------+
    | parameter     | type | default | description                                              |
    +===============+======+=========+==========================================================+
    | dim           | str  | 't2'    | Dimension to calculate DC offset                         |
    +---------------+------+---------+----------------------------------------------------------+
    | offset_points | int  | 10      | Number of points at end of data to average for DC offset |
    +---------------+------+---------+----------------------------------------------------------+

    Returns:
        dnpdata: data object with offset removed
    """

    # Determine if data is dictionary or dnpdata object
    data, isDict = return_data(all_data)

    proc_parameters = {
        "dim": dim,
        "offset_points": offset_points,
    }

    dim = proc_parameters["dim"]
    offset_points = int(proc_parameters["offset_points"])

    offsetData = data[dim, -1 * offset_points :].values
    offsetData = offsetData.reshape(-1)
    offset = _np.mean(offsetData)

    data -= offset

    proc_attr_name = "remove_offset"
    data.add_proc_attrs(proc_attr_name, proc_parameters)

    if isDict:
        all_data[all_data.processing_buffer] = data
        return all_data
    else:
        return data


def window(
    all_data,
    dim="t2",
    type="exponential",
    linewidth=1,
    gaussian_max=0,
    inverse=False,
):
    """Apply Apodization to data down given dimension

    .. math::

        \mathrm{exponential}    &=  \exp(-2t * \mathrm{linewidth}) &

        \mathrm{gaussian}       &=  \exp((\mathrm{linewidth[0]} * t) - (\mathrm{linewidth[1]} * t^{2})) &

        \mathrm{hamming}        &=  0.53836 + 0.46164\cos(\pi * n/(N-1)) &

        \mathrm{han}            &=  0.5 + 0.5\cos(\pi * n/(N-1)) &

        \mathrm{sin2}           &=  \cos((-0.5\pi * n/(N - 1)) + \pi)^{2} &

        \mathrm{lorentz\_gauss} &=  \exp(L -  G^{2}) &

               L(t)    &=  \pi * \mathrm{linewidth[0]} * t &

               G(t)    &=  0.6\pi * \mathrm{linewidth[1]} * (\mathrm{gaussian\_max} * (N - 1) - t) &

        \mathrm{traf}           &=  (f1 * (f1 + f2)) / (f1^{2} + f2^{2}) &

               f1(t)   &=  \exp(-t * \pi * \mathrm{linewidth[0]}) &

               f2(t)   &=  \exp((t - T) * \pi * \mathrm{linewidth[1]}) &


    Args:
        all_data (dnpdata, dict): data container

    +-----------------+-------------------------+---------------+---------------------------------------------------+
    | parameter       | type                    | default       | description                                       |
    +=================+=========================+===============+===================================================+
    | dim             | str                     | 't2'          | Dimension to apply exponential apodization        |
    +-----------------+-------------------------+---------------+---------------------------------------------------+
    | type            | str                     | 'exponential' | type of apodization                               |
    +-----------------+-------------------------+---------------+---------------------------------------------------+
    | linewidth       | float, list, or ndarray | 1             | linewidths  in Hz                                 |
    +-----------------+-------------------------+---------------+---------------------------------------------------+
    | gaussian_max    | float                   | 0             | Location of gaussian component maximum            |
    +-----------------+-------------------------+---------------+---------------------------------------------------+
    | inverse         | boolean                 | False         | invert the window function                        |
    +-----------------+-------------------------+---------------+---------------------------------------------------+

    Returns:
        dnpdata: data object with window function applied, including attr "window"
    """
    data, isDict = return_data(all_data)
    dim_size = data.coords[dim].shape[-1]
    shape_data = _np.shape(data.values)

    if (isinstance(linewidth, _np.ndarray) or isinstance(linewidth, list)) and len(
        linewidth
    ) == 2:
        a = linewidth[0]
        b = linewidth[1]
    elif isinstance(linewidth, int) or isinstance(linewidth, float):
        a = linewidth
        b = linewidth
    else:
        raise ValueError("linewidth must be int/float, or list/ndarray with len==2")

    if type == "exponential":
        apwin = _np.exp(-2 * data.coords[dim] * linewidth)
    elif type == "gaussian":
        apwin = _np.exp((a * data.coords[dim]) - (b * data.coords[dim] ** 2))
    elif type == "hamming":
        apwin = 0.53836 + 0.46164 * _np.cos(
            1.0 * _np.pi * _np.arange(dim_size) / (dim_size - 1)
        )
    elif type == "hann":
        apwin = 0.5 + 0.5 * _np.cos(
            1.0 * _np.pi * _np.arange(dim_size) / (dim_size - 1)
        )
    elif type == "lorentz_gauss":
        expo = _np.pi * data.coords[dim] * a
        gaus = 0.6 * _np.pi * b * (gaussian_max * (dim_size - 1) - data.coords[dim])
        apwin = _np.exp(expo - gaus ** 2).reshape(dim_size)
    elif type == "sin2":
        apwin = (
            _np.cos((-0.5 * _np.pi * _np.arange(dim_size) / (dim_size - 1)) + _np.pi)
            ** 2
        )
    elif type == "traf":
        E_t = _np.exp(-1 * data.coords[dim] * _np.pi * a)
        e_t = _np.exp((data.coords[dim] - max(data.coords[dim])) * _np.pi * b)
        apwin = (E_t * (E_t + e_t)) / ((E_t ** 2) + (e_t ** 2))
    else:
        raise ValueError("Invalid window type")

    apwin.reshape(dim_size)

    if inverse:
        apwin = 1 / apwin

    if len(shape_data) == 2:
        for ix in range(shape_data[1]):
            data.values[:, ix] *= apwin
    else:
        data.values *= apwin

    proc_parameters = {
        "type": type,
        "linewidth": linewidth,
        "dim": dim,
        "gaussian_max": gaussian_max,
        "inverse": inverse,
    }
    proc_attr_name = "window"
    data.add_proc_attrs(proc_attr_name, proc_parameters)
    data.attrs["window"] = apwin

    if isDict:
        all_data[all_data.processing_buffer] = data
        return all_data
    else:
        return data


def phasecycle(all_data, dim, receiver_phase):
    """Phase cycle

    Args:
        all_data (dnpdata_collection, dnpdata): data to process
        dim (str): dimension to perform phase cycle
        receiver_phase (numpy.array, list): Receiver Phase 0 (x), 1 (y), 2 (-x), 3 (-y)

    Returns:
        dnpdata: data object after phase cycle applied
    """

    data, isDict = return_data(all_data)

    data = data.copy()

    if dim not in data.dims:
        raise ValueError("dim not in dims")

    coord = data.coords[dim]
    receiver_phase = _np.array(receiver_phase).ravel()

    proc_parameters = {"dim": dim, "receiver_phase": receiver_phase}

    receiver_phase = _np.tile(receiver_phase, int(coord.size / receiver_phase.size))

    index = data.dims.index(dim)

    reshape_size = [1 for k in data.dims]
    reshape_size[index] = len(data.coords[dim])

    data *= _np.exp(1j * (_np.pi / 2.0) * receiver_phase.reshape(reshape_size))

    proc_attr_name = "phasecycle"
    data.add_proc_attrs(proc_attr_name, proc_parameters)

    return data

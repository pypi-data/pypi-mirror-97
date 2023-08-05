import numpy as np
from scipy.stats import t
# from scipy.stats.stats import _ttest_finish
from ..combinations import n_conditions_to_combinations, trials_to_n_conditions
from ..array import samples_in_arr1_are_in_arr2
from .. import maths as cc_maths


def select_sum(exclude_nan=True):
    if exclude_nan:
        sum = np.nansum
    else:
        sum = np.sum
    return sum


def counter_excluding_nan_keeping_dims(scores, axis_samples):
    n_samples = np.sum(cc_maths.is_not_nan(scores), axis=axis_samples, keepdims=True)
    return n_samples


def counter_excluding_nan_not_keeping_dims(scores, axis_samples):
    n_samples = np.sum(cc_maths.is_not_nan(scores), axis=axis_samples, keepdims=False)
    return n_samples


# def counter_including_nan_keeping_dims(scores, axis_samples):
#     n_samples = np.empty(scores.shape, dtype='i')
#     n_samples[:] = scores.shape[axis_samples]
#     return n_samples
#
#
# def counter_including_nan_not_keeping_dims(scores, axis_samples):
#     n_samples = scores.shape[axis_samples]
#     return n_samples
def counter_including_nan(scores, axis_samples):
    n_samples = scores.shape[axis_samples]
    return n_samples


def select_counter(exclude_nan=True, keepdims=False):
    if exclude_nan:
        if keepdims:
            counter = counter_excluding_nan_keeping_dims
        else:
            counter = counter_excluding_nan_not_keeping_dims
    else:
        counter = counter_including_nan
        # if keepdims:
        #     counter = counter_including_nan_keeping_dims
        # else:
        #     counter = counter_including_nan_not_keeping_dims
    return counter


def scores_to_diff_of_scores(scores, axis, delta=1, stride=1, keepdims=False):
    # this function will go to cc.array in future versions

    shape_scores = np.asarray(scores.shape)
    n_axes_scores = shape_scores.size
    if axis < 0:
        axis += n_axes_scores

    n_conditions = shape_scores[axis]
    index_0 = np.empty(n_axes_scores, dtype=object)
    index_0[:] = slice(None)
    index_1 = np.copy(index_0)

    index_diff = np.copy(index_0)
    index_diff[axis] = 0

    n_differences = int((n_conditions - abs(delta)) // abs(stride))
    shape_diff_of_scores = shape_scores
    shape_diff_of_scores[axis] = n_differences
    diff_of_scores = np.empty(shape_diff_of_scores, dtype=scores.dtype)

    if delta > 0 and stride > 0:
        for i in range(0, n_conditions - delta, stride):
            index_0[axis] = i
            index_1[axis] = i + delta
            diff_of_scores[tuple(index_diff)] = scores[tuple(index_0)] - scores[tuple(index_1)]
            index_diff[axis] += 1
    elif delta < 0 and stride > 0:
        for i in range(abs(delta), n_conditions, stride):
            index_0[axis] = i
            index_1[axis] = i + delta
            diff_of_scores[tuple(index_diff)] = scores[tuple(index_0)] - scores[tuple(index_1)]
            index_diff[axis] += 1
    elif delta > 0 and stride < 0:
        for i in range(n_conditions - delta - 1, -1, stride):
            index_0[axis] = i
            index_1[axis] = i + delta
            diff_of_scores[tuple(index_diff)] = scores[tuple(index_0)] - scores[tuple(index_1)]
            index_diff[axis] += 1
    elif delta < 0 and stride < 0:
        for i in range(n_conditions - 1, abs(delta) -1, stride):
            index_0[axis] = i
            index_1[axis] = i + delta
            diff_of_scores[tuple(index_diff)] = scores[tuple(index_0)] - scores[tuple(index_1)]
            index_diff[axis] += 1
    elif delta == 0:
        raise ValueError('delta has to be an intiger smaller or greater than 0. It cannot be 0')
    elif stride == 0:
        raise ValueError('stride has to be an intiger smaller or greater than 0. It cannot be 0')
    else:
        raise ValueError('Both delta and stride have to be an intiger smaller or greater than 0.')

    if not keepdims and (diff_of_scores.shape[axis] == 1):
        diff_of_scores = np.squeeze(diff_of_scores, axis=axis)

    return diff_of_scores


def scores_to_n_samples(scores, axis_samples, keepdims=False, exclude_nan=True):

    counter = select_counter(exclude_nan=exclude_nan, keepdims=keepdims)

    if scores.dtype == object:

        shape_object_scores = np.asarray(scores.shape)
        n_axes_object_scores = shape_object_scores.size
        axes_object_scores = np.arange(n_axes_object_scores)

        indexes_object = np.empty(n_axes_object_scores, dtype=object)
        indexes_object[:] = 0
        shape_scores = np.asarray(scores[tuple(indexes_object)].shape)
        n_axes_scores = shape_scores.size
        if axis_samples < 0:
            axis_samples += n_axes_scores

        if keepdims:
            shape_scores_tmp = shape_scores
            shape_scores_tmp[axis_samples] = 1
        else:
            shape_scores_tmp = shape_scores[np.arange(n_axes_scores) != axis_samples]

        shape_n_samples = np.append(shape_object_scores, shape_scores_tmp)
        n_samples = np.empty(shape_n_samples, dtype=int)

        n_axes_n_samples = shape_n_samples.size
        indexes_n_samples = np.empty(n_axes_n_samples, dtype=object)
        indexes_n_samples[:] = slice(None)

        indexes_object = n_conditions_to_combinations(shape_object_scores)
        for indexes_object_i in indexes_object:

            indexes_n_samples[axes_object_scores] = indexes_object_i
            indexes_n_samples_tuple = tuple(indexes_n_samples)
            indexes_object_i_tuple = tuple(indexes_object_i)

            n_samples[indexes_n_samples_tuple] = counter(scores[indexes_object_i_tuple], axis_samples=axis_samples)

            # n_samples[indexes_n_samples_tuple] = np.sum(
            #     cc_maths.is_not_nan(scores[indexes_object_i_tuple]), axis=axis_samples, keepdims=keepdims)

    else:
        shape_scores = np.asarray(scores.shape)
        n_axes_scores = shape_scores.size
        if axis_samples < 0:
            axis_samples += n_axes_scores

        n_samples = counter(scores, axis_samples=axis_samples)

    return n_samples


def samples_to_frequencies(data, axis_samples, axis_variables_table):

    if axis_samples < axis_variables_table:
        axis_comb = 0
    elif axis_samples > axis_variables_table:
        axis_comb = 1
    else:
        raise ValueError('The following assumption is not met:\n'
                         '\taxis_samples \u003D axis_variables_table')

    shape_data = np.asarray(data.shape, dtype=int)
    n_axes_data = shape_data.size
    axes_data = np.arange(n_axes_data)
    axes_others_and_samples = axes_data[axes_data != axis_variables_table]
    axes_other_data = axes_others_and_samples[axes_others_and_samples != axis_samples]
    n_axes_other_data = axes_other_data.size
    n_variables_table = shape_data[axis_variables_table]

    indexes_data = np.empty(n_axes_data, dtype=object)
    indexes_data[:] = slice(None)
    indexes_data[axes_other_data] = 0

    n_conditions = trials_to_n_conditions(data[tuple(indexes_data)], axis_combinations=axis_comb)

    n_axes_frequencies = n_axes_other_data + n_variables_table
    shape_frequencies = np.empty(n_axes_frequencies, dtype=int)
    shape_frequencies[slice(n_axes_other_data)] = shape_data[axes_other_data]
    shape_frequencies[slice(n_axes_other_data, n_axes_frequencies)] = n_conditions
    frequencies = np.empty(shape_frequencies, dtype=int)
    frequencies[:] = 0
    indexes_frequencies = np.empty(n_axes_data, dtype=object)

    combinations_others_and_samples = n_conditions_to_combinations(shape_data[axes_others_and_samples])
    # combinations_others = combinations_others_and_samples[slice(None), axes_others_and_samples != axis_samples]
    indexes_comb_c = axes_others_and_samples != axis_samples
    for comb_c in combinations_others_and_samples:

        indexes_data[axes_others_and_samples] = comb_c

        indexes_frequencies[slice(n_axes_other_data)] = comb_c[indexes_comb_c]
        indexes_frequencies[slice(n_axes_other_data, n_axes_frequencies)] = data[tuple(indexes_data)]

        frequencies[tuple(indexes_frequencies)] += 1

    return frequencies


def samples_to_probabilities(data, axis_samples, axis_variables_table):

    if axis_samples == axis_variables_table:
        raise ValueError('The following assumption is not met:\n'
                         '\taxis_samples \u2260 axis_variables_table')
    n_samples = data.shape[axis_samples]
    frequencies = samples_to_frequencies(data, axis_samples, axis_variables_table)
    probabilities = frequencies / n_samples

    return probabilities


def samples_to_percentages(data, axis_samples, axis_variables_table):
    if axis_samples == axis_variables_table:
        raise ValueError('The following assumption is not met:\n'
                         '\taxis_samples \u2260 axis_variables_table')
    n_samples = data.shape[axis_samples]
    frequencies = samples_to_frequencies(data, axis_samples, axis_variables_table)
    percentages = frequencies / n_samples * 100

    return percentages


def scores_to_df_of_variance_and_paired_t(scores, axis_samples, keepdims=False, exclude_nan=True):

    n_samples = scores_to_n_samples(scores, axis_samples=axis_samples, keepdims=keepdims, exclude_nan=exclude_nan)
    df = n_samples - 1

    return df


def scores_to_means(scores, axes, keepdims=False, exclude_nan=True):

    axes_means = axes

    sum = select_sum(exclude_nan=exclude_nan)

    if scores.dtype == object:

        shape_object_scores = np.asarray(scores.shape)
        n_axes_object_scores = shape_object_scores.size
        axes_object_scores = np.arange(n_axes_object_scores)

        indexes_object = np.empty(n_axes_object_scores, dtype=object)
        indexes_object[:] = 0
        shape_scores = np.asarray(scores[tuple(indexes_object)].shape, dtype=int)
        n_axes_scores = shape_scores.size
        try:
            len(axes_means)
            # n_axes_means = len(axes_means)
            axes_means = np.asarray(axes_means, dtype=int)
            axes_means[axes_means < 0] += n_axes_scores
            # check point 1
            if np.sum(axes_means[0] == axes_means) > 1:
                raise ValueError('axes cannot contain repeated values')
            axes_means = np.sort(axes_means)[::-1]
        except TypeError:
            if axes_means < 0:
                axes_means += n_axes_scores
            axes_means = np.asarray([axes_means], dtype=int)
            # n_axes_means = 1

        if keepdims:
            shape_scores_tmp = shape_scores
            shape_scores_tmp[axes_means] = 1
        else:
            axes_scores = np.arange(n_axes_scores)
            shape_scores_tmp = shape_scores[np.logical_not(samples_in_arr1_are_in_arr2(
                axes_scores, axes_means))]

        shape_means = np.append(shape_object_scores, shape_scores_tmp)
        means = np.empty(shape_means, dtype=float)

        n_axes_means = shape_means.size
        indexes_means = np.empty(n_axes_means, dtype=object)
        indexes_means[:] = slice(None)

        indexes_object = n_conditions_to_combinations(shape_object_scores)
        for indexes_object_i in indexes_object:

            indexes_means[axes_object_scores] = indexes_object_i
            indexes_means_tuple_i = tuple(indexes_means)
            indexes_object_tuple_i = tuple(indexes_object_i)

            scores_tmp_i = scores[indexes_object_tuple_i]
            for a in axes_means:
                n_samples = scores_to_n_samples(
                    scores_tmp_i, axis_samples=a, keepdims=keepdims, exclude_nan=exclude_nan)
                # n_samples = np.sum(cc_maths.is_not_nan(scores_tmp_i), axis=a, keepdims=keepdims)

                sum_of_scores = sum(scores_tmp_i, axis=a, keepdims=keepdims)
                scores_tmp_i = sum_of_scores / n_samples

            means[indexes_means_tuple_i] = scores_tmp_i

    else:

        shape_scores = np.asarray(scores.shape, dtype=int)
        n_axes_scores = shape_scores.size

        try:
            len(axes_means)
            # n_axes_means = len(axes_means)
            axes_means = np.asarray(axes_means, dtype=int)
            axes_means[axes_means < 0] += n_axes_scores
            # check point 1
            if np.sum(axes_means[0] == axes_means) > 1:
                raise ValueError('axes cannot contain repeated values')
            axes_means = np.sort(axes_means)[::-1]
        except TypeError:
            if axes_means < 0:
                axes_means += n_axes_scores
            axes_means = np.asarray([axes_means], dtype=int)
            # n_axes_means = 1
        scores_tmp = scores
        for a in axes_means:
            n_samples = scores_to_n_samples(
                scores_tmp, axis_samples=a, keepdims=keepdims, exclude_nan=exclude_nan)
            # n_samples = np.sum(cc_maths.is_not_nan(scores_tmp), axis=a, keepdims=keepdims)
            sum_of_scores = sum(scores_tmp, axis=a, keepdims=keepdims)
            scores_tmp = sum_of_scores / n_samples
        means = scores_tmp

    return means


def scores_to_variances(scores, axis_samples, keepdims=False, exclude_nan=True):

    sum = select_sum(exclude_nan=exclude_nan)

    if scores.dtype == object:

        shape_object_scores = np.asarray(scores.shape)
        n_axes_object_scores = shape_object_scores.size
        axes_object_scores = np.arange(n_axes_object_scores)

        indexes_object = np.empty(n_axes_object_scores, dtype=object)
        indexes_object[:] = 0
        shape_scores = np.asarray(scores[tuple(indexes_object)].shape)
        n_axes_scores = shape_scores.size
        if axis_samples < 0:
            axis_samples += n_axes_scores

        if keepdims:
            shape_scores_tmp = shape_scores
            shape_scores_tmp[axis_samples] = 1
        else:
            shape_scores_tmp = shape_scores[np.arange(n_axes_scores) != axis_samples]

        shape_variances = np.append(shape_object_scores, shape_scores_tmp)
        variances = np.empty(shape_variances, dtype=float)

        n_axes_variances = shape_variances.size
        indexes_variances = np.empty(n_axes_variances, dtype=object)
        indexes_variances[:] = slice(None)

        indexes_object = n_conditions_to_combinations(shape_object_scores)
        for indexes_object_i in indexes_object:

            indexes_variances[axes_object_scores] = indexes_object_i
            indexes_variances_tuple = tuple(indexes_variances)
            indexes_object_i_tuple = tuple(indexes_object_i)

            n_samples = scores_to_n_samples(
                scores[indexes_object_i_tuple], axis_samples=axis_samples, keepdims=True, exclude_nan=exclude_nan)
            # n_samples = np.sum(cc_maths.is_not_nan(
            #     scores[indexes_object_i_tuple]), axis=axis_samples, keepdims=True)

            sum_of_scores = sum(scores[indexes_object_i_tuple], axis=axis_samples, keepdims=True)
            # sum_of_scores = np.nansum(scores[indexes_object_i_tuple], axis=axis_samples, keepdims=keepdims)

            means = sum_of_scores / n_samples
            # means = scores_to_means(
            #     scores[indexes_object_i_tuple], axes=axis_samples, keepdims=keepdims, exclude_nan=exclude_nan)

            sum_of_squared_distances = sum(
                (scores[indexes_object_i_tuple] - means) ** 2, axis=axis_samples, keepdims=keepdims)

            if not keepdims:
                try:
                    n_samples[axis_samples]
                    n_samples = np.squeeze(n_samples, axis=axis_samples)
                except TypeError:
                    pass

            df = n_samples - 1

            variances[indexes_variances_tuple] = sum_of_squared_distances / df

    else:

        shape_scores = np.asarray(scores.shape)
        n_axes_scores = shape_scores.size
        if axis_samples < 0:
            axis_samples += n_axes_scores

        n_samples = scores_to_n_samples(scores, axis_samples=axis_samples, keepdims=True, exclude_nan=exclude_nan)
        # n_samples = np.sum(cc_maths.is_not_nan(scores), axis=axis_samples, keepdims=True)
        sum_of_scores = sum(scores, axis=axis_samples, keepdims=True)
        means = sum_of_scores / n_samples
        # means = np.nansum(scores, axis=axis_samples, keepdims=True) / n_samples
        sum_of_squared_distances = sum((scores - means) ** 2, axis=axis_samples, keepdims=keepdims)
        # sum_of_squared_distances = np.nansum((scores - means) ** 2, axis=axis_samples, keepdims=keepdims)
        if not keepdims:
            try:
                n_samples[axis_samples]
                n_samples = np.squeeze(n_samples, axis=axis_samples)
            except TypeError:
                pass

        df = n_samples - 1
        variances = sum_of_squared_distances / df

    return variances


def scores_to_standard_deviations(scores, axis_samples, keepdims=False, exclude_nan=True):

    variances = scores_to_variances(scores, axis_samples, keepdims=keepdims, exclude_nan=exclude_nan)
    standard_deviations = np.sqrt(variances)

    return standard_deviations


def scores_to_standard_errors(scores, axis_samples, keepdims=False, exclude_nan=True):

    # shape_scores = np.asarray(scores.shape)
    # n_axes_scores = shape_scores.size
    # if axis_samples < 0:
    #     axis_samples += n_axes_scores

    n_samples = scores_to_n_samples(scores, axis_samples, keepdims=keepdims, exclude_nan=exclude_nan)
    variances = scores_to_variances(scores, axis_samples, keepdims=keepdims, exclude_nan=exclude_nan)
    std_error = np.sqrt(variances / n_samples)

    return std_error


def scores_to_confidence_intervals(
        scores, axis_samples, alpha=0.05, tails='2', keepdims=False, exclude_nan=True):

    confidence = 1 - alpha

    # shape_scores = np.asarray(scores.shape)
    # n_axes_scores = shape_scores.size
    # if axis_samples < 0:
    #     axis_samples += n_axes_scores

    std_err = scores_to_standard_errors(scores, axis_samples, keepdims=keepdims, exclude_nan=exclude_nan)
    df = scores_to_df_of_variance_and_paired_t(scores, axis_samples, keepdims=keepdims, exclude_nan=exclude_nan)

    shape_df = np.asarray(df.shape)
    indexes_df = n_conditions_to_combinations(shape_df)
    t_critical = np.empty(shape_df, dtype=float)

    for indexes_df_i in indexes_df:

        indexes_df_i_tuple = tuple(indexes_df_i)

        if tails == '2':
            t_critical[indexes_df_i_tuple] = t.ppf((1 + confidence) / 2., df[indexes_df_i_tuple])

        elif tails == '1l':
            t_critical[indexes_df_i_tuple] = -t.ppf(confidence, df[indexes_df_i_tuple])
        elif tails == '1r':
            t_critical[indexes_df_i_tuple] = t.ppf(confidence, df[indexes_df_i_tuple])

    h = std_err * t_critical

    return h


def scores_to_local_mean(data, axis, n_neighbours, exclude_nan=True):

    n_axes = len(data.shape)
    if axis < 0:
        axis += n_axes

    I = data.shape[axis]

    shape_means_local = list(data.shape)
    shape_means_local[axis] = I - n_neighbours + 1

    means_local = np.empty(shape_means_local, dtype='f')

    indexes_means_local = np.empty(n_axes, dtype='O')
    indexes_data = np.empty(n_axes, dtype='O')

    for a in range(n_axes):
        if a != axis:
            indexes_means_local[a] = slice(0, means_local.shape[a], 1)
            indexes_data[a] = slice(0, data.shape[a], 1)

    for i in range(0, I - n_neighbours + 1, 1):
        indexes_means_local[axis] = i
        indexes_data[axis] = slice(i, i + n_neighbours, 1)
        means_local[tuple(indexes_means_local)] = scores_to_means(
            data[tuple(indexes_data)], axes=axis, keepdims=False, exclude_nan=exclude_nan)

    return means_local


def scores_to_value_frequencies(data, axis, value):

    if cc_maths.is_nan(value):
        arr_logical = cc_maths.is_nan(data)
    else:
        arr_logical = data == value

    arr = np.sum(arr_logical, axis=axis, initial=0)
    return arr


def scores_to_local_value_frequencies(data, axis, n_neighbours, value):
    n_axes = len(data.shape)
    if axis < 0:
        axis += n_axes

    I = data.shape[axis]

    shape_local_frequencies = list(data.shape)
    shape_local_frequencies[axis] = I - n_neighbours + 1

    local_frequencies = np.empty(shape_local_frequencies, dtype='i')

    indexes_local_frequencies = np.empty(n_axes, dtype='O')
    indexes_data = np.empty(n_axes, dtype='O')

    for a in range(n_axes):
        if a != axis:
            indexes_local_frequencies[a] = slice(0, local_frequencies.shape[a], 1)
            indexes_data[a] = slice(0, data.shape[a], 1)

    for i in range(0, I - n_neighbours + 1, 1):
        indexes_local_frequencies[axis] = i
        indexes_data[axis] = slice(i, i + n_neighbours, 1)

        local_frequencies[tuple(indexes_local_frequencies)] = scores_to_value_frequencies(
            data[tuple(indexes_data)], axis, value)

    return local_frequencies

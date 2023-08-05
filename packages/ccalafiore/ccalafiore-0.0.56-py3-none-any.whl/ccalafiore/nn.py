# websites:
# https://pytorch.org/docs/stable/torchvision/transforms.html
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py
# https://pytorch.org/hub/pytorch_vision_resnet/
# https://discuss.pytorch.org/t/normalize-each-input-image-in-a-batch-independently-and-inverse-normalize-the-output/23739
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

import torch
import torchvision
import PIL
import math
import numpy as np
import os
import copy
from . import array as cc_array
from . import txt as cc_txt
from . import clock as cc_clock
from . import directory as cc_directory
from . import maths as cc_maths
from . import combinations as cc_combinations
from .strings import format_float_to_str as cc_strings_format_float_to_str


class Time:
    # TODO make range for each directory level
    def __init__(self, range_time, level, range_shifts=None, n_shifts=None):

        if not isinstance(range_time, cc_array.IntRange):
            self.range_time = cc_array.IntRange(range_time)
        else:
            self.range_time = range_time

        self.level = level

        if range_shifts is None:
            self.range_shifts = range_shifts
            self.random_shifts = False
        else:
            self.range_shifts = cc_array.IntRange(range_shifts)
            if self.range_shifts.len < 1:
                self.random_shifts = False
                self.range_shifts = None
            else:
                self.random_shifts = True

        self.possible_shifts = None
        self.n_possible_shifts = None
        self.n_shifts = None
        self.shifts = None

        self.use_tmp_shifts = False
        self.n_tmp_shifts = None
        self.tmp_shifts = None

        if self.random_shifts:
            self.possible_shifts = self.range_shifts.to_list()
            self.n_possible_shifts = self.possible_shifts.__len__()
            if n_shifts is not None:
                self.n_shifts = n_shifts
                self.n_tmp_shifts = self.n_possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
                if self.n_tmp_shifts > self.n_shifts:
                    self.use_tmp_shifts = True
                    self.tmp_shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
                else:
                    self.shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)

    def set_n_shifts(self, n_shifts):

        if self.random_shifts and (n_shifts is not None):
            self.n_shifts = n_shifts
            self.n_tmp_shifts = self.n_possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
            if self.n_tmp_shifts > self.n_shifts:
                self.use_tmp_shifts = True
                self.tmp_shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
                self.shifts = None
            else:
                self.shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)

    def next_shifts(self):

        if self.random_shifts and (self.n_shifts is not None):
            if self.use_tmp_shifts:
                self.shifts = np.random.permutation(self.tmp_shifts)[:self.n_shifts]
            else:
                self.shifts = np.random.permutation(self.shifts)


class Loader:
    """
    A class used to load batches of samples

    Extended description

    Attributes
    ----------
    directory_root : str
        A formatted string to print out what the animal says
    time : Time
        The name of the animal
    L, n_levels_directories : int
        The number of the directory tree in the dataset.
    conditions_directories : sequence of sequences of ints
        The l_th element of the sequence contains the conditions of the l_th directory level that will be loaded

    Methods
    -------
    load_batches_e(order_outputs=None)
        It is a batch generator. It load a batch of samples at the time.
    """

    # TODO add inter-sample levels and intra-sample levels
    def __init__(
            self, directory_root, level_classes, n_levels_directories=None,
            conditions_directories=None, batch_size=None, n_batches=None,
            shuffle=False, time=None, transforms=None, device=None,
            order_outputs='il'):
        """
        Parameters
        ----------
        directory_root : str
            The directory of the dataset
        level_classes : int
            The directory level of the classes in the directory tree of the dataset.
        n_levels_directories : int, optional
            number of levels of the directory tree of the dataset (default is None). It is required if
            conditions_directories is None.
        conditions_directories : None or sequence of Nones and sequences of ints, optional
            Conditions_directories can be a sequence or None (default is None). If it is a sequence, the l_th element
            of it is None or a sequence of ints. If the l_th element is a sequence of ints, it contains the conditions
            of the tree l_th level that will be loaded. If the l_th element is None all conditions of the l_th level
            will be loaded. If conditions_directories is None all conditions in all level will be loaded. It requires
            to be a sequence if n_levels_directories is None.
        order_outputs : str or sequence of str, optional
            The desired outputs of the self.load_batches_e(). Accepted values are "i", "l", "c","r", "a" or any
            combination of them like "ilcr", "ilr" (default is "il"). "i" stands for input samples, "l" for labels of
            the samples, "c" for combinations of the level conditions of the samples, "r" for the relative directories
            of the samples, "a" for the absolute directories of the samples.
        """

        self.directory_root = directory_root
        self.level_classes = level_classes

        self.time = time

        if n_levels_directories is None:
            self.n_levels_directories = len(conditions_directories)
        elif conditions_directories is None:
            self.n_levels_directories = n_levels_directories
            conditions_directories = [None] * self.n_levels_directories  # type: list

        self.L = self.n_levels_directories

        self.shuffle = shuffle

        if transforms is None:
            self.transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
        else:
            self.transforms = transforms

        self.device = device

        self.conditions_directories_names = [None] * self.L  # type: list
        self.n_conditions_directories = [None] * self.L  # type: list
        self.conditions_directories = [None] * self.L  # type: list

        self.order_accepted_values = 'ilcra'
        if order_outputs is None:
            self.order_outputs = 'il'
            self.n_outputs = 2
        else:
            self.order_outputs = order_outputs
            self.n_outputs = len(self.order_outputs)
            for o in range(self.n_outputs):
                if not (self.order_outputs[o] in self.order_accepted_values):
                    raise ValueError('order_outputs')


        self.outputs = [None] * self.n_outputs  # type: list

        self.return_inputs_eb = 'i' in self.order_outputs
        self.return_labels_eb = 'l' in self.order_outputs
        self.return_combinations_eb = 'c' in self.order_outputs
        self.return_relative_directories_eb = 'r' in self.order_outputs
        self.return_absolute_directories_eb = 'a' in self.order_outputs

        directory_root_l = self.directory_root
        for l in range(self.L):
            self.conditions_directories_names[l] = os.listdir(directory_root_l)

            if conditions_directories[l] is None:
                self.n_conditions_directories[l] = len(self.conditions_directories_names[l])
                self.conditions_directories[l] = np.arange(self.n_conditions_directories[l])
            else:
                self.conditions_directories[l] = conditions_directories[l]
                self.n_conditions_directories[l] = len(self.conditions_directories[l])

            directory_root_l = os.path.join(directory_root_l, self.conditions_directories_names[l][0])

        if self.time is not None:
            if self.time.range_time.stop is None:
                self.time.range_time.stop = self.n_conditions_directories[self.time.level]
            self.conditions_directories[self.time.level] = (
                self.conditions_directories[self.time.level][self.time.range_time.to_slice()])
            self.n_conditions_directories[self.time.level] = len(self.conditions_directories[self.time.level])

        self.K = self.n_classes = self.n_conditions_directories[self.level_classes]
        self.V = self.n_variables = len(self.n_conditions_directories)
        self.n_samples = cc_maths.prod(self.n_conditions_directories)
        # self.n_samples = math.prod(self.n_conditions_directories)

        if batch_size is None:
            if n_batches is None:
                self.batch_size = self.n_samples
                self.n_batches = 1
            else:
                self.n_batches = n_batches
                self.batch_size = cc_maths.rint(self.n_samples / self.n_batches)
        else:
            self.batch_size = batch_size
            self.n_batches = cc_maths.rint(self.n_samples / self.batch_size)

        print('self.batch_size =', self.batch_size)
        print('self.n_samples =', self.n_samples)
        print('self.n_batches =', self.n_batches)
        print('self.time =', self.time)
        print('self.n_conditions_directories =', self.n_conditions_directories)
        # print('self.conditions_directories =', self.conditions_directories)

        if self.shuffle:
            self.batches_indexes = None
        else:
            self.batches_indexes = np.split(np.arange(self.n_samples), self.n_batches, axis=0)

        if (self.time is not None) and self.time.random_shifts:
            self.combinations_directories_no_shift = (
                cc_combinations.conditions_to_combinations(self.conditions_directories))
            self.combinations_directories = None
            # self.combinations_directories = np.copy(self.combinations_directories_no_shift)

            if self.time.n_shifts is None:
                self.time.set_n_shifts(self.n_samples)

            # self.time.next_shifts()
            # self.combinations_directories[:, self.time.level] += self.time.shifts
            if self.return_labels_eb:
                self.labels = torch.tensor(
                    self.combinations_directories_no_shift[slice(0, self.n_samples, 1), self.level_classes],
                    dtype=torch.int64, device=self.device)
            else:
                self.labels = None

        else:
            self.combinations_directories_no_shift = None
            self.combinations_directories = (
                cc_combinations.conditions_to_combinations(self.conditions_directories))
            if self.return_labels_eb:
                self.labels = torch.tensor(
                    self.combinations_directories[slice(0, self.n_samples, 1), self.level_classes],
                    dtype=torch.int64, device=self.device)
            else:
                self.labels = None

        if self.return_relative_directories_eb:
            self.relative_directories_eb = [None] * self.batch_size  # type: list
        else:
            self.relative_directories_eb = None

        if self.return_absolute_directories_eb:
            self.absolute_directories_eb = [None] * self.batch_size  # type: list
        else:
            self.absolute_directories_eb = None

        combination_directory_str_0 = [self.conditions_directories_names[l][0] for l in range(self.L)]
        directory_0 = os.path.join(self.directory_root, *combination_directory_str_0)
        image_0 = PIL.Image.open(directory_0)
        tensor_0 = self.transforms(image_0)
        # shape_sample_0 = np.asarray(tensor_0.shape)
        # self.shape_sample = shape_sample_0
        # self.shape_batch = np.empty(self.shape_sample.size + 1, self.shape_sample.dtype)
        # self.shape_batch[0] = self.batch_size
        # self.shape_batch[1:] = self.shape_sample
        # self.tensor_batch = torch.empty(tuple(self.shape_batch), dtype=tensor_0.dtype)
        shape_sample_0 = list(tensor_0.shape)
        self.shape_sample = shape_sample_0
        self.shape_batch = torch.Size(tuple([self.batch_size] + shape_sample_0))
        if self.return_inputs_eb:
            self.inputs_eb = torch.empty(self.shape_batch, dtype=tensor_0.dtype, device=self.device)
        else:
            self.inputs_eb = None

        self.n_dims_samples = self.shape_sample.__len__()
        self.n_dims_batch = self.n_dims_samples + 1
        self.indexes_batch = np.empty(self.n_dims_batch, dtype=object)
        self.indexes_batch[1:] = slice(0, None, 1)

        print('self.shape_batch =', self.shape_batch)
        print()

    def load_batches_e(self):
        """
        short description

        long description

        Returns
        -------
        out : generator
            A generator of lists of elements requested in order_outputs. The elements have the same order as in
            order_outputs. It generates a list per batch of input samples.

        Raises
        ------
        ValueError
            somenthing

        Examples
        --------
        example 1:

        >>> a = 2
        >>> b = 3
        >>> a + b
        5

        example 2:

        >>> a = 2
        >>> b = 3
        >>> a * b
        6

        """

        if (self.time is not None) and self.time.random_shifts:
            self.time.next_shifts()
            self.combinations_directories = np.copy(self.combinations_directories_no_shift)
            self.combinations_directories[:, self.time.level] += self.time.shifts

        if self.shuffle:
            self.batches_indexes = np.split(np.random.permutation(self.n_samples), self.n_batches, axis=0)

        for b in range(self.n_batches):
            if self.return_labels_eb:
                labels_eb = self.labels[self.batches_indexes[b]]

            combinations_eb = self.combinations_directories[self.batches_indexes[b], :]
            # batch_size_eb = batches_indexes_e.shape[0]
            for i in range(self.batch_size):
                combination_directory_ebi = combinations_eb[i, :]
                combination_directory_str_ebi = [
                    self.conditions_directories_names[l][combination_directory_ebi[l]] for l in range(self.L)]

                relative_directory_ebi = os.path.join(*combination_directory_str_ebi)
                absolute_directory_ebi = os.path.join(self.directory_root, relative_directory_ebi)

                self.indexes_batch[0] = i

                if self.return_inputs_eb:
                    inputs_ebi = PIL.Image.open(absolute_directory_ebi)
                    self.inputs_eb[tuple(self.indexes_batch)] = self.transforms(inputs_ebi)

                if self.return_relative_directories_eb:
                    self.relative_directories_eb[i] = relative_directory_ebi

                if self.return_absolute_directories_eb:
                    self.absolute_directories_eb[i] = absolute_directory_ebi

            for o in range(self.n_outputs):
                if self.order_outputs[o] == 'i':
                    self.outputs[o] = self.inputs_eb
                elif self.order_outputs[o] == 'l':
                    self.outputs[o] = labels_eb
                elif self.order_outputs[o] == 'c':
                    self.outputs[o] = combinations_eb
                elif self.order_outputs[o] == 'r':
                    self.outputs[o] = self.relative_directories_eb
                elif self.order_outputs[o] == 'a':
                    self.outputs[o] = self.absolute_directories_eb

            yield self.outputs


def train_classifier_with_early_stop(
        model, loader, criterion, optimizer, scheduler, I=20, directory_outputs=''):
    # timer = cc_clock.Timer()
    cc_timer = cc_clock.Timer()

    for key_loader_k in loader.keys():
        if key_loader_k == 'training' or key_loader_k == 'validation':
            pass
        else:
            raise ValueError('Unknown keys in loader')

    headers = [
        'Epoch', 'Unsuccessful Epochs', 'Training Loss', 'Training Accuracy',
        'Valuation Loss', 'Lowest Valuation Loss', 'Is Lower Loss',
        'Valuation Accuracy', 'Highest Valuation Accuracy', 'Is Higher Accuracy']

    n_columns = len(headers)
    new_line_stats = [None] * n_columns  # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    directory_model = os.path.join(directory_outputs, 'model.pth')
    directory_model_state = os.path.join(directory_outputs, 'model_state.pth')
    directory_stats = os.path.join(directory_outputs, 'stats.csv')

    n_decimals_for_printing = 6

    best_model_wts = copy.deepcopy(model.state_dict())

    lowest_loss = math.inf
    lowest_loss_str = str(lowest_loss)
    highest_accuracy = -math.inf
    highest_accuracy_str = str(highest_accuracy)

    i = 0
    e = 0

    n_dashes = 110
    dashes = '-' * n_dashes
    print(dashes)

    while i < I:

        print('Epoch {e} ...'.format(e=e))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e

        # Each epoch has a training and a validation phase
        # training phase
        model.train()  # Set model to training mode
        criterion.train()

        running_loss_e = 0.0
        running_corrects_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['training'].load_batches_e():
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            # track history
            torch.set_grad_enabled(True)
            outputs = model(batch_eb)
            _, preds = torch.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            # backward + optimize
            loss_eb.backward()
            optimizer.step()

            torch.set_grad_enabled(False)

            # # statistics
            # loss_float_eb = loss_eb.item()
            # # noinspection PyTypeChecker
            # corrects_eb = torch.sum(preds == labels_eb).item()
            # accuracy_eb = corrects_eb / batch_eb.shape[0]
            # loss_str_eb = cc_strings_format_float_to_str(loss_float_eb, n_decimals=n_decimals_for_printing)
            # accuracy_str_eb = cc_strings_format_float_to_str(accuracy_eb, n_decimals=n_decimals_for_printing)
            # print('Training. Epoch: {:d}. Batch {:d}. Loss: {:s}. Accuracy: {:s}.'.format(e, b, loss_str_eb, accuracy_str_eb))

            running_loss_e += loss_eb.item() * batch_eb.shape[0]
            # noinspection PyTypeChecker
            running_corrects_e += torch.sum(preds == labels_eb).item()

            b += 1

        # scheduler.step()

        loss_e = running_loss_e / loader['training'].n_samples
        accuracy_e = running_corrects_e / loader['training'].n_samples
        # loss_e = float(running_loss_e / loader['training'].n_samples)
        # accuracy_e = float(running_corrects_e / loader['training'].n_samples)

        loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cc_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        print('Epoch: {:d}. Training.   Loss: {:s}. Accuracy: {:s}.'.format(e, loss_str_e, accuracy_str_e))

        stats['lines'][e][stats['headers']['Training Loss']] = loss_e
        stats['lines'][e][stats['headers']['Training Accuracy']] = accuracy_e
        # stats['Training Loss'].append(float(loss_e))
        # stats['Training Accuracy'].append(float(accuracy_e))

        # validation phase
        model.eval()  # Set model to evaluate mode

        criterion.eval()

        # zero the parameter gradients
        optimizer.zero_grad()

        torch.set_grad_enabled(False)

        running_loss_e = 0.0
        running_corrects_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['validation'].load_batches_e():
            # forward
            outputs = model(batch_eb)
            _, preds = torch.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            # # statistics
            # loss_float_eb = loss_eb.item()
            # # noinspection PyTypeChecker
            # corrects_eb = torch.sum(preds == labels_eb).item()
            # accuracy_eb = corrects_eb / batch_eb.shape[0]
            # loss_str_eb = cc_strings_format_float_to_str(loss_float_eb, n_decimals=n_decimals_for_printing)
            # accuracy_str_eb = cc_strings_format_float_to_str(accuracy_eb, n_decimals=n_decimals_for_printing)
            # print('Validation. Epoch: {:d}. Batch {:d}. Loss: {:s}. Accuracy: {:s}.'.format(e, b, loss_str_eb, accuracy_str_eb))

            running_loss_e += loss_eb.item() * batch_eb.shape[0]
            # noinspection PyTypeChecker
            running_corrects_e += torch.sum(preds == labels_eb).item()

            b += 1

        loss_e = running_loss_e / loader['validation'].n_samples
        accuracy_e = running_corrects_e / loader['validation'].n_samples
        # loss_e = float(running_loss_e / loader['training'].n_samples)
        # accuracy_e = float(running_corrects_e / loader['training'].n_samples)

        loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cc_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        stats['lines'][e][stats['headers']['Valuation Loss']] = loss_e
        stats['lines'][e][stats['headers']['Valuation Accuracy']] = accuracy_e

        if accuracy_e > highest_accuracy:
            highest_accuracy = accuracy_e
            highest_accuracy_str = cc_strings_format_float_to_str(highest_accuracy, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 1
            stats['lines'][e][stats['headers']['Highest Valuation Accuracy']] = highest_accuracy
        else:
            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 0
            stats['lines'][e][stats['headers']['Highest Valuation Accuracy']] = highest_accuracy

        if loss_e < lowest_loss:

            lowest_loss = loss_e
            lowest_loss_str = cc_strings_format_float_to_str(lowest_loss, n_decimals=n_decimals_for_printing)
            i = 0
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 1
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Valuation Loss']] = lowest_loss

            best_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
            for directory_i in [directory_model, directory_model_state, directory_stats]:
                if os.path.isfile(directory_i):
                    os.remove(directory_i)

            torch.save(model, directory_model)
            torch.save(best_model_wts, directory_model_state)

            cc_txt.lines_to_csv_file(directory_stats, stats['lines'], stats['headers'])
        else:
            i += 1
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 0
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Valuation Loss']] = lowest_loss

            if os.path.isfile(directory_stats):
                os.remove(directory_stats)
            cc_txt.lines_to_csv_file(directory_stats, stats['lines'], stats['headers'])

        print('Epoch: {:d}. Validation. Loss: {:s}. Lowest Loss: {:s}. Accuracy: {:s}. Highest Accuracy: {:s}.'.format(
            e, loss_str_e, lowest_loss_str, accuracy_str_e, highest_accuracy_str))

        print('Epoch {e} - Unsuccessful Epochs {i}.'.format(e=e, i=i))

        e += 1
        print(dashes)

    print()
    E = e

    time_training = cc_timer.get_delta_time()

    print('Training completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_training.days, h=time_training.hours,
        m=time_training.minutes, s=time_training.seconds))
    print('Number of Epochs: {E:d}'.format(E=E))
    print('Lowest Validation Loss: {:s}'.format(lowest_loss_str))
    print('Highest Validation Accuracy: {:s}'.format(highest_accuracy_str))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, stats


def extract_features(model, loader, directory_dataset_features=''):
    cc_timer = cc_clock.Timer()

    n_decimals_for_printing = 6

    if model.training:
        model.eval()  # Set model to evaluate mode

    # Now set requires_grad to false
    for param in model.parameters():
        param.requires_grad = False

    torch.set_grad_enabled(False)

    # Iterate over data.
    for data_eb in loader.load_batches_e():

        samples_eb, relative_directories_eb = data_eb

        # forward
        outputs_eb = model(samples_eb)
        # outputs_eb = outputs_eb.numpy()

        # _, a = torch.max(outputs_eb, 1)
        # a = a.cpu().numpy()

        # 1. produce the directory_features
        relative_directories_features_eb = cc_directory.replace_extensions(relative_directories_eb, 'csv')
        absolute_directories_features_eb = cc_directory.conditions_to_directories(
            [[directory_dataset_features], relative_directories_features_eb], order_outputs='v')

        # 2. save features (make funtion array_to_csv_files(array, directories, axes='frc'))
        outputs_eb = torch.unsqueeze(outputs_eb, 1).cpu().numpy()
        # outputs_eb = torch.unsqueeze(outputs_eb, 1).numpy()
        cc_txt.array_to_csv_files(
            outputs_eb, 1, 2, [absolute_directories_features_eb], headers=None)

    time_extraction = cc_timer.get_delta_time()

    print('Test completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_extraction.days, h=time_extraction.hours,
        m=time_extraction.minutes, s=time_extraction.seconds))


def test_classifier(model, loader, criterion, directory_test_output):
    cc_timer = cc_clock.Timer()

    headers_stats = ['N_samples', *['C_' + str(v) for v in range(loader.V)], 'Loss', 'Accuracy']

    n_columns_stats = len(headers_stats)
    line_stats = [loader.n_samples, *loader.n_conditions_directories, None, None]  # type: list

    stats = {
        'headers': {headers_stats[i]: i for i in range(n_columns_stats)},
        'lines': [line_stats]}

    headers_trials = [
        'ID_Trial',
        *['Condition_' + str(v) for v in range(loader.V)],
        'Label',
        *['Probability_' + str(k) for k in range(loader.K)],
        'Classification',
        'Correct_Classification'
    ]

    n_columns_trials = len(headers_trials)

    trials = {
        'headers': {headers_trials[i]: i for i in range(n_columns_trials)},
        'lines': None}

    n_decimals_for_printing = 6

    if model.training:
        model.eval()  # Set model to evaluate mode

    if criterion.training:
        criterion.eval()

    softmax = torch.nn.Softmax(dim=1)
    if softmax.training:
        softmax.eval()

    # Now set requires_grad to false
    for param_model in model.parameters():
        param_model.requires_grad = False

    for param_criterion in criterion.parameters():
        param_criterion.requires_grad = False

    for param_softmax in softmax.parameters():
        param_softmax.requires_grad = False

    torch.set_grad_enabled(False)

    running_loss_e = 0.0
    running_corrects_e = 0

    start_index_samples = 0
    stop_index_samples = 0

    index_combinations_e = np.empty(2, dtype=object)
    index_combinations_e[1] = slice(0, loader.V, 1)
    combinations_e = np.empty([loader.n_samples, loader.V], dtype=object)

    index_outputs_e = np.empty(2, dtype=object)
    index_outputs_e[1] = slice(0, loader.K, 1)
    outputs_e = np.empty([loader.n_samples, loader.K], dtype=object)

    index_labels_e = np.empty(2, dtype=object)
    index_labels_e[1] = 0
    labels_e = np.empty([loader.n_samples, 1], dtype=object)

    classifications_e = labels_e.copy()

    correct_classifications_e = labels_e.copy()

    id_trials = np.arange(loader.n_samples, dtype=object)[:, None]

    # b = 0
    # Iterate over data.
    for data_eb in loader.load_batches_e():
        samples_eb, labels_eb, combinations_eb = data_eb

        # forward
        outputs_eb = model(samples_eb)
        probabilities_eb = softmax(outputs_eb)
        _, classifications_eb = torch.max(outputs_eb, 1)
        correct_classifications_eb = (classifications_eb == labels_eb).long()
        loss_eb = criterion(outputs_eb, labels_eb)

        # todo: get probabilities
        # todo: fill trials['lines']

        stop_index_samples += samples_eb.shape[0]
        index_samples = slice(start_index_samples, stop_index_samples, 1)

        index_combinations_e[0] = index_samples
        combinations_e[tuple(index_combinations_e)] = combinations_eb.tolist()

        index_outputs_e[0] = index_samples
        outputs_e[tuple(index_outputs_e)] = probabilities_eb.tolist()

        index_labels_e[0] = index_samples
        labels_e[tuple(index_labels_e)] = labels_eb.tolist()

        classifications_e[tuple(index_labels_e)] = classifications_eb.tolist()

        correct_classifications_e[tuple(index_labels_e)] = correct_classifications_eb.tolist()

        start_index_samples = stop_index_samples

        running_loss_e += loss_eb.item() * samples_eb.shape[0]
        # noinspection PyTypeChecker
        running_corrects_e += torch.sum(correct_classifications_eb).item()

        # b += 1

    loss_e = running_loss_e / loader.n_samples
    accuracy_e = running_corrects_e / loader.n_samples

    stats['lines'][0][stats['headers']['Loss']] = loss_e
    stats['lines'][0][stats['headers']['Accuracy']] = accuracy_e

    trials['lines'] = np.concatenate(
        (id_trials, combinations_e, labels_e, outputs_e, classifications_e, correct_classifications_e),
        axis=1)

    loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
    accuracy_str_e = cc_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

    print('Test. Loss: {:s}. Accuracy: {:s}.'.format(loss_str_e, accuracy_str_e))
    print()

    time_test = cc_timer.get_delta_time()

    print('Test completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_test.days, h=time_test.hours,
        m=time_test.minutes, s=time_test.seconds))

    return stats, trials


class ResNetNoLastLayer(torchvision.models.resnet.ResNet):

    def __init__(self, name_resnet):

        if name_resnet == 'resnet18':
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.BasicBlock, [2, 2, 2, 2])
        elif name_resnet == 'resnet34':
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.BasicBlock, [3, 4, 6, 3])
        elif name_resnet == 'resnet50':
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.Bottleneck, [3, 4, 6, 3])
        elif name_resnet == 'resnet101':
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.Bottleneck, [3, 4, 23, 3])
        elif name_resnet == 'resnet152':
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.Bottleneck, [3, 8, 36, 3])

        elif name_resnet == 'resnext50_32x4d':
            kwargs = {'groups': 32, 'width_per_group': 4}
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.Bottleneck, [3, 4, 6, 3], **kwargs)

        elif name_resnet == 'resnext101_32x8d':
            kwargs = {'groups': 32, 'width_per_group': 8}
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.Bottleneck, [3, 4, 23, 3], **kwargs)

        elif name_resnet == 'wide_resnet50_2':
            kwargs = {'width_per_group': 64 * 2}
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.Bottleneck, [3, 4, 6, 3], **kwargs)

        elif name_resnet == 'wide_resnet101_2':
            kwargs = {'width_per_group': 64 * 2}
            super(ResNetNoLastLayer, self).__init__(torchvision.models.resnet.Bottleneck, [3, 4, 23, 3], **kwargs)

    def _forward_impl(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        return x


def load_resnet(name_resnet, last_layer=True, K=None, softmax=False, pretrained=False, device=None):

    if last_layer:
        if isinstance(pretrained, str):
            resnet = load_model(name_resnet, pretrained=False, device=None)
        else:
            resnet = load_model(name_resnet, pretrained=pretrained, device=None)

        if (K is None) or (K == resnet.fc.out_features):
            if softmax:
                resnet.fc = torch.nn.Sequential(resnet.fc, torch.nn.Softmax())
        else:
            num_ftrs = resnet.fc.in_features
            if softmax:
                resnet.fc = torch.nn.Sequential(torch.nn.Linear(num_ftrs, K), torch.nn.Softmax())
            else:
                # Here the size of each output sample is set to K.
                resnet.fc = torch.nn.Linear(num_ftrs, K)
        if isinstance(pretrained, str):
            state_dict = torch.load(pretrained)
            resnet.load_state_dict(state_dict)
    else:
        resnet = ResNetNoLastLayer(name_resnet)

        if isinstance(pretrained, str):
            if not ((K is None) or (K == resnet.fc.out_features)):
                num_ftrs = resnet.fc.in_features
                resnet.fc = torch.nn.Linear(num_ftrs, K)
            state_dict = torch.load(pretrained)
            resnet.load_state_dict(state_dict)
        elif pretrained:
            urls_resnets = {
                'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
                'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
                'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
                'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
                'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
                'resnext50_32x4d': 'https://download.pytorch.org/models/resnext50_32x4d-7cdf4587.pth',
                'resnext101_32x8d': 'https://download.pytorch.org/models/resnext101_32x8d-8ba56ff5.pth',
                'wide_resnet50_2': 'https://download.pytorch.org/models/wide_resnet50_2-95faca4d.pth',
                'wide_resnet101_2': 'https://download.pytorch.org/models/wide_resnet101_2-32ee1156.pth',
            }
            state_dict = torch.hub.load_state_dict_from_url(urls_resnets[name_resnet])
            resnet.load_state_dict(state_dict)
        delattr(resnet, 'fc')

    resnet = set_device(resnet, device)

    return resnet


def load_model(name_model, pretrained=False, device=None):
    # model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet152', pretrained=True)

    # model = torchvision.models.resnet18()
    if isinstance(name_model, str):
        template_load_string = f"model = torchvision.models.{name_model:s}(pretrained=pretrained)"
    else:
        template_load_string = f"model = torchvision.models.{str(name_model):s}(pretrained=pretrained)"

    dict_globals = {'__builtins__': None}
    if isinstance(pretrained, str):
        dict_locals = {'torchvision': torchvision, 'pretrained': False}  # type: dict
    else:
        dict_locals = {'torchvision': torchvision, 'pretrained': pretrained}  # type: dict
    exec(template_load_string, dict_globals, dict_locals)
    model = dict_locals['model']

    if isinstance(pretrained, str):
        model.load_state_dict(torch.load(pretrained))

    model = set_device(model, device)

    return model


def set_device(tensor, device):

    # if isinstance(tensor, torch.Tensor):
    if isinstance(tensor, (torch.nn.Module, torch.Tensor)):
        if device is None:
            return tensor
        elif isinstance(device, (str, torch.device)):
            tensor = tensor.to(device)
            return tensor
        else:
            raise TypeError('device')
    else:
        raise TypeError('tensor')

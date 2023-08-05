from matplotlib import pyplot as plt
# import seaborn as sns; sns.set()


def heat_maps(
        values, shape_figure=None,
        id_figures=None, directories_images=None, formats_images=['svg'], hspace=0.5,
        annot=False, fmt_annot=['.2g'], fontsize_annot=None,
        titles=None, x_labels=None, y_labels=None, xticklabels='auto', yticklabels='auto',
        fontsize_title='auto', rotation_title='auto',
        fontsize_x_labels='auto', rotation_x_labels='auto',
        fontsize_y_labels='auto', rotation_y_labels='auto',
        fontsize_xticklabels='auto', rotation_xticklabels='auto',
        fontsize_yticklabels='auto', rotation_yticklabels='auto',
        cmap=None, fontsize_cbar_ticklabels='auto'):

    figures_existing = plt.get_fignums()
    n_figures_existing = len(figures_existing)

    if id_figures is None:
        n_figures = values.shape[0]
        id_figures = [None] * n_figures
        i = 0
        f = 0
        while f < n_figures:
            if i in figures_existing:
                pass
            else:
                id_figures[f] = i
                f += 1
            i += 1
    else:
        n_figures = len(id_figures)
        for f in id_figures:
            if f in figures_existing:
                print('Warning: overwriting plot {}'.format(f))

    # plt.figure(0, frameon=False, dpi=200)
    # plt.figure(1,  frameon=False, dpi=200)
    if shape_figure is None:
        rows = values.shape[1]
        colomns = 1
    else:
        rows = shape_figure.shape[0]
        colomns = shape_figure.shape[1]

    n_figures = values.shape[0]
    n_subplots_per_fig = values.shape[1]

    a_num = ord('a')
    if titles is None:
        titles = ['{})'] * n_subplots_per_fig
    else:
        n_titles = len(titles)
        for t in range(n_titles):
            titles[t] = '{}) ' + titles[t]

    if cmap is None:
        cmap = [None] * n_subplots_per_fig

    if len(fmt_annot) == 1:
        fmt_annot = fmt_annot * n_subplots_per_fig
    # if x_labels is None:
    #     x_labels = [None] * n_subplots_per_fig
    #
    # if y_labels is None:
    #     y_labels = [None] * n_subplots_per_fig

    subplot = (100 * rows) + (10 * colomns) + 1
    for f in range(n_figures):

        plt.figure(id_figures[f], frameon=False, dpi=200)
        # plt.figure(f)

        for s in range(n_subplots_per_fig):

            plt.subplot(subplot + s)
            ax = sns.heatmap(
                values[f, s], annot=annot, fmt=fmt_annot[s], cmap=cmap[s],
                xticklabels=xticklabels,
                yticklabels=yticklabels,
                annot_kws=dict([('fontsize', fontsize_annot)]))

            if xticklabels is not False:
                # r=0 and s=8
                if fontsize_xticklabels != 'auto' and rotation_xticklabels == 'auto':
                    plt.xticks(fontsize=fontsize_xticklabels)
                elif fontsize_xticklabels == 'auto' and rotation_xticklabels != 'auto':
                    plt.xticks(rotation=rotation_xticklabels)
                elif fontsize_xticklabels != 'auto' and rotation_xticklabels != 'auto':
                    plt.xticks(fontsize=fontsize_xticklabels, rotation=rotation_xticklabels)


            if yticklabels is not False:
                # r=0 and s=8
                if fontsize_yticklabels != 'auto' and rotation_yticklabels == 'auto':
                    plt.yticks(fontsize=fontsize_yticklabels)
                elif fontsize_yticklabels == 'auto' and rotation_yticklabels != 'auto':
                    plt.yticks(rotation=rotation_yticklabels)
                elif fontsize_yticklabels != 'auto' and rotation_yticklabels != 'auto':
                    plt.yticks(fontsize=fontsize_yticklabels, rotation=rotation_yticklabels)

            if fontsize_cbar_ticklabels != 'auto':
                # fontsize_cbar_ticklabels = 8
                # use matplotlib.colorbar.Colorbar object
                cbar = ax.collections[0].colorbar
                # here set the labelsize
                cbar.ax.tick_params(labelsize=fontsize_cbar_ticklabels)

            # general layout
            # fontsize_x_labels = 12
            # rotation_x_labels = 0
            if fontsize_title == 'auto' and rotation_title == 'auto':
                plt.title(titles[s].format(chr(a_num + s), f))
            elif fontsize_title != 'auto' and rotation_title == 'auto':
                plt.title(titles[s].format(chr(a_num + s), f), fontsize=fontsize_title)
            elif fontsize_title == 'auto' and rotation_title != 'auto':
                plt.title(titles[s].format(chr(a_num + s), f), rotation=rotation_title)
            elif fontsize_title != 'auto' and rotation_title != 'auto':
                plt.title(titles[s].format(chr(a_num + s), f), fontsize=fontsize_title, rotation=rotation_title)

            if x_labels is not None:
                # fontsize_x_labels = 10
                # rotation_x_labels = 0
                if fontsize_x_labels == 'auto' and rotation_x_labels == 'auto':
                    plt.xlabel(x_labels)
                elif fontsize_x_labels != 'auto' and rotation_x_labels == 'auto':
                    plt.xlabel(x_labels, fontsize=fontsize_x_labels)
                elif fontsize_x_labels == 'auto' and rotation_x_labels != 'auto':
                    plt.xlabel(x_labels, rotation=rotation_x_labels)
                elif fontsize_x_labels != 'auto' and rotation_x_labels != 'auto':
                    plt.xlabel(x_labels, fontsize=fontsize_x_labels, rotation=rotation_x_labels)

            if y_labels is not None:
                # fontsize_y_labels = 10
                # rotation_y_labels = 0
                if fontsize_y_labels == 'auto' and rotation_y_labels == 'auto':
                    plt.ylabel(y_labels)
                elif fontsize_y_labels != 'auto' and rotation_y_labels == 'auto':
                    plt.ylabel(y_labels, fontsize=fontsize_y_labels)
                elif fontsize_y_labels == 'auto' and rotation_y_labels != 'auto':
                    plt.ylabel(y_labels, rotation=rotation_y_labels)
                elif fontsize_y_labels != 'auto' and rotation_y_labels != 'auto':
                    plt.ylabel(y_labels, fontsize=fontsize_y_labels, rotation=rotation_y_labels)

    save_figure(id_figures=id_figures, directories=directories_images, formats=formats_images, hspace=hspace)

    plt.close('all')


def save_figure(id_figures=None, directories=None, formats=['svg'], hspace=0.5):
    
    if id_figures is None:
        id_figures = plt.get_fignums()
        
    n_figures = len(id_figures)

    if directories is None:
        directories = id_figures
    else:
        n_directories = len(directories)
        if n_figures != n_directories:
            raise ValueError('n_figures and n_directories must be equal.\n'
                             'Now, n_figures = {} and n_directories = {}'.format(n_figures, n_directories))

    n_formats = len(formats)
    for i in range(n_figures):

        plt.figure(id_figures[i])

        for j in range(n_formats):

            plt.subplots_adjust(hspace=hspace)
            directory_i_j = '.'.join([directories[i], formats[j]])
            plt.savefig(directory_i_j, format=formats[j], bbox_inches='tight', pad_inches=0.0)

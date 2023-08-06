.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_adversarial_robustness_plot_visualizing_adversarial_attacks.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_adversarial_robustness_plot_visualizing_adversarial_attacks.py:


Visualizing Adversarial Examples
================================

This example shows how to generate and plot adversarial examples for a batch of datapoints from CIFAR-10,
and compares the examples from different constraint sets, penalizations and solvers.



.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/adversarial_robustness/images/sphx_glr_plot_visualizing_adversarial_attacks_001.png
          :alt: cat, ship, ship, plane, frog, frog, car, cat, car, car, ship, frog, cat, car, cat, car, car, ship, deer, cat, dog, cat, ship, car, car, frog, frog, car
          :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/adversarial_robustness/images/sphx_glr_plot_visualizing_adversarial_attacks_002.png
          :alt: plot visualizing adversarial attacks
          :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/adversarial_robustness/images/sphx_glr_plot_visualizing_adversarial_attacks_003.png
          :alt: plot visualizing adversarial attacks
          :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/adversarial_robustness/images/sphx_glr_plot_visualizing_adversarial_attacks_004.png
          :alt: plot visualizing adversarial attacks
          :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    <frozen importlib._bootstrap>:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
    <frozen importlib._bootstrap>:219: RuntimeWarning: numpy.ufunc size changed, may indicate binary incompatibility. Expected 192 from C header, got 216 from PyObject
    Files already downloaded and verified
    L2 norm constraint.
    GroupL1 constraint.
    F1 score: 0.095 for alpha=0.8000
    Nuclear norm ball adv examples
    F1 score: 0.633 for alpha=0.5000






|


.. code-block:: default



    from itertools import product

    import numpy as np

    import torch
    import torchvision

    from robustbench.data import load_cifar10
    from robustbench.utils import load_model

    import matplotlib.pyplot as plt

    import chop
    from chop.image import group_patches, matplotlib_imshow_batch
    from chop.logging import Trace

    from sklearn.metrics import f1_score

    from torch.autograd import profiler

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # device = torch.device('cpu')

    batch_size = 7

    # Note that this example uses load_cifar10 from the robustbench library
    data, target = load_cifar10(n_examples=batch_size, data_dir='~/datasets')
    data = data.to(device)
    target = target.to(device)

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse',
               'ship', 'truck')


    model = load_model('Standard')  # Can be changed to any model from the robustbench model zoo
    model = model.to(device)
    criterion = torch.nn.CrossEntropyLoss(reduction='none')

    # Define the constraint set + initial point
    print("L2 norm constraint.")
    alpha = 127 / 255
    constraint = chop.constraints.L2Ball(alpha)


    def image_constraint_prox(delta, step_size=None):
        adv_img = torch.clamp(data + delta, 0, 1)
        delta = adv_img - data
        return delta


    def prox(delta, step_size=None):
        delta = constraint.prox(delta, step_size)
        delta = image_constraint_prox(delta, step_size)
        return delta


    adversary = chop.Adversary(chop.optim.minimize_pgd_madry)
    callback_L2 = Trace()
    _, delta = adversary.perturb(data, target, model, criterion,
                                 prox=prox,
                                 lmo=constraint.lmo,
                                 max_iter=20,
                                 step=2. / 20,
                                 callback=callback_L2)

    # Plot adversarial images
    fig, ax = plt.subplots(nrows=7, ncols=batch_size, figsize=(16, 14))

    # Plot clean data
    matplotlib_imshow_batch(data, labels=[classes[k] for k in target], axes=ax[0, :],
                            title="Original images")

    # Adversarial Lp images
    adv_output = model(data + delta)
    adv_labels = torch.argmax(adv_output, dim=-1)
    matplotlib_imshow_batch(data + delta, labels=[classes[k] for k in adv_labels], axes=ax[1, :],
                            title=f'L{constraint.p}')

    # Perturbation
    matplotlib_imshow_batch(abs(delta), axes=ax[4, :], normalize=True,
                            title=f'L{constraint.p}')


    print("GroupL1 constraint.")

    groups = group_patches(x_patch_size=8, y_patch_size=8)

    for eps in [5e-2]:
        alpha = eps * len(groups)
        constraint_group = chop.constraints.GroupL1Ball(alpha, groups)
        adversary_group = chop.Adversary(chop.optim.minimize_frank_wolfe)

        # callback_group = Trace(callable=lambda kw: criterion(model(data + kw['x']), target))
        callback_group = Trace()

        with profiler.profile() as prof:
            _, delta_group = adversary_group.perturb(data, target, model, criterion,
                                                    lmo=constraint_group.lmo,
                                                    max_iter=20,
                                                    callback=callback_group)

    
        delta_group = image_constraint_prox(delta_group)

        # Show adversarial examples and perturbations
        adv_output_group = model(data + delta_group)
        adv_labels_group = torch.argmax(adv_output_group, dim=-1)

        matplotlib_imshow_batch(data + delta_group, labels=(classes[k] for k in adv_labels_group),
                                axes=ax[2, :],
                                title='Group Lasso')

        matplotlib_imshow_batch(abs(delta_group), axes=ax[5, :], normalize=True,
                                title='Group Lasso')

        print(f"F1 score: {f1_score(target.detach().cpu(), adv_labels_group.detach().cpu(), average='macro'):.3f}"
              f" for alpha={alpha:.4f}")

    print("Nuclear norm ball adv examples")

    for alpha in [.5]:
        constraint_nuc = chop.constraints.NuclearNormBall(alpha)


        def prox_nuc(delta, step_size=None):
            delta = constraint_nuc.prox(delta, step_size)
            delta = image_constraint_prox(delta, step_size)
            return delta


        adversary = chop.Adversary(chop.optim.minimize_frank_wolfe)
        callback_nuc = Trace()

        _, delta_nuc = adversary.perturb(data, target, model, criterion,
                                    #  prox=prox,
                                    lmo=constraint_nuc.lmo,
                                    max_iter=20,
                                    #  step=2. / 20,
                                    callback=callback_nuc)

        # Clamp last iterate to image space
        delta_nuc = image_constraint_prox(delta_nuc)

        # Add nuclear examples to plot
        adv_output_nuc = model(data + delta_nuc)
        adv_labels_nuc = torch.argmax(adv_output_nuc, dim=-1)

        matplotlib_imshow_batch(data + delta_nuc, labels=(classes[k] for k in adv_labels_nuc),
                                axes=ax[3, :],
                                title='Nuclear Norm')

        matplotlib_imshow_batch(abs(delta_nuc), axes=ax[6, :], normalize=True,
                                title='Nuclear Norm')

        print(f"F1 score: {f1_score(target.detach().cpu(), adv_labels_nuc.detach().cpu(), average='macro'):.3f}"
              f" for alpha={alpha:.4f}")

    plt.tight_layout()
    plt.show()


    # TODO refactor this in functions

    # Plot group lasso loss values
    fig, ax = plt.subplots(figsize=(6, 10), nrows=batch_size, sharex=True)
    for k in range(batch_size):
        ax[k].plot([-trace[k] for trace in callback_group.trace_f])
    plt.tight_layout()
    plt.show()

    # Plot loss functions per datapoint
    fig, ax = plt.subplots(figsize=(6, 10), nrows=batch_size, sharex=True)
    for k in range(batch_size):
        ax[k].plot([-trace[k] for trace in callback_nuc.trace_f])

    plt.tight_layout()
    plt.show()

    # Plot loss functions per datapoint
    fig, ax = plt.subplots(figsize=(6, 10), nrows=batch_size, sharex=True)
    for k in range(batch_size):
        ax[k].plot([-trace[k] for trace in callback_L2.trace_f])

    plt.tight_layout()
    plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  22.447 seconds)

**Estimated memory usage:**  2548 MB


.. _sphx_glr_download_auto_examples_adversarial_robustness_plot_visualizing_adversarial_attacks.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_visualizing_adversarial_attacks.py <plot_visualizing_adversarial_attacks.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_visualizing_adversarial_attacks.ipynb <plot_visualizing_adversarial_attacks.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_

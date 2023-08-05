from __future__ import print_function
import numpy as np
import os
import pandas as pd
from pyniel.python_tools.path_tools import make_dir_if_not_exists
import time
from datetime import datetime

from navrep.tools.data_extraction import archive_to_lidar_dataset
from navrep.tools.rings import generate_rings
from navrep.models.vae2d import ConvVAE, reset_graph
from navrep.tools.commonargs import parse_common_args

_Z = 32

if __name__ == "__main__":
    common_args, _ = parse_common_args()
    VARIANT = common_args.environment
    print(common_args)

    # Parameters for training
    batch_size = 100
    DATA_DIR = "record"
    START_TIME = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    MAX_STEPS = common_args.n
    if MAX_STEPS is None:
        MAX_STEPS = 222222
    NUM_EPOCH = MAX_STEPS  # don't limit based on epoch

    if VARIANT == "ian":
        model_save_path = os.path.expanduser("~/navrep/models/V/vae.json")
        dataset_dir = os.path.expanduser("~/navrep/datasets/V/ian")
        log_path = os.path.expanduser("~/navrep/logs/V/vae_train_log_{}.csv".format(START_TIME))
    if VARIANT == "toy":
        model_save_path = os.path.expanduser("~/navrep/models/V/toyvae.json")
        dataset_dir = os.path.expanduser("~/navrep/datasets/V/toy")
        log_path = os.path.expanduser("~/navrep/logs/V/toyvae_train_log_{}.csv".format(START_TIME))
    if VARIANT == "markone":
        model_save_path = os.path.expanduser("~/navrep/models/V/markonevae.json")
        dataset_dir = os.path.expanduser("~/navrep/datasets/V/markone")
        log_path = os.path.expanduser("~/navrep/logs/V/markonevae_train_log_{}.csv".format(START_TIME))
    if VARIANT == "marktwo":
        model_save_path = os.path.expanduser("~/navrep/models/V/marktwovae.json")
        dataset_dir = os.path.expanduser("~/navrep/datasets/V/marktwo")
        log_path = os.path.expanduser("~/navrep/logs/V/marktwovae_train_log_{}.csv".format(START_TIME))
    if VARIANT == "navreptrain":
        model_save_path = os.path.expanduser("~/navrep/models/V/navreptrainvae.json")
        dataset_dir = os.path.expanduser("~/navrep/datasets/V/navreptrain")
        log_path = os.path.expanduser("~/navrep/logs/V/navreptrainvae_train_log_{}.csv".format(START_TIME))
    if VARIANT == "irl":
        model_save_path = os.path.expanduser("~/navrep/models/V/irlvae.json")
        dataset_dir = os.path.expanduser("~/navrep/datasets/V/irl")
        log_path = os.path.expanduser("~/navrep/logs/V/irlvae_train_log_{}.csv".format(START_TIME))

    if common_args.dry_run:
        model_save_path = model_save_path.replace(os.path.expanduser("~/navrep"), "/tmp/navrep")
        log_path = log_path.replace(os.path.expanduser("~/navrep"), "/tmp/navrep")

    make_dir_if_not_exists(os.path.dirname(model_save_path))
    make_dir_if_not_exists(os.path.dirname(log_path))

    # create network
    reset_graph()
    vae = ConvVAE(z_size=_Z, batch_size=batch_size, is_training=True, reuse=False)
    vae.print_trainable_params()

    # create training dataset
    dataset = archive_to_lidar_dataset(dataset_dir)
    if len(dataset) == 0:
        raise ValueError("no scans found, exiting")
    print(len(dataset), "scans in dataset.")

    # split into batches:
    total_length = len(dataset)
    num_batches = int(np.floor(total_length / batch_size))

    # rings converter
    rings_def = generate_rings(64, 64)

    # train loop:
    print("train", "step", "loss", "recon_loss", "kl_loss")
    values_logs = None
    start = time.time()
    for epoch in range(NUM_EPOCH):
        np.random.shuffle(dataset)
        for idx in range(num_batches):
            batch = dataset[idx * batch_size : (idx + 1) * batch_size]
            scans = batch

            obs = (
                rings_def["lidar_to_rings"](scans).astype(float)
                / rings_def["rings_to_bool"]
            )
            # remove "too close" points
            obs[:, :, 0, :] = 0.0

            feed = {
                vae.x: obs,
            }

            (train_loss, r_loss, kl_loss, train_step, _) = vae.sess.run(
                [vae.loss, vae.r_loss, vae.kl_loss, vae.global_step, vae.train_op], feed
            )

            if (train_step + 1) % 500 == 0:
                if common_args.render:
                    from matplotlib import pyplot as plt

                    #           plt.ion()
                    plt.figure("training_status")
                    plt.clf()
                    plt.suptitle("training step {}".format(train_step))
                    f, (ax1, ax2) = plt.subplots(2, 1, num="training_status")
                    ax1.imshow(obs[0, :, :, 0], cmap=plt.cm.Greys)
                    ax2.imshow(vae.encode_decode(obs)[0, :, :, 0], cmap=plt.cm.Greys)
                    plt.savefig("/tmp/vae_step{:07}.png".format(train_step))
                #           plt.pause(0.01)
                print("step", (train_step + 1), train_loss, r_loss, kl_loss)
                vae.save_json(model_save_path)
                # log
                end = time.time()
                time_taken = end - start
                start = time.time()
                values_log = pd.DataFrame(
                    [[train_step, train_loss, r_loss, kl_loss, time_taken]],
                    columns=["step", "cost", "rec_cost", "kl_cost", "train_time_taken"],
                )
                if values_logs is None:
                    values_logs = values_log.copy()
                else:
                    values_logs = values_logs.append(values_log, ignore_index=True)
                values_logs.to_csv(log_path)

            if MAX_STEPS is not None:
                if train_step > MAX_STEPS:
                    break
        if MAX_STEPS is not None:
            if train_step > MAX_STEPS:
                break

    # finished, final model:
    vae.save_json(model_save_path)

"""
Initial demonstration pipeline.

Mostly for development purposes but also to show a representative example of how the VTF calibration
will run.
"""

import glob
import datetime as dt
from os.path import join
from commands.align_frames import align_frames
from commands.dark_correct import correct_darks
from commands.flat_correct import correct_flats
from commands.reduce_darks import reduce_darks
from commands.reduce_flats import reduce_flats
from commands.reduce_targets import reduce_targets

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from preprocess_data import process

DATA = join("/", "home", "drew", "DKIST", "vtfcal", "vtfcal", "data")

default_args = {"owner": "airflow", "depends_on_past": False, "start_date": dt.datetime.now()}

dag = DAG("pipeline-demo", default_args=default_args, schedule_interval="@once")
data_tree = join(DATA, "{}_data_tree")


def null():
    """Null function so I've got a thing to pass to bits of the pipeline I haven't written yet"""
    return


preprocess = PythonOperator(
    task_id="Pre-process-data", python_callable=process, op_args=["00000000"], dag=dag
)

"""
Data reduction tasks
"""
# Dark reduction
# --------------
bb_dark_reduction = PythonOperator(
    task_id="Reduce-broadband-darks",
    python_callable=reduce_darks,
    op_args=[data_tree.format("bb")],
    dag=dag,
)

nb1_dark_reduction = PythonOperator(
    task_id="Reduce-narrowband-1-darks",
    python_callable=reduce_darks,
    op_args=[data_tree.format("nb1")],
    dag=dag,
)

nb2_dark_reduction = PythonOperator(
    task_id="Reduce-narrowband-2-darks",
    python_callable=reduce_darks,
    op_args=[data_tree.format("nb2")],
    dag=dag,
)

# Flat reduction
# --------------
bb_flat_reduction = PythonOperator(
    task_id="Reduce-broadband-flats",
    python_callable=reduce_flats,
    op_args=[data_tree.format("bb")],
    dag=dag,
)
bb_dark_reduction >> bb_flat_reduction

nb1_flat_reduction = PythonOperator(
    task_id="Reduce-narrowband-1-flats",
    python_callable=reduce_flats,
    op_args=[data_tree.format("nb1")],
    dag=dag,
)
nb1_dark_reduction >> nb1_flat_reduction

nb2_flat_reduction = PythonOperator(
    task_id="Reduce-narrowband-2-flats",
    python_callable=reduce_flats,
    op_args=[data_tree.format("nb2")],
    dag=dag,
)
nb2_dark_reduction >> nb2_flat_reduction

# Target reduction
# ----------------
target_reduction = PythonOperator(
    task_id="Correct-and-reduce-targets",
    python_callable=reduce_targets,
    op_args=[glob.glob(data_tree.format("*"))],
    dag=dag,
)

# Prefilter reduction
# -------------------
prefil_red = PythonOperator(task_id="Reduce-prefilter", python_callable=null, dag=dag)

# Polarimetric calibration
# ------------------------
polcal = PythonOperator(task_id="Polarisation-calibration", python_callable=null, dag=dag)


"""
Data correction tasks
"""
dark_correction_bb = PythonOperator(
    task_id="Dark-correct-broadband-data",
    python_callable=correct_darks,
    op_args=[data_tree.format("bb")],
    dag=dag,
)

dark_correction_nb1 = PythonOperator(
    task_id="Dark-correct-narrowband1-data",
    python_callable=correct_darks,
    op_args=[data_tree.format("nb1")],
    dag=dag,
)

dark_correction_nb2 = PythonOperator(
    task_id="Dark-correct-narrowband2-data",
    python_callable=correct_darks,
    op_args=[data_tree.format("nb2")],
    dag=dag,
)

bb_dark_reduction >> dark_correction_bb
nb1_dark_reduction >> dark_correction_nb1
nb2_dark_reduction >> dark_correction_nb2

flat_correction_bb = PythonOperator(
    task_id="Flat-correct-broadband-data",
    python_callable=correct_flats,
    op_args=[data_tree.format("bb")],
    dag=dag,
)

flat_correction_nb1 = PythonOperator(
    task_id="Flat-correct-narrowband1-data",
    python_callable=correct_flats,
    op_args=[data_tree.format("nb1")],
    dag=dag,
)

flat_correction_nb2 = PythonOperator(
    task_id="Flat-correct-narrowband2-data",
    python_callable=correct_flats,
    op_args=[data_tree.format("nb2")],
    dag=dag,
)

(bb_flat_reduction, dark_correction_bb) >> flat_correction_bb
(nb1_flat_reduction, dark_correction_nb1) >> flat_correction_nb1
(nb2_flat_reduction, dark_correction_nb2) >> flat_correction_nb2

"""
Reconstruction tasks
"""
data_alignment1 = PythonOperator(
    task_id="Align-narrowband1-data",
    python_callable=align_frames,
    op_args=[data_tree.format("nb1")],
    dag=dag,
)

data_alignment2 = PythonOperator(
    task_id="Align-narrowband2-data",
    python_callable=align_frames,
    op_args=[data_tree.format("nb2")],
    dag=dag,
)

(target_reduction, flat_correction_nb1) >> data_alignment1
(target_reduction, flat_correction_nb2) >> data_alignment2

recon_bb = PythonOperator(task_id="reconstruct-broadband", python_callable=null, dag=dag)

recon_nb1 = PythonOperator(task_id="reconstruct-narrowband-1", python_callable=null, dag=dag)

recon_nb2 = PythonOperator(task_id="reconstruct-narrowband-2", python_callable=null, dag=dag)

(recon_bb, data_alignment1) >> recon_nb1
(recon_bb, data_alignment2) >> recon_nb2


# """
# Calibration tasks
# """
# prefil_cal = PythonOperator(task_id="correct-for-prefilter", bash_command="", dag=dag)

# (prefil_red, recon_nb1, recon_nb2) >> prefil_cal

# align2 = PythonOperator(task_id="realign-channels", bash_command="", dag=dag)

# prefil_cal >> align2

# wlshift = PythonOperator(task_id="correct-for-wavelength-shift", bash_command="", dag=dag)
# align2 >> wlshift


# """
# Science processing tasks
# """
# demod = PythonOperator(task_id="demodulate-pol-states", bash_command="", dag=dag)

# (wlshift, polcal) >> demod

# tmatrix = PythonOperator(task_id="correct-for-tmatrix", bash_command="", dag=dag)

# demod >> tmatrix

# crosstalk = PythonOperator(task_id="correct-for-crosstalk", bash_command="", dag=dag)

# tmatrix >> crosstalk

# combine = PythonOperator(task_id="combine-narrowbands", bash_command="", dag=dag)

# crosstalk >> combine

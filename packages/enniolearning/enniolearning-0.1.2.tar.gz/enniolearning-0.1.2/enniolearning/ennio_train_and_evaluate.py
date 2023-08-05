from jordan_py import jordan
from enniolearning import ennio_models_evaluation, ennio_training
from music21.instrument import *
from matplotlib import pyplot as plt
from datetime import date

test_name = 'The Nightmare Before Christmas'
dump_path = f"../data/midi_songs/{test_name}"
nb_epochs = 300
# resume_from = 69
lrs = [1e-5]

do_training = True
do_eval = True

# jordan instance
JORDAN_SERVER_BASE_URL = 'http://192.168.1.41:5000/jordan/'
jordan_instance = None
try:
    jordan_instance = jordan.register(JORDAN_SERVER_BASE_URL, client_name=f" {date.today()} Train {test_name} {nb_epochs}ep")
except Exception as network_error:
    print('Could not register to Jordan server', str(network_error))

try:

    if do_training:
        ennio_training.train(test_name,
                             nb_epochs,
                             lrs,
                             dump_path=dump_path,
                             midi_files_path=f"{dump_path}/*.m*",
                             force_reload_dataset=True,
                             skip_percussion=True, skip_vocal=True, include_type_list=[],
                             skip_type_list=[Recorder],
                             plot_result=True,
                             jordan_instance=jordan_instance
                             # resume_model=resume_from,
                             )

    if do_eval:
        ennio_models_evaluation.evaluate(test_name=test_name, exec_nb=50, learning_rates=lrs,lstm_hidden_cells_count=256,
                                         select_epochs=range(int(3 * nb_epochs / 4), nb_epochs, 1),
                                         plot_result=True, jordan_instance=jordan_instance, dump_path=dump_path)

    if jordan_instance:
        jordan_instance.unregister()

    plt.show()

except BaseException as exc:
    print('error', str(exc))
    if jordan_instance:
        jordan_instance.fatal(exc)
    raise exc


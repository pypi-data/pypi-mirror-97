from enniolearning.training_fcts import make_path
from enniolearning.prediction_fcts import evaluate_models, LEARNING_RATE, plot_model_evaluation, compute_evaluation_score, SKIP_LOSS_FUNCTION, SKIP_LEARNING_RATE, SKIP_MODEL_FILE
from jordan_py import jordan
from enniolearning.utils import log

#Parameters
hp_test_name = 'classic'
hp_exec_nb = 250  # each model will be evaluated this number of times
hp_generate_output_length = 50  # each execution will generate a socre this long
hp_loss_func_names = ['BCELoss()']  # madatory in current implem, even if a single one
hp_learning_rates = [1e-5]  # madatory in current implem, even if a single one
hp_select_epochs = range(100,120)  # optional : default is False (all models)

# weights for score calculation
diversity_rate_score_weight = 15
plagia_part_score_weight = -1
rejected_for_repetition_score_weight = -5
post_processing_score_weight = 1 # ratio [0,1]

def evaluate(test_name=hp_test_name, exec_nb=hp_exec_nb, loss_func_names=hp_loss_func_names, learning_rates=hp_learning_rates, select_epochs=hp_select_epochs, generate_output_length=hp_generate_output_length, plot_result=False, jordan_instance=None, **kwargs):
    jordan_evaluate_task_instance = None
    if jordan_instance:
        jordan_evaluate_actions = jordan.with_action(SKIP_LOSS_FUNCTION).with_action(SKIP_LEARNING_RATE).with_action(SKIP_MODEL_FILE).build()
        jordan_evaluate_task_instance = jordan_instance.create_task('evaluate', jordan_evaluate_actions)

    if jordan_evaluate_task_instance:
        jordan_evaluate_task_instance.send_status(f"Starting evaluation for loss={loss_func_names}, learning rates={learning_rates}, epochs={select_epochs}, output length={generate_output_length}, execution nb={exec_nb}")

    models_path = make_path(test_name, LEARNING_RATE)
    evaluation = evaluate_models(models_path, exec_nb=exec_nb, loss_func_names=loss_func_names, lrs=learning_rates, select_epochs=select_epochs, generate_output_length=generate_output_length, jordan_instance=jordan_evaluate_task_instance, **kwargs)

    best_model, best_score = compute_evaluation_score(evaluation,
                                                      ['diversity_rate', 'plagia_part', 'rejected_for_repetition', 'post_processing_score'],
                                                      [diversity_rate_score_weight, plagia_part_score_weight, rejected_for_repetition_score_weight, post_processing_score_weight])
    if jordan_evaluate_task_instance:
        jordan_evaluate_task_instance.send_success_status(f"Best model found = {best_model}")
        jordan_evaluate_task_instance.complete()

    log(f"best model:  {best_model}", **kwargs)

    if plot_result:
        plot_model_evaluation(evaluation, 'diversity_rate', **kwargs)
        plot_model_evaluation(evaluation, 'plagia_part', **kwargs)
        plot_model_evaluation(evaluation, 'rejected_for_repetition', **kwargs)
        plot_model_evaluation(evaluation, 'post_processing_score', **kwargs)
        plot_model_evaluation(evaluation, 'score', **kwargs)
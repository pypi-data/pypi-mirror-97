# Ennio-Learning
Ennio is a machine learning program.
It takes musics in MID format to learn a theme.
Themes are collections of datasets (collection of MID files) having common features, for example :
- Heroic fantasy
- Thriller
- Horror
- Suspense
- Classic
- Manga
- etc.

Once learning (training) for one theme is done, the model (network weights) is serialized and can be reused for later music generation.
Such models are used for instance in [Ennio app project](https://github.com/Mara-tech/Ennio).

### Training features
Ennio Learning handles [Jordan](https://github.com/Mara-tech/jordan) features during training and model evaluation. As these are long processes, Jordan app gives remote access to logs (and ETA), and some control over loops. For example, one may skip a training task if it is not going to be efficient (loss is not decreasing).

### Logging
A default logger exists, at level `logging.INFO`. You may adjust this level by calling

    import logging
    from enniolearning.utils import set_default_logger_level
    
    set_default_logger_level(logging.DEBUG)
        
You can also provide your own logger (defined from [logging library](https://docs.python.org/3/howto/logging.html))
by passing `logger` argument. For example :

    import logging, logging.config
    logging.config.fileConfig('logging.yml')
    logger_from_config = logging.getLogger('simpleExample')
    
    from ennio_training import train
    train(logger=logger_from_config)
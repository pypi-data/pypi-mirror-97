import logging
import click
import docker

logger=logging.getLogger('mldock')

def compute_progress(current, max_value=10):

    if current > max_value:
        multiple = current // max_value
        current = current - max_value * multiple 
    
    return current

def get_layer_state(stream, layer_id, state={}, fill_char='#', increment=5, max_value=20):
    """
        Computes a status update to the state of layer during a push.
        Additionally, adds a progress bar and flexible fill character.
    """
    _progress = ''
    try:
        current_layer = state[layer_id]

        if stream.lower() == 'pushing':
            current_progress = len(current_layer['progress'])
            _progress = compute_progress(current_progress, max_value=max_value) + increment
            _progress = fill_char * _progress


        state.update(
            {layer_id: {'msg':stream, 'progress': _progress}}
        )
    except KeyError as exception:
        state.update(
            {layer_id: {'msg':stream, 'progress': _progress}}
        )
    return state

def stateful_log_emitter(line: dict, state={}):
    error = line.get('error', None)
    errorDetail = line.get('errorDetail', None)
    if error is not None:
        logger.error('{}\n{}'.format(error, errorDetail))
    
    stream = line.get('status','')
    layer_id = line.get('id','')

    if (layer_id == ''):
        return state
    else:
        # perform status update, using layer_id as key
        state = get_layer_state(stream, layer_id, state)

        # clear terminal to allow for friendlier update
        click.clear()

        # emit current state to stdout
        {logger.info("{}: {} {}".format(k,v['msg'], v['progress'])) for k, v in state.items()}

    return state

def push_image_to_repository(
    image_repository: str,
    auth_config: dict,
    tag='latest'
):
    """
        Push image to cloud repository. Using auth_config this will Authenticate client.
    """
    client = docker.from_env()
    states = {}
    push_response = client.images.push(
        repository=image_repository,
        tag=tag,
        stream=True,
        decode=True,
        auth_config=auth_config
    )

    for line in push_response:
        states = stateful_log_emitter(line, states)

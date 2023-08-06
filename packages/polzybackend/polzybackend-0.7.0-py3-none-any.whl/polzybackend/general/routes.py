from flask import jsonify, request, current_app
from polzybackend.general import bp
from polzybackend.utils.import_utils import all_stages
from polzybackend import auth, models
from datetime import datetime
import os
from uuid import uuid4

@bp.route('/stages')
def stages():
    #
    # returns list of all available stages for login
    #

    try:
        # get all stages
        stages = all_stages()()
        current_app.logger.debug(f"Value of stages: {stages}")

    except Exception as e:
        current_app.logger.warning(f'Failed to get All Stages: {e}')
        stages = []

    return jsonify(stages), 200


@bp.route('/values', methods=['POST'])
@auth.login_required
def values():
    #
    # returns value list
    #

    # get post data
    data = request.get_json()

    try:
        # get parent instance from app store
        # try policies first
        instance = current_app.config['ANTRAGS'].get(data['instanceId'])
        if instance is None:
            # try antrags then
            instance = current_app.config['POLICIES'].get(data['instanceId'])
            if instance is None:
                raise Exception(f'Instance of with id {data["instanceId"]} not found in PoLZy storage. Most probably app restarted.')

        # get value list
        result = instance.getValueList(data.get('valueListName'))
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.exception(f'Faild to get value-list for paylod {data}\n{e}')
    
    return jsonify({'error': f'Failed to get value-list'}), 400


@bp.route('/upload', methods=['POST'])
@auth.login_required
def upload():
    # get file
    file = request.files.get('file')
    print('\n*** File Upload:')
    print(file)
    if file is None:
        return jsonify({'error': 'Request does not contain dataFile'}), 400

    # save file
    try:
        user = auth.current_user()
        #filename = '.'.join((
        #    '_'.join((
        #        user.id,
        #        user.company_id,
        #        datetime.now().strftime("%Y%m%d_%H%M%S"),
        #    )),
        #    file.filename.split('.')[-1],
        #))
        filename_parts = (str(uuid4()), file.filename.split('.')[-1])
        path_to_file = os.path.join(current_app.config['UPLOADS'], '.'.join(filename_parts))
        print(path_to_file)
        file.save(path_to_file)
        # create file instance in db
        file_db = models.File.new(
            user=auth.current_user(),
            id=filename_parts[0],
            filename=file.filename,
        )
        return {'OK': f'File {file_db.filename} saved with id {file_db.id}'}, 200
    except Exception as error:
        current_app.logger.error(f'Failed to upload file "{file.filename}" by {user}: {error}.')
        return jsonify({'error': 'File upload failed'}), 400
    

from flask import jsonify, request, current_app, send_file, abort
from polzybackend.antrag import bp
from polzybackend.utils.import_utils import antrag_products, antrag_class
from polzybackend import auth
from polzybackend.models import AntragActivityRecords
from polzybackend.utils.import_utils import import_class
import json

@bp.route('/antrag/products')
@auth.login_required
def get_antrag_products():
    #
    # returns all products that available for current user
    #
    try:
        # get all stages
        product_list = antrag_products().getAllAvailableProducts(auth.current_user())
        return jsonify(product_list), 200

    except Exception as e:
        current_app.logger.exception(f"Error during get_antrag_products: {e}")
        
    return jsonify({'error': f'Failed to get antrag products'}), 400


@bp.route('/antrag/new/<string:product_type>')
@auth.login_required
def new_antrag(product_type):
    #
    # creates an Antrag by product_type
    # and returns it to frontend
    #
    try:
        antrag = antrag_class()(product_type, auth.current_user())

        # store antrag and return it to store and return json object
        antrag.initialize()
        current_app.config['ANTRAGS'][antrag.id] = antrag
        result = antrag.get()
        return jsonify(result), 200

    except Exception as e:
        current_app.logger.exception(f'Initialization of antrag instance {product_type} failed: {e}')

    return jsonify({'error': f'Initialization of antrag instance failed'}), 400


@bp.route('/antrag/clone/<string:id>')
@auth.login_required
def clone_antrag(id):
    #
    # clone antrag instance by id
    #

    try:
        # get antrag from app store
        antrag_src = current_app.config['ANTRAGS'].get(id)
        if antrag_src is None:
            raise Exception(f'Antrag {id} not found')

        # make copy and return antrag json object
        antrag = antrag_src.clone()
        current_app.config['ANTRAGS'][antrag.id] = antrag
        result = antrag.get()
        return jsonify(result), 200

    except Exception as e:
        current_app.logger.warning(f'Cloning of antrag {id} failed: {e}')
    
    return jsonify({'error': f'Cloning of antrag instance failed'}), 400


@bp.route('/antrag/tag/<string:antrag_id>', methods=['POST', 'DELETE'])
@auth.login_required
def antrag_tag(antrag_id):
    #
    # set or delete custom tag of antrag
    #

    # get antrag from app store
    antrag = current_app.config['ANTRAGS'].get(antrag_id)
    if antrag is None:
        current_app.logger.warning(f'Antrag {antrag_id} is absent in PoLZy storage. Most probably instance restarted.')
        return jsonify({'error': f'Antrag instance not found'}), 400

    # update tag
    if request.method == 'POST':
        # get tag from payload
        tag = request.get_json().get('tag')
        if tag:
            antrag.instance.setCustomTag(tag)
            return {'OK': 'Custom Tag successfully set'}, 200

    # delete tag
    antrag.instance.setCustomTag(None)
    return {'OK': 'Custom Tag successfully deleted'}, 200


@bp.route('/antrag/update', methods=['POST'])
@auth.login_required
def update_antrag():
    #
    # updates antrag fields
    #

    # get post data
    data = request.get_json()

    # get antrag and update its values
    try:
        # get antrag from app store
        antrag = current_app.config['ANTRAGS'].get(data['id'])
        if antrag is None:
            raise Exception(f'Antrag {data["id"]} is absent in PoLZy storage. Most probably instance restarted.')

        # update antrag values and return antrag json object
        antrag.updateFields(data)
        result = antrag.get()
        return jsonify(result), 200

    except Exception as e:
        current_app.logger.exception(f'Antrag {data["id"]}, fields update failed: {e}')
    
    return jsonify({'error': f'Update of the antrag fields failed'}), 400


@bp.route('/antrag/execute', methods=['POST'])
@auth.login_required
def execute_antrag():
    #
    # executes antrag activities
    #

    # get post data
    data = request.get_json()

    # get antrag and execute activity
    try:
        # get antrag from app store
        antrag = current_app.config['ANTRAGS'].get(data['id'])
        if antrag is None:
            raise Exception(f'Antrag {data["id"]} is absent in PoLZy storage. Most probably instance restarted.')

        # execute antrag activity and return the response object
        result = antrag.executeActivity(data)
        return jsonify(result), 200

    except Exception as e:
        current_app.logger.exception(f'Failed execute activity {data.get("activity")} of antrag {data["id"]}: {e}')
    
    return jsonify({'error': f'Execution of antrag activiy {data.get("activity")} failed'}), 400



@bp.route('/antrag/records/search', methods=['POST'])
@auth.login_required
def getSearchStringFromRecords():
    data = request.get_json()

    # supplying current user to get records of current user & company
    found_antrags = AntragActivityRecords.getSearchString(auth.current_user(), data.get("value"))
    results = [{
        'id': instance.antrag_id,
        'label': instance.get_label(),  # 'get_label' method should be adjusted to proper render results
    } for instance in found_antrags] if found_antrags else []
    #results = [instance.to_dict() for instance in found_antrags] if found_antrags else []
    #result = {"results": []}
    #if results:
    #    result = {"results": [instance.to_dict() for instance in results]}

    return jsonify(results), 200

# we have to pass only antrag id. it will be easier to use GET method
@bp.route('/antrag/records/<string:antrag_id>')#load', methods=['POST'])
@auth.login_required
def loadLatestRecords(antrag_id):
    #data = request.get_json()
    #result = AntragActivityRecords.getLatest(data.get("antrag_id") or data.get("id"))  # flexible to get from both ids
    #class_ = import_class(current_app.config.get('DATACLASSES') + (f".{result.class_name}" * 2))
    #instance = class_(auth.current_user(), result.sapClient)  # creating class instance of Antrag

    # get antrag record by id
    antrag_record = AntragActivityRecords.getLatest(antrag_id)
    if antrag_record is None:
        return {'error': f'No record found of antrag {antrag_id}'}, 404

    # create antrag instance from the record
    antrag = antrag_class()(antrag_record.class_name, auth.current_user())

    # load antrag instance and store it within the app
    antrag.load(antrag_record.sapClient)
    current_app.config['ANTRAGS'][antrag.id] = antrag

    # creating dictionary with name as key and value as value of inputField. These are used to load fields.
    #formatValue = lambda item: int(item) if item and item.isdigit() else item # format int values
    dic = {js.get("name"): js.get("valueChosenOrEntered") for js in json.loads(antrag_record.json_data)}
    #instance.updateFieldValues(dic)  # loading above created dic to instance
    #return jsonify(result.to_dict()), 200

    # update field values from the record and return the result
    antrag.instance.id = antrag_record.antrag_id  # using same antrag_id as from record to avoid new record because of
    antrag.instance.updateFieldValues(dic)                                                            ## new antrag id
    antrag.instance.status = antrag_record.status
    antrag.instance.loadActivitiesFromDict(json.loads(antrag_record.json_data_activities))
    # update tag
    antrag.instance.setCustomTag(antrag_record.tag)
    result = antrag.get()
    return jsonify(result), 200


import dateutil.parser
from flask import request
from flask_restplus import Resource
from .. import socketio
from ..service.user_service import get_stats_by_user
from ..util.dto import MinerDto
from ..service.miner_service import (
    create_new_miner,
    get_all_miners,
    get_miner,
    get_healths_by_miner,
    get_shares_by_miner,
)
from ..service.user_service import (
    get_user_by_username,
    get_user_by_id
)
from ..service import update, delete
from ..util.decorators import token_required, api_token_required
from flask_socketio import SocketIO, emit

api = MinerDto.namespace
_miner = MinerDto.miner
_health = MinerDto.health
_health_aggregate = MinerDto.health_aggregate
_share = MinerDto.share
_share_aggregate = MinerDto.share_aggregate
stats_schema = MinerDto.StatsQuerySchema()


@api.route('/')
@api.response(201, 'Miner successfully created.')
@api.doc('create a new miner')
@api.expect(_miner, validate=True)
class Miner(Resource):
    @api_token_required
    def post(self):
        """Creates a new Miner """
        data = request.json
        return create_new_miner(data)

    @api_token_required
    def put(self):
        """Updates a User's miner """
        miner_id = request.json.get('miner_id')
        miner = get_miner(miner_id)
        if not miner:
            api.abort(404)
        else:
            data = request.json
            return update(miner, data)


@api.route('/<user_id>/')
@api.param('user_id', "User's id")
@api.response(404, 'No User with that id.')
class MinerList(Resource):
    @api.doc('list_of_miners_owned_by_this_user')
    @api.marshal_list_with(_miner, envelope='data')
    # TODO: remove before prod
    # @token_required
    def get(self, user_id):
        """List all miners owned by this user"""
        user = get_user_by_id(user_id=user_id)
        return get_all_miners(user)


@api.route('/<username>/<miner_id>')
@api.param('username', "User's username")
@api.param('miner_id', "The miner's id")
@api.response(404, 'No User/Miner with that id.')
class UserMiner(Resource):
    @api.response(200, 'Miner successfully deleted.')
    @api.doc("delete a user's miner")
    @token_required
    def delete(self, username, miner_id):
        """ Delete a user's miner """
        miner = get_miner(miner_id)
        if not miner:
            api.abort(404)
        else:
            return delete(miner)


@api.route('/<miner_id>/health')
@api.param('miner_id', "The miner's id")
@api.response(404, 'No User/Miner with that id.')
class MinerHealths(Resource):
    # TODO: add default limits ^
    @api.param('end', "Optional time after which to retrieve stats")
    @api.param('start', "Optional time before which to retrieve stats")
    @api.marshal_list_with(_health_aggregate)
    # TODO: resecure before full prod deploy
    # @token_required
    def get(self, miner_id):
        """ Get a miner's temp, hashrate and power usage by gpu. Not specifying start or end will return the past 12 hrs of stats """
        miner = get_miner(miner_id)
        if not miner:
            api.abort(404)
        else:
            """validate the query params"""
            start = request.args.get('start')
            end = request.args.get('end')
            res = request.args.get('resolution')

            start_dt = None
            end_dt = None
            if start:
                start_dt = dateutil.parser.parse(start)
            if end:
                end_dt = dateutil.parser.parse(end)
            if res:
                res = int(res)

            # errors = stats_schema.validate(start_dt, end_dt)
            # if errors:
            #    api.abort(400, error="Start/end datetime param improperly formatted")

        return get_healths_by_miner(miner,
                                    start_dt,
                                    end_dt,
                                    res)


@api.route('/<miner_id>/share')
@api.param('miner_id', "The miner's id")
@api.response(404, 'No Miner with that id.')
class MinerShares(Resource):
    # TODO: add default limits ^
    @api.param('end', "Optional time after which to retrieve stats")
    @api.param('start', "Optional time before which to retrieve stats")
    @api.param('resolution', "Optional resolution of time aggregation in seconds")
    @api.marshal_list_with(_share_aggregate)
    # TODO: resecure before full prod deploy
    # @token_required
    def get(self, miner_id):
        """ Get a miners shares by gpu. Not specifying start or end will return the past 7 days of stats """
        miner = get_miner(miner_id)
        if not miner:
            api.abort(404)
        else:
            """validate the query params"""
            start = request.args.get('start')
            end = request.args.get('end')
            res = request.args.get('resolution')

            start_dt = None
            end_dt = None
            if start:
                start_dt = dateutil.parser.parse(start)
            if end:
                end_dt = dateutil.parser.parse(end)
            if res:
                res = int(res)

            # errors = stats_schema.validate(start_dt, end_dt)
            # if errors:
            #    api.abort(400, error="Start/end datetime param improperly formatted")

        return get_shares_by_miner(miner,
                                   start_dt,
                                   end_dt,
                                   res)

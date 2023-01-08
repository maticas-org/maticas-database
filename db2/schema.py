# db2/schema.py

import graphene
from utilities              import *
from graphene               import relay
from graphene_sqlalchemy    import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models                 import (db_session, 
                                    User as UserModel, 
                                    Variable as VariableModel, 
                                    Measurement as MeasurementModel)

#----------------------------------------------------------------------------#
#--------------------------------    Queries   ------------------------------#
#----------------------------------------------------------------------------#

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

class Variable(SQLAlchemyObjectType):
    class Meta:
        model = VariableModel
        interfaces = (relay.Node,)

class Measurement(SQLAlchemyObjectType):
    class Meta:
        model = MeasurementModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    #----------------------------------------------------#
    #------------ queries for the graphene schema -------#
    #----------------------------------------------------#

    variables    = graphene.List(Variable)
    measurements = graphene.List(Measurement,
                                 api_key = graphene.String(description = "The user's api_key."),
                                 nmeasurements = graphene.Int(description = "The number of measurements to return. Default 100. If \
                                                              start_time and end_time are specified, this parameter is ignored. If \
                                                              no start_time and end_time are specified, it will return the last \
                                                              nmeasurements."),

                                 start_time = graphene.String(description = "The start time of the interval to return data. \
                                                                             If only start_time is specified, it will return \
                                                                             data from start_time to the present.\
                                                                             format YYYY-MM-DD HH:MM:SS"),

                                 end_time = graphene.String(description = "The end time of the interval to return data. \
                                                                             If only end_time is specified, it will return \
                                                                             data from the beginning to end_time.\
                                                                            format YYYY-MM-DD HH:MM:SS"),

                                 description = "Returns a list of measurements for a given user.")
    log_in = graphene.Field(graphene.String,
                            username = graphene.String(description = "The user's username."),
                            password = graphene.String(description = "The user's password."),
                            description = "Logs in a user and returns the user's api_key, and ok status.")




    #----------------------------------------------------#
    #----------- resolve methods for queries ------------#
    #----------------------------------------------------#

    def resolve_variables(self, info):
        query = Variable.get_query(info)
        return query.all()


    def resolve_measurements(self, info,
                             api_key: str,
                             nmeasurements = 100,
                             start_time = None,
                             end_time = None):
    
        query_meas = Measurement.get_query(info)
        query_user = User.get_query(info)
        user = query_user.filter(UserModel.api_key == api_key).first()

        if user is None:
            return None
        else:
            user_id = user.id
            measurements = query_meas.filter(MeasurementModel.user_id == user_id)

        no_start_time = ((start_time is None) or (start_time == ""))
        no_end_time = ((end_time is None) or (end_time == ""))

        # if no end time and no start time, then the last nmeasurements will be sent
        if (no_start_time and no_end_time):
            return measurements.order_by(MeasurementModel.time.desc()).limit(nmeasurements).all()

        # if only start_time is provided, then retrieves all the data starting from start_time 
        elif (no_end_time):
            start_time = toDateTime(start_time)
            return measurements.filter(MeasurementModel.time >= start_time).order_by(MeasurementModel.time.desc()).all()

        # if only end_time is provided, then retrieves all the data until end_time
        elif (no_start_time):
            end_time = toDateTime(end_time)
            return measurements.filter(MeasurementModel.time <= end_time).order_by(MeasurementModel.time.desc()).all()

        # if both start_time and end_time are provided, then returns all the data between that timespan
        else:
            start_time = toDateTime(start_time)
            end_time = toDateTime(end_time)
            return measurements.filter(MeasurementModel.time >= start_time, MeasurementModel.time <= end_time).order_by(MeasurementModel.time.desc()).all()


    def resolve_log_in(self, info, username: str, password: str) -> str:
        query = User.get_query(info)
        hashed_password = hash_password(password)

        #filters where username and password match
        user = query.filter(UserModel.username == username, UserModel.password == hashed_password).first()

        if user is None:
            return None
        else:
            return user.api_key


#----------------------------------------------------------------------------#
#--------------------------------   Mutations  ------------------------------#
#----------------------------------------------------------------------------#

# mutations: https://www.youtube.com/watch?v=pI5IBcXf8Qk 

class SignUp(graphene.Mutation):
    class Arguments:
        username = graphene.String(required = True)
        email    = graphene.String(required = True)
        password = graphene.String(required = True)

    #output fields, of the output when resolved
    ok = graphene.Boolean()

    def mutate(root, info, username, email, password):

        time_now = now()
        password = hash_password(password)
        api_key  = generate_api_key(username = username, 
                                    password = password,
                                    email    = email)

        newuser  = UserModel(username = username, 
                             email    = email, 
                             api_key  = api_key,
                             password = password,
                             time_created = time_now) 
        db_session.add(newuser)
        db_session.commit()

        return SignUp(ok = True)

class Mutation(graphene.ObjectType):
    sign_up = SignUp.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)




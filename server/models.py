from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask import abort

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ( '-signups.activity' )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column( db.DateTime, server_default=db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

    signups = db.relationship( 'Signup', backref = 'activity' )
    campers = association_proxy( 'signups', 'camper' )

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ( '-activity.campers', 'signups' )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column( db.DateTime, server_default=db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

    signups = db.relationship( 'Signup', backref = 'camper' )
    activities = association_proxy( 'signups', 'activity' )

    @validates( 'name' )
    def validate_name( self, key, name ):
        if isinstance( name, str ) and name:
            return name
        else:
            abort( 422, "Campers must have a name that is a string.")
    
    @validates( 'age' )
    def validate_age( self, key, age ):
        if isinstance( age, int ) and 8 <= age <= 18:
            return age
        else:
            abort( 422, "Age must be a number between 8 & 18." )

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'
    
class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    serialize_rules = ( 'activity.signups' )

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column( db.Integer )
    created_at = db.Column( db.DateTime, server_default=db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

    camper_id = db.Column( db.Integer, db.ForeignKey( 'campers.id' ) )
    activity_id = db.Column( db.Integer, db.ForeignKey( 'activities.id' ) )

    @validates( 'time' )
    def validate_time( self, key, time ):
        if isinstance( time, int ) and time <= 23:
            return time
        else:
            abort( 422, "Time must be a number smaller than 24." )

    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need. 






























# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin
# from flask import abort


# convention = {
#   "ix": "ix_%(column_0_label)s",
#   "uq": "uq_%(table_name)s_%(column_0_name)s",
#   "ck": "ck_%(table_name)s_%(constraint_name)s",
#   "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#   "pk": "pk_%(table_name)s"
# }

# metadata = MetaData(naming_convention=convention)

# db = SQLAlchemy(metadata=metadata)

# class Activity(db.Model, SerializerMixin):
#     __tablename__ = 'activities'

#     serialize_rules = ( '-signups.activity' )

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     difficulty = db.Column(db.Integer)
#     created_at = db.Column( db.DateTime, server_default=db.func.now() )
#     updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

#     signups = db.relationship( 'Signup', backref = "activity" )
#     campers = association_proxy( 'signups', 'camper' )

#     def __repr__(self):
#         return f'<Activity {self.id}: {self.name}>'

# class Camper(db.Model, SerializerMixin):
#     __tablename__ = 'campers'

#     serialize_rules = ( '-activity.campers', 'signups' )

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     age = db.Column(db.Integer)
#     created_at = db.Column( db.DateTime, server_default=db.func.now() )
#     updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

#     signups = db.relationship( 'Signup', backref = "camper" )
#     activities = association_proxy( 'signups', 'activity' )

#     @validates( 'name' )
#     def validate_name( self, key, name ):
#         if type( name ) is str and name:
#             return name
#         else: 
#             abort( 422, "Campers must have a name." )

#     @validates( 'age' )
#     def validate_age( self, key, age ):
#         if isinstance( age, int ) and 8 <= age <= 18:
#             return age
#         else:
#             abort( 422, "Age must be a number between 8 & 18." )

#     def __repr__(self):
#         return f'<Camper {self.id}: {self.name}>'
    
# class Signup(db.Model, SerializerMixin):
#     __tablename__ = 'signups'

#     serialize_rules = ( '-activity.signups' )

#     id = db.Column(db.Integer, primary_key=True)
#     time = db.Column( db.Integer )
#     created_at = db.Column( db.DateTime, server_default=db.func.now() )
#     updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

#     camper_id = db.Column( db.Integer, db.ForeignKey( 'campers.id' ) )
#     activity_id = db.Column( db.Integer, db.ForeignKey( 'activities.id' ) )

#     @validates( 'time' )
#     def validate_time( self, key, time ):
#         if isinstance( time, int ) and time <= 23:
#             return time
#         else:
#             abort( 422, "Time must be a number 23 or lower." )

#     def __repr__(self):
#         return f'<Signup {self.id}>'








# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin
# from flask import abort

# convention = {
#   "ix": "ix_%(column_0_label)s",
#   "uq": "uq_%(table_name)s_%(column_0_name)s",
#   "ck": "ck_%(table_name)s_%(constraint_name)s",
#   "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#   "pk": "pk_%(table_name)s"
# }

# metadata = MetaData(naming_convention=convention)

# db = SQLAlchemy(metadata=metadata)

# class Activity(db.Model, SerializerMixin):
#     __tablename__ = 'activities'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     difficulty = db.Column(db.Integer)
#     created_at = db.Column( db.DateTime, server_default=db.func.now() )
#     updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

#     def __repr__(self):
#         return f'<Activity {self.id}: {self.name}>'

# class Camper(db.Model, SerializerMixin):
#     __tablename__ = 'campers'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     age = db.Column(db.Integer)
#     created_at = db.Column( db.DateTime, server_default=db.func.now() )
#     updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

# # @validates( 'Camper' )
# # def validate_camper( self ):


#     def __repr__(self):
#         return f'<Camper {self.id}: {self.name}>'
    
# class Signup(db.Model, SerializerMixin):
#     __tablename__ = 'signups'

#     id = db.Column(db.Integer, primary_key=True)
#     time = db.Column( db.Integer )
#     created_at = db.Column( db.DateTime, server_default=db.func.now() )
#     updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

#     camper_id = db.Column( db.Integer, db.ForeignKey( 'campers.id' ))
#     activity_id = db.Column( db.Integer, db.ForeignKey( 'activities.id' ))

#     def __repr__(self):
#         return f'<Signup {self.id}>'


# # add any models you may need. 
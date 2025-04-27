from sqlalchemy.dialects.sqlite import BLOB
from database import db
from flask_sqlalchemy import SQLAlchemy

class Roles_t(db.Model):
    __tablename__ = 'Roles'
    role_id = db.Column(db.Integer(), nullable=False, autoincrement=True, primary_key=True)
    rolename = db.Column(db.String(), nullable=False)

    __table_args__ = (db.UniqueConstraint('rolename', name='uq_rolename'),)

class User_t(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.role_id'), nullable=False)
    is_flagged = db.Column(db.Boolean , default=False)
    type = db.Column(db.String(50))
    
    def get_user(username):
        if username is None:
            return User_t.query.all()
        else:
            return User_t.query.filter_by(username=username).first()
        
    def get_user_by_id(id):
        if id is None:
            return User_t.query.all()
        else:
            return User_t.query.filter_by(id=id).first()
    
    
    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'User'
    }

class Sponsor_t(User_t):
    __tablename__ = 'Sponsor'
    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    Industry = db.Column(db.String(64), nullable=False)
    Company_name = db.Column(db.String(64), nullable=False)
    Contact_name = db.Column(db.String(64), nullable=False)
    Contact_email = db.Column(db.String(64), nullable=False)
    Contact_phone = db.Column(db.String(64), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'Sponsor'
    }

    @staticmethod
    def get_sponsor(username):
        if username is None:
            return Sponsor_t.query.all()
        else:
            return Sponsor_t.query.filter_by(username=username).first()
        
class Platform_t(db.Model):
    __tablename__ = 'Platform'
    influencer_id = db.Column(db.Integer(), db.ForeignKey("Influencer.id"), nullable=False, primary_key=True)
    platform_name = db.Column(db.String(), nullable=False, primary_key=True)
    Reach = db.Column(db.Integer(), nullable=False)

    __table_args__ = (db.ForeignKeyConstraint(['influencer_id'], ['Influencer.id'], name='fk_platform_inf'),)

class Influencer_t(User_t):
    __tablename__ = 'Influencer'
    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    Contact_name = db.Column(db.String(64), nullable=False)
    Contact_email = db.Column(db.String(64), nullable=False)
    Contact_phone = db.Column(db.String(64), nullable=False)
    DOB = db.Column(db.DateTime, nullable=False)
    Niche = db.Column(db.String(64), nullable=False)
    platforms = db.relationship('Platform_t', backref='influencer', lazy=True)
    
    @staticmethod
    def get_influencer(username):
        if username is None:
            return Influencer_t.query.all()
        else:
            return Influencer_t.query.filter_by(username=username).first()
    
    __mapper_args__ = {
        'polymorphic_identity': 'Influencer'
    }

class Admin_t(User_t):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'Admin'
    }


class Campaign_t(db.Model):
    __tablename__ = 'Campaign'
    Campaign_id = db.Column(db.Integer(), nullable=False, primary_key=True, autoincrement=True)
    Sponsor_id = db.Column(db.Integer(), db.ForeignKey("Sponsor.id"), nullable=False)
    Title = db.Column(db.String())
    Desc = db.Column(db.String())
    Img = db.Column(BLOB)
    Niche = db.Column(db.String(), nullable=True)
    Status = db.Column(db.String(), nullable=False, default="created")
    date_created = db.Column(db.Date(), nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=True)
    Goal_ads = db.Column(db.Integer(), nullable=True)
    Budget = db.Column(db.Integer(), nullable=False)
    ads = db.relationship('Ad_Campaign_t', backref='campaign', lazy=True)

    @staticmethod
    def get_campaign(Campaign_id):
        if Campaign_id is None:
            return Campaign_t.query.all()
        else:
            return Campaign_t.query.filter_by(Campaign_id=Campaign_id).first()

    __table_args__ = (db.ForeignKeyConstraint(['Sponsor_id'], ['Sponsor.id'], name='fk_campaign_sponsor'),)

class Ad_Campaign_t(db.Model):
    __tablename__ = 'Ad_Campaign'
    Ad_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Campaign_id = db.Column(db.Integer(), db.ForeignKey("Campaign.Campaign_id"), nullable=False)
    Title = db.Column(db.String(), nullable=False)
    Desc = db.Column(db.String())
    Terms = db.Column(db.String())
    Status = db.Column(db.String(), nullable=False, default="created")
    Payment_amt = db.Column(db.Integer(), nullable=False)
    requests = db.relationship('Request_t', backref='Ad_Campaign', lazy=True)

    @staticmethod
    def get_ad(Ad_id):
        if Ad_id is None:
            return Ad_Campaign_t.query.all()
        else:
            return Ad_Campaign_t.query.filter_by(Ad_id=Ad_id).first()
    
    def get_adcount_by_camp(Campaign_id):
        return Ad_Campaign_t.query.filter_by(Campaign_id=Campaign_id).count()
    
    def get_ad_list_by_campaign(Campaign_id):
        return Ad_Campaign_t.query.filter_by(Campaign_id=Campaign_id)
    
    __table_args__ = (db.ForeignKeyConstraint(['Campaign_id'], ['Campaign.Campaign_id'], name='fk_ad_campaign_campaign'),)

class Ad_influencers_t(db.Model):
    __tablename__ = 'Ad_influencers'
    Ad_id = db.Column(db.Integer(), primary_key=True)
    influencer_name = db.Column(db.String(), primary_key=True)
    
    @staticmethod
    def get_ad_influencer(Ad_id):
        if Ad_id is None:
            return Ad_influencers_t.query.all()
        else:
            return Ad_influencers_t.query.filter_by(Ad_id=Ad_id)
    

class Request_t(db.Model):
    __tablename__ = 'Request'
    Req_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Ad_id = db.Column(db.Integer(), db.ForeignKey("Ad_Campaign.Ad_id"), nullable=False)
    requester_id = db.Column(db.Integer(), db.ForeignKey("User.id"), nullable=False)
    responser_id = db.Column(db.Integer(), db.ForeignKey("User.id"), nullable=False)
    Status = db.Column(db.String(), nullable=False)
    req_date = db.Column(db.Date(), nullable=False)
    payment_amt = db.Column(db.Integer(), nullable=False)
    message_req = db.Column(db.String())
    message_resp = db.Column(db.String())

    @staticmethod
    def get_request(req_id):
        if req_id is None:
            return Request_t.query.all()
        else:
            return Request_t.query.filter_by(Req_id=req_id).first()
    
    @staticmethod
    def get_requests_by_ad(Ad_id):
        return Request_t.query.filter_by(Ad_id=Ad_id)
    
    def get_camp(self):
        Campaign_id= Ad_Campaign_t.get_ad(Ad_id=self.Ad_id).Campaign_id
        return Campaign_t.get_campaign(Campaign_id)
    

    __table_args__ = (db.ForeignKeyConstraint(['Ad_id'], ['Ad_Campaign.Ad_id'], name='fk_ad_campaign_request'),
                      db.ForeignKeyConstraint(['responser_id'], ['User.id'], name='fk_ad_campaign_responser'),
                      db.ForeignKeyConstraint(['requester_id'], ['User.id'], name='fk_ad_campaign_requester'))


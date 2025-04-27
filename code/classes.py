from models import * 
from datetime import datetime, date
import logging
import matplotlib.pyplot as plt

class User:
    def __init__(self, username):
        self.this_user = User_t.get_user(username)
        self.id = self.this_user.id
        self.username = self.this_user.username
        self.password = self.this_user.password
        self.role_id = self.this_user.role_id
        self.type= self.this_user.type
        self.is_flagged = self.this_user.is_flagged
    
    @staticmethod
    def is_exist(username):
        if User_t.get_user(username)==None:
            return False
        else:
            return True
        
    def validate_user(self, u_name, pwd):
        if self.username == u_name and self.password == pwd:
            return True
        else:
            return False

    def is_spons(self):
        if self.role_id == 2:
            return True
        else:
            return False

    def is_inf(self):
        if self.role_id == 3:
            return True
        else:
            return False

    def is_admin(self):
        if self.role_id == 1:
            return True
        else:
            return False

        
#children of user:
class Sponsor(User):
    def __init__(self, username):
        super().__init__(username)
        self.Industry = self.this_user.Industry
        self.Company_name = self.this_user.Company_name
        self.Contact_name = self.this_user.Contact_name
        self.Contact_email = self.this_user.Contact_email
        self.Contact_phone = self.this_user.Contact_phone
    
    @staticmethod
    def create_Sponsor(username, password, role_id, Industry, Company_name, Contact_name, Contact_email, Contact_phone):
        this_user = Sponsor_t.get_sponsor(username)
        if this_user:
            return "user already exists!"
        else:
            try:
                new_user = Sponsor_t(username = username, password = password, role_id=role_id, Industry=Industry,Company_name=Company_name, Contact_name=Contact_name,Contact_email=Contact_email,Contact_phone=Contact_phone)
                db.session.add(new_user)
                db.session.commit()
                return Sponsor(username)
            except Exception as e:
                # catch any error
                logging.error("An error occurred: " + str(e))
                return {"error": "An error occurred", "message": "Check Duplicate entry or constraint violation, go back and fill all fields correctly\n" + "Error:" +str(e)}
            

    def get_camp_list(self):
        camp_list=[]
        for campgn in Campaign_t.get_campaign(None):
            if campgn.Sponsor_id==self.id and campgn.Status!='flagged':
                camp_list.append(Campaign(campgn.Campaign_id))
        return camp_list
        # returns an array of campaign type objects associated with sponsor

    def flag_it(self):
        self.this_user.is_flagged=1
        db.session.commit()
        pass

    def unflag(self):
        self.this_user.is_flagged=0
        db.session.commit()
        pass

    def delete(self):
        db.session.delete(self.this_user)
        db.session.commit()

    def get_influencer(self):
        # returns an array of influencer type objects associated with sponsor
        influencer_list=[]
        for influ in Influencer_t.get_influencer(None):
            if influ.is_flagged==0:
                influencer_list.append(Influencer(influ.username))
        return influencer_list
        pass

    def get_ad_list(self):
        # returns an array of ad type objects associated with sponsor
        ad_list=[]
        for ad in Ad_Campaign_t.get_ad(None):
            ad=Ad(ad.Ad_id)
            if Campaign(ad.Campaign_id).Sponsor_id==self.id and ad.Status!='flagged':
                ad_list.append(ad)
        return ad_list

    def get_requests(self):
        # returns an array of request type objects associated with sponsor
        pass

    def Niche_wise_ad_count(self, user_id):
        # return path to image
        pass

    def Influencer_count_per_campaign(self, user_id):
        # return path to image
        pass

    def Budget_wise_campaign_pie_chart(self, user_id):
        # return path to image
        pass

    def Influencer_wise_ad_status(self, user_id):
        # return path to image
        pass


class Influencer(User):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.Contact_name = self.this_user.Contact_name
        self.Contact_email = self.this_user.Contact_email
        self.Contact_phone = self.this_user.Contact_phone
        self.DOB = self.this_user.DOB
        self.Niche = self.this_user.Niche
        self.platform = dict(zip([p.platform_name for p in self.this_user.platforms], [p.Reach for p in self.this_user.platforms]))
    
    @staticmethod
    def create_Influencer(username, password, role_id, Contact_name, Contact_email, Contact_phone, DOB, Niche, platforms):
        this_user = Influencer_t.get_influencer(username)
        if this_user:
            return "user already exists!"
        else:
            try:
                new_user = Influencer_t(username = username, password = password, role_id=role_id, Contact_name=Contact_name,Contact_email=Contact_email,Contact_phone=Contact_phone, DOB=DOB, Niche=Niche)
                db.session.add(new_user)
                db.session.commit()
                for platform in platforms:
                    if platform['platform_name']!=None:
                        new_platform = Platform_t(influencer_id = new_user.id, platform_name=platform['platform_name'], Reach=platform['reach'])
                        db.session.add(new_platform)
                        db.session.commit()
                return Influencer(username)
            except Exception as e:
                # catch any error
                logging.error("An error occurred: " + str(e))
                return {"error": "An error occurred", "message": "Check Duplicate entry or constraint violation, go back and fill all fields correctly\n" + "Error:" +str(e)}

    def flag_it(self):
        self.this_user.is_flagged=1
        db.session.commit()
        pass

    def unflag(self):
        self.this_user.is_flagged=0
        db.session.commit()
        pass

    def delete(self):
        db.session.delete(self.this_user)
        db.session.commit()

    def get_camp_list(self):
        # returns an array of campaign type objects associated with Influencer
        camp_list=[]
        ad_list=self.get_ad_list()
        for ads in ad_list:
            camp= Campaign(ads.Campaign_id)
            if camp not in camp_list:
                camp_list.append(camp)
        return camp_list

    def get_sponsor(self):
        sponsor_list=[]
        for spon in Sponsor_t.get_sponsor(None):
            if spon.is_flagged==0:
                sponsor_list.append(Sponsor(spon.username))
        return sponsor_list
        # returns an array of sponsor type objects associated with Influencer

    def get_ad_list(self):
        # returns an array of ad type objects associated with Influencer
        ad_list=[]
        for ads in Ad_Campaign_t.get_ad(None):
            for relation in Ad_influencers_t.get_ad_influencer(ads.Ad_id):
                if relation.influencer_name==self.username:
                    ads=Ad(ads.Ad_id)
                    ad_list.append(ads)
        return ad_list

    def get_requests(self):
        req_list=[]
        for req in Request_t.get_request(None):
            if req.requester_id==self.id or req.responser_id==self.id:
                req_list.append(Request(req.Req_id))
        return req_list
        # returns an array of request type objects associated with Influencer
        
    def Sponsor_spread_ads_Count(self, user_id):
        # return path to image
        pass
    def Ad_wise_revenue(self, user_id):
        # return path to image
        pass
    def Sponsor_wise_revenue(self, user_id):
        # return path to image
        pass
    def Industry_wise_ad_counts(self, user_id):
        # return path to image
        pass

class Admin(User):
    def __init__(self, user_id):
        super().__init__(user_id)

    def get_camp_list(self):
        camp_list=[]
        for camp in Campaign_t.get_campaign(None):
            camp=Campaign(camp.Campaign_id)
            camp_list.append(camp)
        # returns an array of all campaign type objects
        return camp_list
    def get_sponsor(self):
        # returns an array of all sponsor type objects
        sponsor_list=[]
        for spon in Sponsor_t.get_sponsor(None):
            sponsor_list.append(Sponsor(spon.username))
        return sponsor_list
        
    def get_influencer(self):
        # returns an array of all Influencer type objects
            influencer_list=[]
            for inf in Influencer_t.get_influencer(None):
                influencer_list.append(Influencer(inf.username))
            return influencer_list
    
    def get_ad_list(self):
        # returns an array of all ad type objects
        ad_list=[]
        for ad in Ad_Campaign_t.get_ad(None):
                ad_list.append(Ad(ad.Ad_id))
        return ad_list
    
    def get_requests(self):
        # returns an array of all request type objects
        req_list=[]
        for requests in Request_t.get_request(None):
            req=Request(requests.Req_id)
            req_list.append(req)
        return req_list
        
    def get_objects(self, type, status):
        result_list=[]
        if type==Sponsor:
            if status=='flagged':
                for entry in self.get_sponsor():
                    if entry.is_flagged==1:
                        result_list.append(entry)
            if status=='active':
                for entry in self.get_sponsor():
                    if entry.is_flagged==0:
                        result_list.append(entry)
            if status==None:
                result_list=self.get_sponsor()
        if type==Influencer:
            if status=='flagged':
                for entry in self.get_influencer():
                    if entry.is_flagged==1:
                        result_list.append(entry)
            if status=='active':
                for entry in self.get_influencer():
                    if entry.is_flagged==0:
                        result_list.append(entry)
            if status==None:
                result_list=self.get_influencer()
        if type==Campaign:
            for entry in self.get_camp_list():
                    if entry.status==status or status==None:
                        result_list.append(entry)
        if type==Ad:
            for entry in self.get_ad_list():
                    if entry.Status==status or status==None:
                        result_list.append(entry)
        if type==Request:
            for entry in self.get_requests():
                    if entry.Status==status or status==None:
                        result_list.append(entry)
        # returns all instances of type object and status status
        return result_list
    
    def get_from_id(self,id,type):
        if type==Sponsor:
            return Sponsor(User_t.get_user_by_id(id).username)
        if type==Influencer:
            return Influencer(User_t.get_user_by_id(id).username)
        if type==Campaign:
            return Campaign(id)
        if type==Ad:
            return Ad(id)
        if type==Request:
            return Request(id)
        
    def flag(self, id, type):
        obj=self.get_from_id(id,type)
        obj.flag_it()
        #flags the object of type 'type' with id 'id' 
        pass

    def unflag(self,id,type):
        print('HEre')
        obj=self.get_from_id(id,type)
        obj.unflag()
        pass

    def delete(self, id, type):
        obj=self.get_from_id(id,type)
        obj.delete()
        # deletes the object from the system
        pass
    def all_users_object_in_sys(self):
        # return path to image 
        # Chart Displaying number of Sponsors, Influencers, campaign, and Ads in the system
        num_sponsors = len(self.get_sponsor())
        num_influencers = len(self.get_influencer())
        num_campaigns = len(self.get_camp_list())
        num_ads = len(self.get_ad_list())
        # Create a pie chart using matplotlib
        
        labels = ['Sponsors', 'Influencers', 'Campaigns', 'Ads']
        sizes = [num_sponsors, num_influencers, num_campaigns, num_ads]
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('All Users Object in System')
        plt.savefig('static/img1.png')
        plt.close()
        return 'static/img1.png'
        
    def Industry_wise_campaign_list(self):
        # return path to image
        # no. of campaigns in each industry
        pass
    def Niche_wise_Ads_list(self):
        # return path to image
        # no. of ads in each niche
        pass
    def Sponsor_wise_campaign_count(self):
        # return path to image
        # number of campaigns per sponsor
        pass

class Campaign:
    def __init__(self, campaign_id):
        self.this_campaign = Campaign_t.get_campaign(campaign_id)
        self.Campaign_id = self.this_campaign.Campaign_id
        self.Sponsor_id = self.this_campaign.Sponsor_id
        self.Title = self.this_campaign.Title
        self.Desc = self.this_campaign.Desc
        self.Niche = self.this_campaign.Niche
        self.date_created = self.this_campaign.date_created
        self.start_date = self.this_campaign.start_date
        self.end_date = self.this_campaign.end_date
        self.Goal_ads = self.this_campaign.Goal_ads
        self.Budget = self.this_campaign.Budget
        self.progress = (Ad_Campaign_t.get_adcount_by_camp(campaign_id) / self.Goal_ads) * 100 
        self.status = self.get_status()
        self.this_campaign.Status = self.status
        self.flagged=self.is_flagged()
        db.session.commit()

    def get_status(self):
        if self.this_campaign.Status=='flagged':
            return self.this_campaign.Status
        elif self.start_date > date.today():
            return "created"
        elif self.start_date <= date.today() and self.end_date >= date.today():
            return "active"
        elif self.end_date < date.today():
            return "ended"
    
    def flag_it(self):
        self.this_campaign.Status='flagged'
        Ads= self.get_ad_list()
        if Ads!=None:
            for ad in Ads:
                ad.flag_it()
        db.session.commit()
        pass

    def unflag(self):
        print('Here')
        self.this_campaign.Status='unflagged'
        Ads= self.get_ad_list()
        if Ads!=None:
            for ad in Ads:
                ad.unflag()
        db.session.commit()
        self.status = self.get_status()
        self.this_campaign.Status = self.status
        db.session.commit()
        

    @staticmethod
    def create_Campaign(Title, Desc, Niche, start_date, end_date, Goal_ads, Budget, username):
        #check date_created with current date and start_date in future, and end_date after start_date, and goal_ads>0
        #now write a try except command like in previous classes to create a row in the table camoaign
        if start_date < date.today() or end_date < start_date or Goal_ads <= 0:
            return "Invalid input"
        try:
            new_campaign = Campaign_t(Sponsor_id = User_t.get_user(username).id,  Title = Title, Desc = Desc, Niche = Niche, date_created = datetime.now(), start_date = start_date, end_date = end_date, Goal_ads = Goal_ads, Budget=Budget)
            db.session.add(new_campaign)
            db.session.commit()
            return Campaign(new_campaign.Campaign_id)
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Check Duplicate entry or constraint violation, go back and fill all fields correctly\n" + "Error:" +str(e)}

    def is_flagged(self):
        return self.status == "flagged"

    def get_influencer(self):
        # returns an array of Influencer type objects associated with the campaign
        return Influencer_t.get_influencer_by_campaign(self.Campaign_id)

    def get_ad_list(self):
        # return list of ads associated with the given ID
        Ad_list=[]
        for ad in Ad_Campaign_t.get_ad_list_by_campaign(self.Campaign_id):
            ad = Ad(ad.Ad_id)
            Ad_list.append(ad)
        return Ad_list

    def get_requests(self):
        # returns an array of all request type objects
        return Request_t.get_requests_by_campaign(self.Campaign_id)

    def delete(self):
        try:
            Ads= self.get_ad_list()
            if Ads!=None:
                for ad in Ads:
                    ad.delete()
            db.session.delete(self.this_campaign)
            db.session.commit()
            return True
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Error:" +str(e)}
     
    def requests(self):
        pass

    def is_active(self):
        # returns if the campaign is active
        return self.status == "active"
    
    def get_active_ad(self):
        #return non flagged ads not assigned to the given Ad
        active_Ads = []
        for ad in Ad_Campaign_t.get_ad():
            ad=Ad(ad.Ad_id)
            if ad.is_flagged == False and self.id not in ad.Influencer_id:
                active_Ads.append(ad)
        return active_Ads 
    
#connot exist without campaign
class Ad:
    def __init__(self, Ad_id):
        self.this_ad = Ad_Campaign_t.get_ad(Ad_id)
        self.Ad_id = self.this_ad.Ad_id
        self.Campaign_id = self.this_ad.Campaign_id
        self.Inf_names=self.Influencer_names()
        self.Title = self.this_ad.Title
        self.Desc = self.this_ad.Desc
        self.Terms = self.this_ad.Terms
        self.progress = Campaign(self.Campaign_id).progress
        self.Niche = Campaign_t.get_campaign(self.Campaign_id).Niche
        self.camp_title = Campaign_t.get_campaign(self.Campaign_id).Title
        self.Status = self.get_status()
        self.this_ad.Status = self.Status
        db.session.commit()
        self.Payment_amt = self.this_ad.Payment_amt
        self.flagged= self.is_flagged()

    def Influencer_names(self):
        names=[]
        list=Ad_influencers_t.get_ad_influencer(self.Ad_id)
        for relation in list:
            names.append(relation.influencer_name)
        return names
    
    @staticmethod
    def get_all_ads():
        ad_list=[]
        for ad in Ad_Campaign_t.get_ad(None):
                print('Here')
                ad_list.append(Ad(ad.Ad_id))
        return ad_list

    def get_status(self):
        if self.this_ad.Status=='flagged':
            return self.this_ad.Status
        elif self.Inf_names==[]:
            return "created"
        elif self.Inf_names!=[]:
            return "active"
        elif Campaign_t.get_campaign(self.Campaign_id).Status=="ended":
            return "ended"

    def flag_it(self):
        self.this_ad.Status='flagged'
        requests=self.requests_by_ad()
        if requests!=None:
            for req in requests:
                req.flag_it()
        db.session.commit()
        pass

    def unflag(self):
        self.this_ad.Status='unflagged'
        db.session.commit()
        self.status = self.get_status()
        self.this_ad.Status = self.status
        requests=self.requests_by_ad()
        if requests!=None:
            for req in requests:
                req.unflag()
        db.session.commit()

    @staticmethod
    def create_Ad(Campaign_id, Title, Desc, Terms, Payment_amt):
        #check if campaign and influencer exist
        if Campaign_t.get_campaign(Campaign_id) == None:
            return "Invalid input"
        try:
            new_ad = Ad_Campaign_t(Campaign_id = Campaign_id, Title = Title, Desc = Desc, Terms = Terms, Payment_amt = Payment_amt)
            db.session.add(new_ad)
            db.session.commit()
            return Ad(new_ad.Ad_id)
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Check Duplicate entry or constraint violation, go back and fill all fields correctly\n" + "Error:" +str(e)}
    
    def is_flagged(self):
        return self.Status == "flagged"

    def is_active(self):
        return self.Status == "active"
    
    def delete(self):
        try:
            requests=self.requests_by_ad()
            if requests!=None:
                for req in requests:
                    req.delete()
            db.session.delete(self.this_ad)
            db.session.commit()
            return True
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Error:" +str(e)}
        
    def get_active_influencer(self):
        #return non flagged influencers not assigned to the given Ad
        active_influencers = []
        for influencer in Influencer_t.get_influencer(None):
            influencer=Influencer(influencer.username)
            if self.Influencer_names()!=[]:
                if influencer.is_flagged == 0 and influencer.username not in self.Influencer_names():
                    active_influencers.append(influencer)
            else:
                if influencer.is_flagged == 0:
                    active_influencers.append(influencer)
        return active_influencers

    def requests_by_ad(self):
        #return list of requests associated with the given ID
        req_list=[]
        requests=Request_t.get_requests_by_ad(self.Ad_id)
        for req in requests:
            req= Request(req.Req_id)
            req_list.append(req)


#connot exist without ad
class Request:
    def __init__(self, req_id):
        self.this_request = Request_t.get_request(req_id)
        self.camp_name = self.this_request.get_camp().Title
        self.Req_id = self.this_request.Req_id
        self.Ad_id = self.this_request.Ad_id
        self.Ad = Ad(self.Ad_id)
        self.ad_terms = Ad(self.Ad_id).Terms
        self.Ad_name = Ad(self.Ad_id).Title
        self.requester_id = self.this_request.requester_id
        self.requester_name = User_t.get_user_by_id(self.requester_id).username
        self.responser_id = self.this_request.responser_id
        self.responser_name = User_t.get_user_by_id(self.responser_id).username
        self.Status = self.this_request.Status
        self.Payment_amt = self.this_request.payment_amt
        self.req_date = self.this_request.req_date
        self.message_req = self.this_request.message_req
        self.message_resp = self.this_request.message_resp

    def set_status(self,stat):
        try:
            self.Status = stat
            self.this_request.Status = self.Status
            db.session.commit()
            return True
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Check Duplicate entry or constraint violation, go back and fill all fields correctly\n" + "Error:" +str(e)}


    def flag_it(self):
        self.this_request.Status='flagged'
        db.session.commit()
        pass

    def unflag(self):
        self.set_status('created')
        db.session.commit()


    @staticmethod
    def create_req(Ad_id, requester_id, responser_id, Payment_amt, message_req, message_resp):
        #check if ad exists
        if Ad_Campaign_t.get_ad(Ad_id) == None:
            return "Invalid input"
        try:
            new_request = Request_t(Ad_id = Ad_id, requester_id = requester_id, responser_id = responser_id, Status = 'created', payment_amt = Payment_amt, req_date = date.today(), message_req = message_req, message_resp = message_resp)
            db.session.add(new_request)
            db.session.commit()
            return Request(new_request.Req_id)
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Check Duplicate entry or constraint violation, go back and fill all fields correctly\n" + "Error:" +str(e)}
    
    def pay(self, amt):
        #edits payment amount for request
        self.Payment_amt = amt
        db.session.commit()

    def req_accept(self, acceptor_id):
        this_user=User(User_t.get_user_by_id(acceptor_id).username)
        if this_user.is_inf():
            this_user=Influencer(this_user.username)
            try:
                new_rel=Ad_influencers_t(Ad_id=self.Ad_id, influencer_name=this_user.username)
                db.session.add(new_rel)
                db.session.commit()
                self.set_status('active')
                return 'accepted'
            except (Exception) as e:
                logging.error("An error occurred: " + str(e))
                return {"error": "An error occurred", "message": "Check uniqueness\n" + "Error:" +str(e)}
        
        if this_user.is_spons():
            u_name = self.requester_name
            try:
                new_rel=Ad_influencers_t(Ad_id=self.Ad_id, influencer_name=u_name)
                db.session.add(new_rel)
                db.session.commit()
                self.set_status('active')
                return 'accepted'
            except Exception as e:
                logging.error("An error occurred: " + str(e))
                return {"error": "An error occurred", "message": "Check Duplicate entry or constraint violation, go back and fill all fields correctly\n" + "Error:" +str(e)}


    def is_flagged(self):
        return self.Status == "flagged"

    def is_active(self):
        return self.Status == "active"
    
    def negotiate(self,updated_payment,your_msg):
        try:
            #updating payment
            self.this_request.payment_amt=updated_payment
            #updating message
            self.this_request.message_resp=your_msg
            #swapping requester and responser
            temp=self.this_request.requester_id
            self.this_request.requester_id=self.this_request.responser_id
            self.this_request.responser_id=temp
            temp=self.this_request.message_req
            self.this_request.message_req=self.this_request.message_resp
            self.this_request.message_resp=temp
            db.session.commit()
            return self
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Error:" +str(e)}
    

    def delete(self):
        try:
            db.session.delete(self.this_request)
            db.session.commit()
            return True
        except Exception as e:
            logging.error("An error occurred: " + str(e))
            return {"error": "An error occurred", "message": "Error:" +str(e)}
    
    @staticmethod
    def get_req_from(name):
        req_list=[]
        requests=Request_t.get_request(None)
        for request in requests:
            request=Request(request.Req_id)
            if request.requester_name==name and request.Status=='created':
                req_list.append(request)
        return req_list
    
    @staticmethod
    def get_req_to(name):
        req_list=[]
        requests=Request_t.get_request(None)
        for request in requests:
            request=Request(request.Req_id)
            if request.responser_name==name and request.Status=='created':
                req_list.append(request)
        return req_list
    
    @staticmethod
    def active_req(name):
        req_list=[]
        requests=Request_t.get_request(None)
        for request in requests:
            request=Request(request.Req_id)
            if (request.responser_name==name or request.responser_name==name) and request.Status=='active':
                req_list.append(request)
        return req_list
    
        


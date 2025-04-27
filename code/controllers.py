from flask import current_app as app
from flask import Flask, render_template, redirect, request, flash, session
import logging
from database import db
from models import *
from classes import *
from datetime import datetime

def string_to_int(string):
    if string is None:
        return 0  # or raise a custom error
    # Convert the concatenated string of ASCII values to an integer
    return int(string)


@app.route('/')
def home():
    return redirect(f'/Login')

@app.route('/Login', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get("u_name")
        pwd = request.form.get("pwd")
        if User.is_exist(username)==False:
            return "user does not exist!"
        else:
            this_user=User(username)
            if this_user.is_flagged:
                return "You are flagged, contact admin!"
            val=this_user.validate_user(username, pwd)
            if val:
                return redirect(f'/user/{this_user.username}')
            else:
                return "incorrect Password"
    return render_template('user_login.html')


@app.route('/spon-reg', methods = ['GET', 'POST'])
def spon_register():
    if request.method == 'POST':
        username = request.form.get("usrnm")
        username = username.strip() or None
        password = request.form.get("pwd")
        password = password.strip() or None
        role_id = 2
        Industry = request.form.get("sponsoringIndustries")
        Company_name = request.form.get("cmpnm")
        Contact_phone = request.form.get("phno")
        Contact_email = request.form.get("email")
        Contact_name = request.form.get("nm")
        new_user=Sponsor.create_Sponsor(username, password, role_id, Industry, Company_name, Contact_name, Contact_email, Contact_phone)
        if isinstance(new_user, Sponsor):
            flash(f'Account created for {new_user.username} as a sponsor!', 'success')
            return redirect('/Login')
        else:
            return new_user
    return render_template('reg_spons.html')

@app.route('/inf-reg', methods = ['GET', 'POST'])
def inf_register():
    if request.method == 'POST':
        username = request.form.get("usrnm")
        username = username.strip() or None
        password = request.form.get("pwd")
        password = password.strip() or None
        role_id = 3
        first_nm= request.form.get("frnm")
        last_name= request.form.get("lstnm")
        Contact_phone = request.form.get("conph")
        Contact_email = request.form.get("conem")
        DOB = datetime.strptime(request.form.get("bday"), "%Y-%m-%d")
        DOB = date(DOB.year, DOB.month, DOB.day)
        Niche = request.form.get("influencerNiche")
        Contact_name = first_nm +' ' + last_name
        platform_name=[]
        platreach=[]
        if request.form.get("fcbk")!=None:
            platform_name.append(request.form.get("fcbk"))
            platreach.append(request.form.get("fcbreach"))
        
        if request.form.get("intgm")!=None:
            platform_name.append(request.form.get("intgm"))
            platreach.append(request.form.get("intreach"))
        
        if request.form.get("twtr")!=None:
            platform_name.append(request.form.get("twtr"))
            platreach.append(request.form.get("twtreach"))
       
        if request.form.get("Utb")!=None:
            platform_name.append(request.form.get("Utb"))
            platreach.append(request.form.get("Utbreach"))
        
        platforms = []
        for platform, reach in zip(platform_name, platreach):
            try:
                platforms.append({"platform_name": platform, "reach": int(reach)})
            except ValueError:
                flash(f"Invalid reach for platform {platform}", "error")
                return redirect('/inf-reg')
            
        new_user=Influencer.create_Influencer(username, password, role_id, Contact_name, Contact_email, Contact_phone, DOB, Niche, platforms)
        if isinstance(new_user, Influencer):
            flash(f'Account created for {new_user.username} as a sponsor!', 'success')
            return redirect('/Login')
        else:
            return new_user
    return render_template('reg_infl.html')


@app.route('/user/<username>', methods = ['GET', 'POST'])
def user_dash(username):
    this_user=User(username)
    #admin dashboard
    if this_user.role_id == 1:
        this_user=Admin(username)
        Flagged_campaigns=this_user.get_objects(Campaign, 'flagged')
        print(Flagged_campaigns)
        return render_template("admin_dash.html", user= this_user.username, active_campaigns=this_user.get_objects(Campaign, 'active'), Flagged_Sponsor=this_user.get_objects(Sponsor, 'flagged'),Flagged_Influencer=this_user.get_objects(Influencer, 'flagged'), Flagged_campaigns=this_user.get_objects(Campaign, 'flagged'))
    
    #spons dasshboard
    if this_user.role_id == 2:
        if request.method=='POST':
            request_type = request.form.get('type')
            req_id=request.form.get('id')
            #print(request_type,req_id)
            this_req=Request(req_id)
            if request_type=='accept':
                new_rel=this_req.req_accept(this_user.id)
                if(new_rel=='accepted'):
                    return redirect(f'/user/{this_user.username}')
                else:
                    return new_req
            if request_type=='reject':
                this_req.set_status('rejected')
            if request_type=='Negotiate':
                updated_payment=request.form.get('payment')
                your_msg = request.form.get('msg')
                if this_req.Status=='created':
                    new_req=this_req.negotiate(updated_payment,your_msg)
                    if(isinstance(new_req, Request)):
                        return redirect(f'/user/{this_user.username}')
                    else:
                        return new_req
                else:
                    return "can not negotiate, The request is accepted, rejected or flagged"
        this_user=Sponsor(username)
        recieved_requests = Request.get_req_to(this_user.username)
        sent_requests = Request.get_req_from(this_user.username)
        return render_template("spons_dash.html", user= this_user.username, active_campaigns= this_user.get_camp_list(), recieved_requests = recieved_requests, sent_requests = sent_requests)

    #influencer dashboard
    if this_user.role_id == 3:
        if request.method=='POST':
            request_type = request.form.get('type')
            req_id=request.form.get('id')
            this_req=Request(req_id)
            if request_type=='accept':
                new_rel=this_req.req_accept(this_user.id)
                return redirect(f'/user/{this_user.username}')
            if request_type=='reject':
                this_req.set_status('rejected')
            if request_type=='Negotiate':
                updated_payment=request.form.get('payment')
                your_msg = request.form.get('msg')
                if this_req.Status=='created':
                    new_req=this_req.negotiate(updated_payment,your_msg)
                    if(isinstance(new_req, Request)):
                        return redirect(f'/user/{this_user.username}')
                    else:
                        return new_req
                else:
                    return "can not negotiate, The request is accepted, rejected or flagged"
        this_user = Influencer(username)
        active_requests = Request.active_req(this_user.username)
        recieved_requests = Request.get_req_to(this_user.username)
        sent_requests = Request.get_req_from(this_user.username)
        return render_template("inf_dash.html", user= this_user.username, active_ads = this_user.get_ad_list(),recieved_requests = recieved_requests, sent_requests = sent_requests)
    
@app.route('/user/<username>/Campaign', methods = ['GET', 'POST'])
def user_Campaign(username):
    this_user = Sponsor(username)
    if request.method=='POST':
        request_type = request.form.get("type")
        if request_type=='delete':
            id=request.form.get('id')
            result = Campaign(id).delete()
            if result:
                return redirect(f'/user/{this_user.username}/Campaign')
            else:
                return result
        if request_type=='submit':
            Title = request.form.get("title")
            Desc = request.form.get("desc")
            Niche = request.form.get("campaign-niche")
            start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
            start_date = date(start_date.year, start_date.month, start_date.day)
            end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
            end_date = date(end_date.year, end_date.month, end_date.day)
            Goal_ads = int(request.form.get("goal_ads"))
            Budget = request.form.get("budget")
            new_campaign = Campaign.create_Campaign(Title, Desc, Niche, start_date, end_date, Goal_ads, Budget, username)
            if isinstance(new_campaign, Campaign):
                flash(f'Campaign created for {this_user.username}!', 'success')
                return redirect(f'/user/{this_user.username}/Campaign')
            else:
                return new_campaign
    # sponsor adds Campaign
    if this_user.role_id == 2:
        return render_template("spons_Campaign.html",user= this_user.username, active_campaigns= this_user.get_camp_list())
    


@app.route('/user/<username>/<int:campaign_id>', methods = ['GET', 'POST'])
def add_Camp(username, campaign_id):
    this_user = Sponsor(username)
    this_camp = Campaign(campaign_id)
    if request.method=='POST':
        request_type = request.form.get("type")
        if request_type=='delete':
            id=request.form.get('id')
            result = Ad(id).delete()
            if result:
                return redirect(f'/user/{this_user.username}/{this_camp.Campaign_id}')
            else:
                return result
        if request_type=='submit':
            Title =request.form.get("title")
            Desc = request.form.get("desc")
            Terms = request.form.get("Terms")
            Payment = string_to_int(request.form.get("Payment-amt"))
            new_ad = Ad.create_Ad(Campaign_id=campaign_id, Title=Title,Desc=Desc,Terms=Terms,Payment_amt=Payment)
            if isinstance(new_ad, Ad):
                return redirect(f'/user/{this_user.username}/{this_camp.Campaign_id}')
            else:
                return new_ad
    return render_template('spons_add_ad.html', user=username, campaign=this_camp, campaign_Ads=this_camp.get_ad_list())

@app.route('/user/<username>/<int:campaign_id>/<int:ad_id>',methods=['GET','POST'])
def assign_influ(username,campaign_id,ad_id):
    this_user = Sponsor(username)
    this_ad = Ad(ad_id)
    if request.method=='POST':  
        request_type = request.form.get("type")
        if request_type=='choose_influ':
            list = this_ad.get_active_influencer()
            influ_list=[]
            for entries in list:
                influ = request.form.get(entries.username)
                influ_msg = request.form.get(entries.username+'-msg')
                if influ!=None:
                    influencer=Influencer(influ)
                    influ_list.append(influencer)
                    new_req=Request.create_req(Ad_id = ad_id, requester_id = this_user.id, responser_id = influencer.id, Payment_amt = this_ad.Payment_amt,  message_req = influ_msg, message_resp=None)
                    if isinstance(new_req, Request)!=True:
                        return new_req
            if entries==[]:
                return 'no influencers in the system'   
            elif influ_list==[]:
                return 'no influencers selected'
            return redirect(f'/user/{this_user.username}')
                            
    return render_template("choose_entries.html", list = this_ad.get_active_influencer(), user=username, type='influencer', campaign_id = campaign_id, ad_id = ad_id)

@app.route('/user/<username>/find', methods=['GET','POST'])
def find_screen(username):
    this_user=User(username)
    if request.method=='POST':
        request_type=request.form.get('type')
        req_id=request.form.get('req_id')
        Ad_id=request.form.get('Ad_id')
        camp_id=request.form.get('camp_id')
        user_id=request.form.get('user_id')
        if this_user.role_id==1:
            this_user=Admin(username)
            if request_type=='flag':
                if req_id!=None:
                    this_user.flag(request.form.get('req_id'),Request)
                if Ad_id!=None:
                    this_user.flag(request.form.get('Ad_id'),Ad)
                if camp_id!=None:
                    this_user.flag(request.form.get('camp_id'),Campaign)
                if user_id!=None:
                    if User(User_t.get_user_by_id(request.form.get('user_id'))).is_inf():
                        this_user.flag(request.form.get('user_id'),Influencer)
                    if User(User_t.get_user_by_id(request.form.get('user_id'))).is_spons():
                        this_user.flag(request.form.get('user_id'),Sponsor)
            if request_type=='unflag':
                if req_id!=None:
                    print('Here1')
                    this_user.unflag(request.form.get('req_id'),Request)
                if Ad_id!=None:
                    print('Here2')
                    this_user.unflag(request.form.get('Ad_id'),Ad)
                if camp_id!=None:
                    print('Here3')
                    this_user.unflag(request.form.get('camp_id'),Campaign)
                if user_id!=None:
                    print('Here4')
                    if User(User_t.get_user_by_id(request.form.get('user_id'))).is_inf:
                        this_user.unflag(request.form.get('user_id'),Influencer)
                    if User(User_t.get_user_by_id(request.form.get('user_id'))).is_spons:
                        this_user.unflag(request.form.get('user_id'),Sponsor)
            if request_type=='delete':
                if req_id!=None:
                    print('Here1')
                    this_user.delete(request.form.get('req_id'),Request)
                if Ad_id!=None:
                    print('Here2')
                    this_user.delete(request.form.get('Ad_id'),Ad)
                if camp_id!=None:
                    print('Here3')
                    this_user.delete(request.form.get('camp_id'),Campaign)
                if user_id!=None:
                    print('Here4')
                    if User(User_t.get_user_by_id(request.form.get('user_id'))).is_inf:
                        this_user.delete(request.form.get('user_id'),Influencer)
                    if User(User_t.get_user_by_id(request.form.get('user_id'))).is_spons:
                        this_user.unflag(request.form.get('user_id'),Sponsor)
        if this_user.role_id==2:
            this_user=Sponsor(username)
            print(req_id)
            if req_id!=None:
                this_req=Request(req_id)
                if request_type=='accept':
                    this_req.req_accept(this_user.id)
                if request_type=='reject':
                    this_req.set_status('rejected')
                if request_type=='Negotiate':
                    updated_payment=request.form.get('payment')
                    your_msg = request.form.get('msg')
                    if this_req.Status=='created':
                        new_req=this_req.negotiate(updated_payment,your_msg)
                        if(isinstance(new_req, Request)):
                            return redirect(f'/user/{this_user.username}')
                        else:
                            return new_req
                    else:
                        return "can not negotiate, The request is accepted, rejected or flagged"
            if request_type=='delete':
                if Ad_id!=None:
                    result = Ad(Ad_id).delete()
                    this_camp=Campaign(result.Campaign_id)
                    if result:
                        return redirect(f'/user/{this_user.username}/{this_camp.Campaign_id}')
                    else:
                        return result
                if camp_id!=None:
                    result = Campaign(camp_id).delete()
      
        if this_user.role_id==3:
            this_req=Request(req_id)
            if request_type=='accept':
                this_req.req_accept(this_user.id)
            if request_type=='reject':
                this_req.set_status('rejected')
            if request_type=='Negotiate':
                updated_payment=request.form.get('payment')
                your_msg = request.form.get('msg')
                if this_req.Status=='created':
                    new_req=this_req.negotiate(updated_payment,your_msg)
                    if(isinstance(new_req, Request)):
                        return redirect(f'/user/{this_user.username}')
                    else:
                        return new_req
                else:
                    return "can not negotiate, The request is accepted, rejected or flagged"
            if request_type=='request':
                this_ad=Ad(Ad_id)
                Request.create_req(Ad_id=Ad_id, requester_id=this_user.id, responser_id=Campaign(this_ad.Campaign_id).Sponsor_id, Payment_amt=this_ad.Payment_amt, message_req=None, message_resp=None)          
        return redirect(f'/user/{username}/find')
    if this_user.role_id==1:
        this_user=Admin(username)
        camp_list= this_user.get_camp_list()
        Influencer_to_view= this_user.get_objects(Influencer,None)
        Sponsor_to_view= this_user.get_objects(Sponsor,None)
        requests_to_view = this_user.get_objects(Request,None)
        ad_list = this_user.get_objects(Ad,None)
        return render_template("Find.html",user=username, this_user=this_user, campaigns=camp_list, Influencers=Influencer_to_view, Sponsors=Sponsor_to_view, ad_list=ad_list, requests=requests_to_view)
    else:
        recieved_requests = Request.get_req_to(this_user.username)
        sent_requests = Request.get_req_from(this_user.username)
        if this_user.role_id==2:
            this_user=Sponsor(username)
            camp_list= this_user.get_camp_list()
            users_to_view= this_user.get_influencer()
            return render_template("Find.html", campaigns=camp_list, this_user=this_user, Influencers=users_to_view, recieved_requests=recieved_requests, sent_requests=sent_requests, user=username)
        if this_user.role_id==3:
            this_user=Influencer(username)
            ad_list= Ad.get_all_ads()
            camp_list= this_user.get_camp_list()
            users_to_view= this_user.get_sponsor()
            return render_template("Find.html", campaigns=camp_list, this_user=this_user, ad_list=ad_list, Sponsors=users_to_view, recieved_requests=recieved_requests, sent_requests=sent_requests, user=username)
        
        

@app.route('/user/<username>/find/<int:influencer_id>', methods=['GET','POST'])
def assign_ad(username,influencer_id):
    this_user = Sponsor(username)
    this_influencer = Influencer(User_t.get_user_by_id(influencer_id).username)
    if request.method=='POST':  
        this_user = Sponsor(username)
        this_influencer = Influencer(User_t.get_user_by_id(influencer_id).username)
        request_type = request.form.get("type")
        if request_type=='choose_ad':
            list = this_user.get_ad_list()
            ad_list=[]
            for ads in list:
                ad = request.form.get(str(ads.Ad_id))
                Ad_msg = request.form.get(str(ads.Ad_id)+'-msg')
                print(ad,Ad_msg)
                if ad!=None:
                    print('Here')
                    ad=Ad(ad)
                    ad_list.append(ad)
                    new_req=Request.create_req(Ad_id = ad.Ad_id, requester_id = this_user.id, responser_id = this_influencer.id, Payment_amt = ad.Payment_amt,  message_req = Ad_msg, message_resp=None)
                    if isinstance(new_req, Request)!=True:
                        return new_req
            if list==[]:
                return 'no ad created by you'   
            elif ad_list==[]:
                return 'no ads selected'
            return redirect(f'/user/{this_user.username}')                      
    return render_template("choose_entries.html", list = this_user.get_ad_list(), user=username, type='ad_list', influ_id= influencer_id)

@app.route('/user/<username>/stat')
def stat(username):
    this_user=User(username)
    if this_user.role_id==1:
        this_user=Admin(username)
        imgpath1=this_user.all_users_object_in_sys()
        imgpath2=this_user.Industry_wise_campaign_list()
        imgpath3=this_user.Niche_wise_Ads_list()
        imgpath4=this_user.Sponsor_wise_campaign_count()
    return render_template("Stat.html", imgpath1=imgpath1, imgpath2=imgpath2, imgpath3=imgpath3, imgpath4=imgpath4 )
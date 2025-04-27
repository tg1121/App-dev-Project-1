//view modals
//viewcamp
$(document).ready(function() {
    // Modal toggle functionality
    $('.view-button-campaign').on('click', function() {
      var campaignId = $(this).data('campaign-id');
      var modalId = '#campaignModal-' + campaignId;
      var modal = $(modalId);
  
      // Retrieve campaign data from button element
      var campaignData = {
        title: $(this).data('campaign-title'),
        desc: $(this).data('campaign-desc'),
        progress: $(this).data('campaign-progress'),
        niche: $(this).data('campaign-niche'),
        status: $(this).data('campaign-status'),
        startDate: $(this).data('campaign-start-date'),
        endDate: $(this).data('campaign-end-date'),
        goalAds: $(this).data('campaign-goal-ads'),
        budget: $(this).data('campaign-budget')
      };
      console.log(campaignData);
      modal.find('.modal-header #campaignModalLabel').text(campaignData.title)
      // Update modal body content
      modal.find('.modal-body #campaign-desc').text(campaignData.desc);
      modal.find('.modal-body #campaign-progress').text(campaignData.progress);
      modal.find('.modal-body #campaign-niche').text(campaignData.niche);
      modal.find('.modal-body #campaign-status').text(campaignData.status);
      modal.find('.modal-body #campaign-start-date').text(campaignData.startDate);
      modal.find('.modal-body #campaign-end-date').text(campaignData.endDate);
      modal.find('.modal-body #campaign-goal-ads').text(campaignData.goalAds);
      modal.find('.modal-body #campaign-budget').text(campaignData.budget);
  
      modal.modal('show');
    });
  });

//viewad
$(document).ready(function() {
  // Modal toggle functionality
  $('.view-button-ad').on('click', function() {
    var AdId = $(this).data('ad-id');
    var modalId = '#adModal-' + AdId;
    var modal = $(modalId);

    // Retrieve campaign data from button element
    var Ad = {
      title: $(this).data('ad-title'),
      desc: $(this).data('ad-desc'),
      terms: $(this).data('ad-terms'),
      status: $(this).data('ad-status'),
      influencer_id: $(this).data('ad-influencer'),
      payment_amt: $(this).data('ad-payment-amt'),
    };
    console.log(Ad)
    modal.find('.modal-header #adModalLabel').text(Ad.title);
    // Update modal body content
    modal.find('.modal-body #ad-desc').text(Ad.desc);
    modal.find('.modal-body #ad-terms').text(Ad.terms);
    modal.find('.modal-body #ad-status').text(Ad.status);
    modal.find('.modal-body #ad-influencer').text(Ad.influencer_id);
    modal.find('.modal-body #ad-payment-amt').text(Ad.payment_amt);
    modal.modal('show');
  });
});

//view influ
$(document).ready(function(){
  $('.view-button-influ').on('click', function(){
    var Id = $(this).data('inf-id');
    var modalId = '#influModal-' + Id;
    var modal = $(modalId);

    var Influ = {
      username: $(this).data('inf-username'),
      Contact_name: $(this).data('inf-name'),
      Contact_email: $(this).data('inf-email'),
      Contact_phone: $(this).data('inf-phone'),
      DOB: $(this).data('inf-dob'),
      Niche: $(this).data('inf-niche'),
      platform: $(this).data('inf-platform'),
    }
    console.log(Influ)
    modal.find('.modal-header #inf-name').text(Influ.Contact_name);
    modal.find('.modal-body #inf-email').text(Influ.Contact_email);
    modal.find('.modal-body #inf-phone').text(Influ.Contact_phone);
    modal.find('.modal-body #inf-dob').text(Influ.DOB);
    modal.find('.modal-body #inf-niche').text(Influ.Niche);
    modal.find('.modal-body #inf-platform').text(Influ.platform);

    console.log('Attempting to show modal:', modalId);
    modal.modal('show');
  })
})

//view spons
$(document).ready(function(){
  $('.view-button-spons').on('click', function(){
    var Id = $(this).data('spon-id');
    var modalId = '#sponsModal-' + Id;
    var modal = $(modalId);

    var spon = {
      username: $(this).data('spon-username'),
      Contact_name: $(this).data('spon-name'),
      Contact_email: $(this).data('spon-email'),
      Contact_phone: $(this).data('spon-phone'),
      Industry: $(this).data('spon-indusry'),
      company_name: $(this).data('spon-company-name'),
    }
    console.log(spon)
    modal.find('.modal-header #spon-name').text(spon.Contact_name);
    modal.find('.modal-body #spon-email').text(spon.Contact_email);
    modal.find('.modal-body #spon-phone').text(spon.Contact_phone);
    modal.find('.modal-body #spon-industry').text(spon.Industry);
    modal.find('.modal-body #spon-company-name').text(spon.company_name);

    console.log('Attempting to show modal:', modalId);
    modal.modal('show');
  })
})

//view requests
$(document).ready(function(){
  $('.view-button-req').on('click', function(){
    var Id = $(this).data('req-id');
    var modalId = '#reqModal-' + Id;
    var modal = $(modalId);

    var Req = {
      ad_name: $(this).data('ad-name'),
      Campaign_name: $(this).data('camp-name'),
      requestor_name: $(this).data('req-name'),
      responser_name: $(this).data('res-name'),
      status: $(this).data('status'),
      terms: $(this).data('ad-terms'),
      payment_amt: $(this).data('payment-amt'),
      msg_recieved: $(this).data('res-msg'),
      your_msg: $(this).data('req-msg'),
    }
    console.log(Req)
    modal.find('.modal-header #ad-name').text(Req.ad_name);
    modal.find('.modal-body #camp-name').text(Req.Campaign_name);
    modal.find('.modal-body #req-name').text(Req.requestor_name);
    modal.find('.modal-body #res-name').text(Req.responser_name);
    modal.find('.modal-body #status').text(Req.status);
    modal.find('.modal-body #terms').text(Req.terms);
    modal.find('.modal-body #payment-amt').text(Req.payment_amt);
    modal.find('.modal-body #req-msg').text(Req.your_msg)
    modal.find('.modal-body #res-msg').text(Req.msg_recieved);

    console.log('Attempting to show modal:', modalId);
    modal.modal('show');
  })
})

//edit modals



  
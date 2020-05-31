from django.conf.urls import url

from . import view

urlpatterns = [

    url(r'^$', view.index),
    url('covid_daily_increasement/', view.covid_daily_increasement),
    url('covid_daily_increasement/customized', view.page_covid_daily_increasement_customized),

    url('china_map/', view.china_map),
    url('covid_daily_update_themeRiver/', view.covid_daily_update_themeRiver),
    url('covid_daily_update_themeRiver/customized', view.covid_daily_update_themeRiver_customized),  # page for user entered range


    url('admin/', view.admin),
    url('log/', view.read_log),
    #url('subscription_list/', view.subscription_list),

]

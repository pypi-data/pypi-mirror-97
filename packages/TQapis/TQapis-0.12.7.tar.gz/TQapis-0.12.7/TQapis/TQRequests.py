"""
Prepares TQ Request Instance with a configuration to hit 
Corresponding API endpoint for a request_Method.
They replalce the key:value pair dictionary for each API with functions and arguments.

Eg (GET method):
request_ip_return(): http://operations.treasuryquants.com/?function_name=ip_return

GitHub Description:
    Contains all the functions that build the request parameters.
"""


# TreasuryQuants.com Ltd.
# email: contact@treasuryquants.com
# Note: this software is provided "as-is" under the agreed terms of your account.
#       For more information see https://treasuryquants.com/terms-of-services/


class Request:
    def __init__(self, params, needs_token=True):
        """
        Initializes TQ Request Class Object

        Args:
            params: Type[dict]
            needs_token: Type[bool]
        """
        self.params = params
        self.needs_token = needs_token


class ParamBuilder:
    _function_name = 'function_name'

    def build(self, params, function_name, needs_token=True):
        """
        Args:
            params: Type[dict]
            function_name: Type[str], function-API-endpoint
            needs_token: Type[bool]

        Returns:
            Type[TQ Request]
        """
        params[self._function_name] = function_name
        return Request(params, needs_token)


#
# initialization to get our IP and at the same time check if we can have connection
#
def request_ip_return():
    """
    Returns:
        Type[Request] (TQ Request Class Object), contains attributes: Type[dict] `params` and `needs_token`
    """
    request_collection = {}
    params = ParamBuilder().build(request_collection, function_name='ip_return', needs_token=False)
    return params


#
# Account related function calls
#


#
# to ensure the status of the user account.
#
def request_account_status(email):
    """
    Returns:
        Type[Request] (TQ Request Class Object), contains attributes: Type[dict] `params` and `needs_token`
    """
    params = {"email": str(email),}
    return ParamBuilder().build(params, function_name='account_status', needs_token=False)


#
# This is the FIRST step of the two-step process for creating a new account.
# For the second step see request_account_reset.
#
def request_account_create(email,password="", ip='127.0.0.1', callback_url="",
                                                           is_test=False):
    params = {"email": str(email),"password": str(password), 'ip':str(ip), 'url':str(callback_url), 'is_test':str(is_test)}
    return ParamBuilder().build(params, function_name='account_create', needs_token=False)

#
# request for regeneration of the activation key, for either activating the account or resetting password
#
def request_account_send_activation_key(email, callback_url="", is_test=False):
    params = {"email": str(email),  'url': str(callback_url), 'is_test': str(is_test)}
    return ParamBuilder().build(params, function_name='account_send_activation_key', needs_token=False)


#
# request for activating an account using activation_key
#
def request_account_activate( activation_key, is_test=False):
    params = {  'activation_key': str(activation_key), 'is_test': str(is_test)}
    return ParamBuilder().build(params, function_name='account_activate', needs_token=False)



#
# request for changing password.
#
def request_account_password_change(email, password,new_password, is_test=False):
    params = {"email": str(email),  'password': str(password),  'new_password': str(new_password), 'is_test': str(is_test)}
    return ParamBuilder().build(params, function_name='account_password_change', needs_token=False)



#
# request for changing IP.
#
def request_account_ip_change(email, password,new_ip, is_test=False):
    params = {"email": str(email),  'password': str(password),  'new_ip': str(new_ip), 'is_test': str(is_test)}
    return ParamBuilder().build(params, function_name='account_ip_change', needs_token=False)

#
# request for password and IP change.
#
def request_account_password_ip_change(email, password,new_password,new_ip, is_test=False):
    params = {"email": str(email),'new_password':str(new_password),  'password': str(password),  'new_ip': str(new_ip), 'is_test': str(is_test)}
    return ParamBuilder().build(params, function_name='account_password_ip_change', needs_token=False)

#
# request for password reset
#
def request_account_password_reset( activation_key,new_password, is_test=False):
    params = {  'activation_key': str(activation_key),  'new_password': str(new_password), 'is_test': str(is_test)}
    return ParamBuilder().build(params, function_name='account_password_reset', needs_token=False)


def request_account_reset(activation_key, email, password, ip, is_test=False):
    params = {"email": email, 'activation_key': activation_key, 'password': password, 'ip': ip, 'is_test': str(is_test)}
    return ParamBuilder().build(params, function_name='account_reset', needs_token=False)


def request_account_activation_key_status(activation_key):
    params = { 'activation_key': activation_key}
    return ParamBuilder().build(params, function_name='account_activation_key_status', needs_token=False)

#
# request to get user profile
#
def request_account_profile(email, password):
    params = {"email": str(email),  'password': str(password)}
    return ParamBuilder().build(params, function_name='account_profile', needs_token=False)




#
# General functions
#


#
# requests for a new token. The expiry of the new token is inside the xml result for each and individual result.
#
def request_account_token_create(email):
    """
    Returns:
        Type[TQ Request], Request Instance configured to hit API /?function_name=account_token_create Endpoint.
    """
    params = {"email": email}
    return ParamBuilder().build(params, function_name='account_token_create', needs_token=False)


def request_function_describe(item_name=""):
    params = {}
    if len(item_name.lstrip()) > 0:
        params = {'element': item_name}
    return ParamBuilder().build(params, 'describe')


def request_function_show_available(item_name=""):
    params = {}
    if len(item_name.lstrip()) > 0:
        params = {'element': item_name}
    return ParamBuilder().build(params, 'show_available')

    # workspace_show_files and workspace_delete_file use the same API workspace


def request_function_workspace_show_files():
    params = {'list': 'all'}
    return ParamBuilder().build(params, 'workspace')

    # workspace_show_files and workspace_delete_file use the same API workspace


def request_function_workspace_delete_file(file_name):
    params = {'delete': file_name}
    return ParamBuilder().build(params, 'workspace')


def request_function_market_swap_rates(asof, currency):
    params = {'asof': asof, 'currency': currency}
    return ParamBuilder().build(params, 'market_swap_rates')

def request_function_formatted_grid_swap_rates(from_date,to_date, currency):
    params = {'from_date':from_date,'to_date': to_date, 'currency': currency}
    return ParamBuilder().build(params, 'formatted_grid_swap_rates')

def request_function_formatted_grid_fx(base_date,base_currency):
    params = {'base_date':base_date, 'base_currency':base_currency}
    return ParamBuilder().build(params, 'formatted_grid_fx')


def request_function_market_fx_rates(asof, to_date, base_currency):
    params = {'asof': asof, 'base_currency': base_currency, 'to_date': to_date}
    return ParamBuilder().build(params, 'market_fx_rates')


def request_function_price_vanilla_swap(
        asof
        , type
        , notional
        , trade_date
        , trade_maturity
        , index_id
        , discount_id
        , floating_leg_period
        , fixed_leg_period
        , floating_leg_daycount
        , fixed_leg_daycount
        , fixed_rate
        , is_payer
        , spread
        , business_day_rule
        , business_centres
        , spot_lag_days
        , save_as=""):
    params = {
        "asof": str(asof)
        , "type": type
        , "notional": str(notional)
        , "trade_date": str(trade_date)
        , "trade_maturity": str(trade_maturity)
        , "index_id": index_id
        , "discount_id": discount_id
        , "floating_leg_period": floating_leg_period
        , "fixed_leg_period": fixed_leg_period
        , "floating_leg_daycount": floating_leg_daycount
        , "fixed_leg_daycount": fixed_leg_daycount
        , "fixed_rate": str(fixed_rate)
        , "is_payer": str(is_payer).lower()
        , "spread": str(spread)
        , "business_day_rule": business_day_rule
        , "business_centres": business_centres
        , "spot_lag_days": str(spot_lag_days)}
    if len(save_as.lstrip()) > 0:
        params['save_as'] = save_as
    return ParamBuilder().build(params, 'price_vanilla_swap')


def request_function_price_fx_forward(
        asof
        , type
        , trade_date
        , trade_expiry
        , pay_amount
        , pay_currency
        , receive_amount
        , receive_currency
        , save_as=""):
    params = {
        "asof": str(asof)
        , "type": type.lower()
        , "trade_date": str(trade_date)
        , "trade_expiry": str(trade_expiry)
        , "pay_amount": str(pay_amount)
        , "pay_currency": pay_currency.lower()
        , "receive_amount": str(receive_amount)
        , "receive_currency": receive_currency.lower()}
    if len(save_as.lstrip()) > 0:
        params['save_as'] = save_as
    return ParamBuilder().build(params, 'price_fx_forward')


def request_function_price(asof, load_as):
    params = {'asof': asof, 'load_as': load_as}
    return ParamBuilder().build(params, 'price')


def request_function_risk_ladder(asof, load_as):
    params = {'asof': asof, 'load_as': load_as}
    return ParamBuilder().build(params, 'risk_ladder')


def request_function_pnl_predict(load_as, from_date, to_date):
    params = {'load_as': load_as, 'from_date': from_date, 'to_date': to_date}
    return ParamBuilder().build(params, 'pnl_predict')


def request_function_pnl_attribute(load_as, from_date, to_date):
    params = {'load_as': load_as, 'from_date': from_date, 'to_date': to_date}
    return ParamBuilder().build(params, 'pnl_attribute')


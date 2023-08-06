import datetime
import tdxlib.tdx_integration
from tdxlib.tdx_api_exceptions import *


class TDXAssetIntegration(tdxlib.tdx_integration.TDXIntegration):
    def __init__(self, filename=None):
        tdxlib.tdx_integration.TDXIntegration.__init__(self, filename)
        if self.asset_app_id is None:
            raise ValueError("Asset App Id is required. Check your INI file for 'assetappid = 000'")
        self.clean_cache()

    def clean_cache(self):
        super().clean_cache()
        self.cache['product_model'] = {}
        self.cache['product_type'] = {}
        self.cache['vendor'] = {}
        self.cache['asset_form'] = {}
        self.cache['asset_status'] = {}
        self.cache['custom_attributes'] = self.get_all_custom_attributes(
            tdxlib.tdx_integration.TDXIntegration.component_ids['asset'], app_id=self.asset_app_id)
        self.cache['custom_attributes'].append(self.get_all_custom_attributes(
            tdxlib.tdx_integration.TDXIntegration.component_ids['configuration_item'], app_id=self.asset_app_id))

    def _make_asset_call(self, url, action, post_body=None):
        url_string = '/' + str(self.asset_app_id) + '/assets'
        if len(url) > 0:
            url_string += '/' + url
        if action == 'get':
            return self.make_get(url_string)
        if action == 'delete':
            return self.make_delete(url_string)
        if action == 'post' and post_body:
            return self.make_post(url_string, post_body)
        if action == 'put' and post_body:
            return self.make_put(url_string, post_body)
        if action == 'patch' and post_body:
            return self.make_patch(url_string, post_body)
        raise TdxApiHTTPRequestError('No method' + action + 'or no post information')

    def make_call(self, url, action, post_body=None):
        """
        Makes an HTTP call using the Assets API information.

        :param url: The URL (everything after assets/) to call
        :param action: The HTTP action (get, put, post, delete, patch) to perform.
        :param post_body: A python dict of the information to post, put, or patch. Not used for get/delete.

        :return: the API's response as a python dict or list

        """
        return self._make_asset_call(url, action, post_body)

    # TODO: Move this down to a more logical place
    def get_asset_custom_attribute_by_name_id(self, key: str) -> dict:
        """
        Gets a specific Asset Custom Attribute object

        :param key: name or id of the Custom Attribute. This must be the exact name, no partial searching.

        :return: dict of custom attribute data

        """
        search_key = str(key) + "_asset_ci"
        if search_key in self.cache['ca_search']:
            return self.cache['ca_search'][search_key]
        # There is no API for searching attributes -- the only way is to get them all.
        for item in self.cache['custom_attributes']:
            if type(item) == dict:
                if str(key).lower() == item['Name'].lower() or str(key) == str(item['ID']):
                    self.cache['ca_search'][search_key] = item
                    return item
        raise TdxApiObjectNotFoundError(
            "No custom asset or CI attribute found for " + str(key))

    def get_all_asset_forms(self) -> list:
        """
        Gets a list asset forms

        :return: list of form data

        """
        return self.make_call('forms', 'get')
        
    def get_asset_form_by_name_id(self, key: str) -> dict:
        """
        Gets a specific asset form object

        :param key: name of AssetForm to search for

        :return: list of form data

        """
        if not self.cache['asset_form']:
            self.cache['asset_form'] = self.get_all_asset_forms()
        for asset_form in self.cache['asset_form']:
            if str(key).lower() in asset_form['Name'].lower():
                return asset_form
            if str(asset_form['ID']).lower() == str(key):
                return asset_form
        raise TdxApiObjectNotFoundError(
            "No asset form found for " + str(key))

    def get_all_asset_statuses(self) -> list:
        """
        Gets a list asset statuses

        :return: list of status data

        """
        return self.make_call('statuses', 'get')

    def get_asset_status_by_name_id(self, key: str) -> dict:
        """
        Gets a specific asset status object

        :param key: name of an asset status to search for

        :return: dict of status data

        """
        if not self.cache['asset_status']:
            self.cache['asset_status'] = self.get_all_asset_statuses()
        for status in self.cache['asset_status']:
            if status['Name'].lower() == str(key).lower() or str(status['ID']) == str(key):
                return status
        raise TdxApiObjectNotFoundError(f'No asset status found for {str(key)}')

    # TODO: def update_asset_status(self, updated_values)-> dict:
    # TODO: def create_asset_status(self, params)-> dict:

    def get_all_product_types(self) -> list:
        """
        Gets a list of all product types

        :return: list of product type data

        """
        type_list = self.make_call("models/types", 'get')
        for this_type in type_list:
            for sub in this_type['Subtypes']:
                type_list.append(sub)
        return type_list

    # TODO: Provide option for lower memory use by allowing use of search instead of getting all.
    def get_product_type_by_name_id(self, key: str) -> dict:
        """
        Gets a specific product type object

        :param key: name of product type to search for

        :return: dict of product type data

        """
        if not self.cache['product_type']:
            self.cache['product_type'] = self.get_all_product_types()
        for product_type in self.cache['product_type']:
            if str(key).lower() == product_type['Name'].lower() or str(product_type['ID']) == str(key):
                return product_type
        raise TdxApiObjectNotFoundError(f'No product type found for {str(key)}')

    def create_product_type(self, name: str, description: str = None, parent=None, order: int = 1,
                            active: bool = True)-> dict:
        """
        Creates a new Product Type with the information provided.

        :param name: The name of the new product type
        :param description: A description of the type (optional)
        :param parent: A Type (dict) or Type ID to set as the parent type of this type (creates a subtype)(optional)
        :param order: Sort order for this type (optional, defaults to 1)
        :param active: Boolean indicating whether or not the new type should be active (optional, default True)

        :return: dict of created product type

        """

        data = {'Name': name, 'IsActive': active, 'Order': order}
        if parent:
            if isinstance(parent, dict) and 'ID' in parent.keys():
                data['ParentID'] = parent['ID']
            else:
                data['ParentID'] = parent
        if description:
            data['Description'] = description
        return self.make_call('models/types', 'post', data)

    def update_product_type(self, product_type, updated_values: dict)-> dict:
        """
        Updates an existing product type

        :param product_type: Type (dict) or Type ID to edit
        :param updated_values: dict of values that should be changed

        :return: dict of edited product type

        """
        if isinstance(product_type, dict):
            product_type = product_type
        else:
            product_type = self.get_product_type_by_name_id(product_type)
        editable_type_values = ['Name', 'Description', 'ParentID', 'IsActive', 'Order']
        for i in updated_values.keys():
            if i not in editable_type_values:
                raise TdxApiObjectTypeError(f'Account attribute {i} is not editable')
        product_type.update(updated_values)
        product_type_id = product_type['ID']
        return self.make_call(f'models/types/{product_type_id}', 'put', product_type)

    def search_product_types(self, search_string: str = '*', active: bool = True, root_only: bool = False,
                             parent=None)-> list:
        """
        Searches product types by parent, text, or parent.

        :param search_string: String to search by name/description
        :param active: Boolean, when true, searches only active product types
        :param root_only: Boolean, when true, limits search to only top-level product types
        :param parent: Name or ID of parent type. Limits search to children of that parent

        :return: list of product types as dicts

        """
        parent_id = ''
        if parent:
            if isinstance(parent, dict) and 'ID' in parent.keys():
                parent_id = parent['ID']
            else:
                parent_id = self.get_product_type_by_name_id(parent)['ID']
        search_data = {'SearchText': search_string, 'IsActive': active, 'IsTopLevel': root_only,
                       'ParentProductTypeID': parent_id}
        post_data = {'search': search_data}
        return self.make_call(f'models/types/search', 'post', post_data)

    def get_all_product_models(self) -> list:
        """
        Gets a list asset models

        :return: list of model data

        """
        return self.make_call("models", 'get')

    # TODO: Provide option for lower memory use by allowing use of search instead of getting all.
    def get_product_model_by_name_id(self, key: str) -> dict:
        """
        Gets a specific product model object

        :param key: name of product model to search for

        :return: dict of model data

        """
        if not self.cache['product_model']:
            self.cache['product_model'] = self.get_all_product_models()
        for product_model in self.cache['product_model']:
            if str(key).lower() in product_model['Name'].lower() or str(product_model['ID']) == str(key):
                return product_model
        raise TdxApiObjectNotFoundError(f'No product model found for {str(key)}')

    def get_all_product_models_of_type(self, product_type) -> list:
        """
        Get all product models of a specific type

        :param product_type: dict, name, or ID of a product type

        :return: list of product models of that type
        """
        result = []
        if isinstance(product_type, str):
            product_type = self.get_product_type_by_name_id(product_type)
        if not isinstance(product_type, dict):
            raise TdxApiObjectTypeError("Can't search assets with type" +
                                        str(type(product_type)) + " as department.")
        children_ids = [x['ID'] for x in self.search_product_types(parent=product_type)]
        models = self.get_all_product_models()
        for model in models:
            if str(model['ProductTypeID']) == str(product_type['ID']) or str(model['ProductTypeID']) in children_ids:
                result.append(model)
        return result

    def create_product_model(self, name: str, product_type, source: str, description: str = None,
                             part_number: str = None, active: bool = True, attributes: dict= None) -> dict:
        """
        Creates a new Product Model with the information provided.

        :param name: The name of the new product model
        :param product_type: A Type (dict) or Type ID to set as the product type of this model
        :param source: The manufacturer or vendor the model is sourced from
        :param description: A description of the model (optional)
        :param part_number: Part number for this model (optional)
        :param active: Boolean indicating whether or not the new model should be active (optional, default True)
        :param attributes: Dict of custom attributes to set on the new model (no validation yet -- build this by hand)

        :return: dict of created product type

        """

        data = {'Name': name, 'IsActive': active}
        if isinstance(source, dict) and 'ID' in source.keys():
            data['ManufacturerID'] = source['ID']
        else:
            data['ManufacturerID'] = self.get_vendor_by_name_id(source)['ID']
        if isinstance(product_type, dict) and 'ID' in product_type.keys():
            data['ProductTypeID'] = product_type['ID']
        else:
            data['ProductTypeID'] = self.get_product_type_by_name_id(product_type)['ID']
        if attributes:
            data['Attributes'] = attributes
        if part_number:
            data['PartNumber'] = part_number
        if description:
            data['Description'] = description
        return self.make_call('models', 'post', data)

    # TODO: def update_product_model(self, updated_values)-> dict:

    def get_all_vendors(self) -> list:
        """
        Gets a list vendors

        :return: list of vendor data

        """
        return self.make_call("vendors", 'get')

    # TODO: Provide option for lower memory use by allowing use of search instead of getting all.
    def get_vendor_by_name_id(self, key):
        """
        Gets a specific vendor object

        :param key: name or ID of vendor to search for

        :return: dict of vendor data

        """
        if not self.cache['vendor']:
            self.cache['vendor'] = self.get_all_vendors()
        for vendor in self.cache['vendor']:
            if str(key).lower() in vendor['Name'].lower() or str(vendor['ID']) == str(key):
                return vendor
        raise TdxApiObjectNotFoundError(f'No vendor found for {str(key)}')

    # TODO: def update_vendor(self, updated_values)-> dict:
    # TODO: def search_vendor(self, key, etc) -> list:

    def create_vendor(self, name, email: str = None, description: str = None, account_number: str = None,
                      additional_info: dict = None, active=True) -> dict:

        """
       Creates a new Vendor with the information provided.

       :param name: The name of the new product model
       :param email: An email contact for the new vendor (optional)
       :param description: A description of the model (optional)
       :param account_number: An account number with the vendor (optional)
       :param active: Boolean indicating whether or not the new vendor should be active (optional, default True)
       :param additional_info: Dict of other info for the vendor (including CAs, no validation yet -- build by hand)

       :return: dict of created product type

       """

        data = {'Name': name, 'IsActive': active}
        if additional_info:
            data.update(additional_info)
        if email:
            data['ContactEmail'] = email
        if account_number:
            data['AccountNumber'] = account_number
        if description:
            data['Description'] = description
        return self.make_call('vendors', 'post', data)

    # TODO: def delete_vendor(self)-> dict:

    def get_asset_by_id(self, asset_id: str) -> dict:
        """
        Gets a specfic asset object, including the full list of attributes.

        :param asset_id: asset ID from TDX

        :return: dict of asset data

        """
        return self.make_call(str(asset_id), 'get')

    def search_assets(self, criteria, max_results=25, retired=False, disposed=False, full_record=False) -> list:
        """
        Searches for assets, based on criteria

        Common criteria to put in dict:
        {'SerialLike': [List of Int],
        'SearchText': [String],
        'StatusIDs': [List of Int],
        'CustomAttributes': [Dict of CA],
        'ParentIDs': [List of Int]}
        (https://api.teamdynamix.com/TDWebApi/Home/type/TeamDynamix.Api.Assets.AssetSearch)

        :param max_results: maximum number of results to return
        :param criteria: a string or dict to search for tickets with. If a string, use as 'SearchString'
        :param retired: include retired assets in search if true
        :param disposed: include disposed assets in search if true
        :param full_record: get full asset record (Default: False). Takes more time, but returns full asset record(s)

        :return: list of asset info (by default, NOT FULL ASSET RECORDS, pass full_record=True to get full record)
        
        """
        # Set default statuses
        statuses = list()
        statuses.append(self.get_asset_status_by_name_id("Inventory")['ID'])
        statuses.append(self.get_asset_status_by_name_id("In Use")['ID'])
        statuses.append(self.get_asset_status_by_name_id("Broken")['ID'])

        # Set conditional statuses
        if retired:
            statuses.append(self.get_asset_status_by_name_id("Retired")['ID'])
        if disposed:
            statuses.append(self.get_asset_status_by_name_id("Disposed")['ID'])

        # Set up search body
        search_body = {'MaxResults': str(max_results), 'StatusIDs': statuses}
        if isinstance(criteria, str):
            search_body['SearchText'] = criteria
        elif isinstance(criteria, dict):
            search_body.update(criteria)
        else:
            raise TdxApiObjectTypeError("Can't search assets with" +
                                        str(type(criteria)) + " as criteria.")
        asset_list = self.make_call('search', 'post', search_body)
        if full_record:
            full_assets = []
            for asset in asset_list:
                full_assets.append(self.get_asset_by_id(asset['ID']))
            return full_assets
        else:
            return asset_list

    def find_asset_by_tag(self, tag, full_record: bool = False) -> dict:
        """
        Gets an asset based on its asset tag

        :param tag: asset tag as a string or int
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info


        :return: the single asset with the corresponding tag

        """
        if type(tag) is str:
            tag = tag.lstrip('0')
        search_params = {'SearchText': str(tag)}
        result = self.search_assets(search_params, disposed=True, retired=True, full_record=full_record)
        if result and len(result) == 1:
            return result[0]
        else:
            for asset in result:
                if asset['Tag'] == tag:
                    return asset
        raise TdxApiObjectNotFoundError(
            f"{str(len(result))} assets with tag {str(tag)} found.")

    def find_asset_by_sn(self, sn, full_record: bool = False) -> dict:
        """
        Gets an asset based on its serial number

        :param sn: serial number as a string or int
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info

        :return: the single asset with the corresponding serial number

        """
        search_params = {'SerialLike': sn}
        result = self.search_assets(search_params, disposed=True, retired=True, full_record=full_record)
        if len(result) == 1:
            return result[0]
        raise TdxApiObjectNotFoundError(
            f"{str(len(result))} assets with SN {str(sn)} found.")

    def get_assets_by_location(self, location, max_results: int = 5000, full_record: bool = False,
                               retired: bool = False, disposed: bool = False) -> list:
        """
        Gets all assets in a location

        :param location: a single location (from get_location_by_name()) or list of same
        :param max_results: an integer indicating the maximum number of results that should be returned (default: 25)
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info
        :param retired: include retired assets in search if true
        :param disposed: include disposed assets in search if true

        :return: a list of assets in the location(s)

        """
        id_list = list()
        if isinstance(location, list):
            for this_location in location:
                if isinstance(this_location, dict):
                    id_list.append(this_location['ID'])
                if isinstance(this_location, str):
                    id_list.append(self.get_location_by_name(this_location)['ID'])
        elif isinstance(location, dict):
            id_list.append(location['ID'])
        elif isinstance(location, str):
            id_list.append(self.get_location_by_name(location)['ID'])
        return self.search_assets({'LocationIDs': id_list}, max_results=max_results, full_record=full_record,
                                  disposed=disposed, retired=retired)

    def get_assets_by_room(self, room: dict, max_results: int = 25, full_record: bool = False,
                           retired: bool = False, disposed: bool = False) -> list:
        """
        Gets all assets in a specific room in a location

        :param room: a single room (from get_room_by_name())
        :param max_results: an integer indicating the maximum number of results that should be returned (default: 25)
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info
        :param retired: include retired assets in search if true
        :param disposed: include disposed assets in search if true

        :return: a list of assets in the room

        """
        return self.search_assets({'RoomID': room['ID']}, max_results=max_results, full_record=full_record,
                                  disposed=disposed, retired=retired)

    def get_assets_by_owner(self, person: str, max_results: int = 25, full_record: bool = False,
                            retired: bool = False, disposed: bool = False) -> list:
        """
        Gets all assets owned by a particular person in TDX

        :param person: the name or email of a person in TDX, or a dict containing their information
        :param max_results: an integer indicating the maximum number of results that should be returned (default: 25)
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info
        :param retired: include retired assets in search if true
        :param disposed: include disposed assets in search if true

        :return: a list of assets owned by that person

        """
        if isinstance(person, str):
            person = self.get_person_by_name_email(person)
        if not isinstance(person, dict):
            raise TdxApiObjectTypeError("Can't search assets with type" +
                                        str(type(person)) + " as person.")
        return self.search_assets({'OwningCustomerIDs': [person['UID']]},
                                  max_results=max_results, full_record=full_record,
                                  disposed=disposed, retired=retired)

    def get_assets_by_requesting_department(self, dept, max_results: int = 25, full_record: bool = False,
                                            retired: bool = False, disposed: bool = False) -> list:
        """
        Gets all assets requested by a particular account/department in TDX

        :param dept: the name or email of a account/department, or a dict containing its information
        :param max_results: an integer indicating the maximum number of results that should be returned (default: 25)
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info
        :param retired: include retired assets in search if true
        :param disposed: include disposed assets in search if true

        :return: a list of assets requested by that department

        """
        if isinstance(dept, str):
            dept = self.get_account_by_name(dept)
        if not isinstance(dept, dict):
            raise TdxApiObjectTypeError("Can't search assets with type" +
                                        str(type(dept)) + " as department.")
        return self.search_assets({'RequestingDepartmentIDs': [dept['ID']]},
                                  max_results=max_results, full_record=full_record,
                                  disposed=disposed, retired=retired)

    def get_assets_by_product_model(self, model, max_results: int = 25, full_record: bool = False,
                                    retired: bool = False, disposed: bool = False) -> list:
        """
        Gets all assets of a certain product model

        :param model: the name or ID of a product model, or a dict of same
        :param max_results: an integer indicating the maximum number of results that should be returned (default: 25)
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info
        :param retired: include retired assets in search if true
        :param disposed: include disposed assets in search if true

        :return: a list of assets of the specified model

        """
        if isinstance(model, str):
            model = self.get_product_model_by_name_id(model)
        if not isinstance(model, dict):
            raise TdxApiObjectTypeError("Can't search assets with type" +
                                        str(type(model)) + " as model.")
        return self.search_assets({'ProductModelIDs': [model['ID']]},
                                  max_results=max_results, full_record=full_record,
                                  disposed=disposed, retired=retired)

    def get_assets_by_product_type(self, product_type, max_results: int = 25, full_record: bool = False,
                                   retired: bool = False, disposed: bool = False) -> list:
        """
        Gets all assets of a certain product type

        :param product_type: the name or ID of a product type, or a dict of same
        :param max_results: an integer indicating the maximum number of results that should be returned (default: 25)
        :param full_record: boolean indicating whether to fetch the full Asset record, or just summary info
        :param retired: include retired assets in search if true
        :param disposed: include disposed assets in search if true

        :return: a list of assets of the specified type

        """
        if isinstance(product_type, str):
            product_type = self.get_product_type_by_name_id(product_type)
        if not isinstance(product_type, dict):
            raise TdxApiObjectTypeError("Can't search assets with type" +
                                        str(type(product_type)) + " as model.")
        models = self.get_all_product_models_of_type(product_type)
        model_ids = [x['ID'] for x in models]
        return self.search_assets({'ProductModelIDs': model_ids},
                                  max_results=max_results, full_record=full_record,
                                  disposed=disposed, retired=retired)

    def update_assets(self, assets, changed_attributes: dict, clear_custom_attributes=False) -> list:
        """
        Updates data in a list of assets

        :param assets: a list of assets (maybe from search_assets()) or a single asset (only ID required)
        :param changed_attributes: a dict of attributes in the ticket to be changed
        :param clear_custom_attributes: (default: False) Indicates whether or not custom attributes should be cleared

        :return: list of updated assets

        """
        changed_custom_attributes = False
        if not isinstance(assets, list):
            asset_list = list()
            asset_list.append(assets)
        else:
            asset_list = assets
        updated_assets = list()
        if 'Attributes' in changed_attributes:
            if isinstance(changed_attributes['Attributes'], list):
                changed_custom_attributes = changed_attributes['Attributes']
            else:
                changed_custom_attributes = [changed_attributes['Attributes']]
            del changed_attributes['Attributes']
        for this_asset in asset_list:
            this_asset = self.get_asset_by_id(this_asset['ID'])
            if 'Attributes' not in this_asset.keys():
                this_asset['Attributes'] = []
            if changed_custom_attributes and not clear_custom_attributes:
                for new_attrib in changed_custom_attributes:
                    new_attrib_marker = True
                    for attrib in this_asset['Attributes']:
                        if str(new_attrib['ID']) == str(attrib['ID']):
                            attrib['Value'] = new_attrib['Value']
                            new_attrib_marker = False
                    if new_attrib_marker:
                        this_asset['Attributes'].append(new_attrib)
            if clear_custom_attributes:
                this_asset['Attributes'] = []
            this_asset.update(changed_attributes)
            updated_assets.append(self.make_call(str(this_asset['ID']), 'post', this_asset))
        return updated_assets

    def change_asset_owner(self, asset, new_owner, new_dept=None) -> list:
        """
        Updates owner data in a list of assets

        :param asset: asset to update (doesn't have to be full record), or list of same
        :param new_owner: email or name of new owner, or dict of their information
        :param new_dept: name of new department, or dict of information

        :return: list of the updated assets

        """
        if isinstance(new_owner, str):
            new_owner_uid = self.get_person_by_name_email(new_owner)['UID']
        elif isinstance(new_owner, dict):
            new_owner_uid = new_owner['UID']
        else:
            raise TdxApiObjectTypeError(
                f"New Owner of type {str(type(new_dept))} not searchable."
            )
        changed_attributes = {'OwningCustomerID': new_owner_uid}
        if new_dept:
            if isinstance(new_dept, str):
                changed_attributes['OwningDepartmentID'] = self.get_account_by_name(new_dept)['ID']
            elif isinstance(new_dept, dict):
                changed_attributes['OwningDepartmentID'] = new_dept['ID']
            else:
                raise TdxApiObjectTypeError(
                    f"Department of type {str(type(new_dept))} not searchable."
                )
        return self.update_assets(asset, changed_attributes)

    def change_asset_requesting_dept(self, asset, new_dept)-> list:
        """
        Updates Requesting Department data in a list of assets

        :param asset: asset to update (doesn't have to be full record), or list of same
        :param new_dept: name of new department

        :return: list of the updated assets

        """
        changed_attributes = dict()
        if isinstance(new_dept, str):
            changed_attributes['RequestingDepartmentID'] = self.get_account_by_name(new_dept)['ID']
        elif isinstance(new_dept, dict):
            changed_attributes['RequestingDepartmentID'] = new_dept['ID']
        else:
            raise TdxApiObjectTypeError(
                f"Department of type {str(type(new_dept))} not searchable."
            )
        return self.update_assets(asset, changed_attributes)

    def build_asset_custom_attribute_value(self, custom_attribute, value) -> dict:
        """
        Builds a custom attribute for an asset from the name of the attribute and value.

        :param custom_attribute: name of custom attribute (or dict of info)
        :param value: name of value to set, or value to set to

        :return: list of updated assets in dict format (for use in change_custom_attribute_value())

        """
        if isinstance(custom_attribute, str) or isinstance(custom_attribute, int):
            ca = self.get_asset_custom_attribute_by_name_id(str(custom_attribute))
        elif isinstance(custom_attribute, dict):
            ca = custom_attribute
        else:
            raise TdxApiObjectTypeError(
                f"Custom Attribute of type {str(type(custom_attribute))} not searchable."
            )
        if len(ca['Choices']) > 0:
            ca_choice = self.get_custom_attribute_choice_by_name_id(ca, value)
            value = ca_choice['ID']
        return {'ID': ca['ID'], 'Value': value}

    def change_asset_custom_attribute_value(self, asset, custom_attributes: list) -> list:
        """
        Takes a correctly formatted list of CA's (from build_asset_custom_attribute_value, for instance)
        and updates one or more assets with the new values.

        :param asset: asset to update (doesn't have to be full record), or list of same
        :param custom_attributes: List of ID/Value dicts (from build_asset_custom_attribute_value())
        :return: list of updated assets in dict format
        """
        to_change = {'Attributes': custom_attributes}
        return self.update_assets(asset, to_change)

    def move_child_assets(self, source_asset: dict, target_asset: dict) -> list:
        """
        Moves child assets from one parent asset to another

        :param source_asset: asset to move children from (doesn't have to be full record)
        :param target_asset: asset to move children to

        :return: list of the updated assets

        """
        search_params = {'ParentID': source_asset['ID']}
        update_params = {'ParentID': target_asset['ID']}
        children = self.search_assets(search_params)
        return self.update_assets(children, update_params)

    def copy_asset_attributes(self, source_asset, target_asset, copy_name=False, exclude=None, new_status: str = None):
        """
        Copies asset attributes from one asset to another. Does not include attributes like Serial Number, Asset Tag,
            and other hardware-specific fields.

        :param source_asset: asset to copy attributes from (doesn't have to be full record)
        :param target_asset: asset to copy attributes to (doesn't have to full record) This asset will be OVERWRITTEN!
        :param copy_name: Set to true to copy the name of the source asset to the target asset
        :param exclude: List of attributes to be excluded, in addition to defaults
        :param new_status: Name or ID of new status for source asset

        :return: list of the target and source asset data

        """
        excluded_attributes = ['SerialNumber', 'Tag', 'ExternalID', 'ModelID', 'SupplierID', 'ManufacturerID',
                               'PurchaseCost', 'ExpectedReplacementDate', 'AcquisitionDate']
        if exclude:
            excluded_attributes.append(exclude)
        if not copy_name:
            excluded_attributes.append('Name')
        full_source = dict(self.get_asset_by_id(source_asset['ID']))
        for protected_attribute in excluded_attributes:
            full_source.pop(protected_attribute, None)
        updated_target = self.update_assets(target_asset, full_source)
        updated_source = None
        if new_status:
            update_params = {'StatusID': self.get_asset_status_by_name_id(new_status)}
            updated_source = self.update_assets(full_source, update_params)
        return [updated_target, updated_source]

    def build_asset(self, asset_name, serial_number, status_name, location_name=None, room_name=None,
                    asset_tag=None, acquisition_date=None, asset_lifespan=None, requester=None,
                    requesting_dept=None, owner=None, owning_dept=None, parent=None, external_id=None,
                    product_model=None, form=None, asset_custom_attributes=None):
        """
        Makes a correctly-formatted dict of asset attributes for inputting into create_asset() function

        :param asset_name: a string containing the name for the asset
        :param serial_number: String with serial number of new asset
        :param status_name: String with name of status of new asset
        :param location_name: String with name of location for new asset (optional)
        :param room_name: String with name of room for new asset (optional, requires location_name)
        :param asset_tag: String with asset tag value for new asset (optional)
        :param acquisition_date: Building name of location (Default: date of execution)
        :param asset_lifespan: Years you expect this device to be in service (Default: 4)
        :param requester: String with email of requester for new asset (Default: integration username)
        :param requesting_dept: Account Name of requesting department for new asset
        :param owner: String with Email of owner of new asset
        :param owning_dept: String with Account name of owning department
        :param parent: Int with ID or String with serial number of a parent asset. Parent Asset must already exist.
        :param external_id: String with external id for new asset (Default: serial Number)
        :param product_model: String with name of product model
        :param form: Name of the Asset form to use
        :param asset_custom_attributes: a dictionary of asset custom attribute values

        :return: dict usable in create_asset()

        """
        # set defaults
        if not acquisition_date:
            acquisition_date = datetime.datetime.today()
        if not requester:
            requester = self.username
        if not external_id:
            external_id = serial_number

        # Required or defaulted parameters
        data = dict()
        data['Name'] = asset_name
        data['SerialNumber'] = serial_number
        data['StatusID'] = self.get_asset_status_by_name_id(status_name)['ID']
        data['AcquisitionDate'] = acquisition_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        data['ExternalID'] = external_id

        # map per-ticket values into title and body

        # set up attribute values
        if asset_custom_attributes:
            data['Attributes'] = []
            for attrib_name, value in asset_custom_attributes.items():
                new_attrib = self.build_asset_custom_attribute_value(attrib_name, value)
                data['Attributes'].append(new_attrib)
        if location_name:
            building = self.get_location_by_name(location_name)
            data['LocationID'] = building['ID']
            if room_name:
                data['LocationRoomID'] = self.get_room_by_name(building, room_name)['ID']
        if asset_lifespan:
            expected_replacement_date = acquisition_date + datetime.timedelta(days=(int(asset_lifespan*365.25)))
            data['ExpectedReplacementDate'] = expected_replacement_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        if requester:
            data['RequestingCustomerID'] = self.get_person_by_name_email(requester)['UID']
        if requesting_dept:
            data['RequestingDepartmentID'] = self.get_account_by_name(requesting_dept)['ID']
        if owner:
            data['OwningCustomerID'] = self.get_person_by_name_email(owner)['UID']
        if owning_dept:
            data['OwningDepartmentID'] = self.get_account_by_name(owning_dept)['ID']
        if product_model:
            data['ProductModelID'] = self.get_product_model_by_name_id(product_model)['ID']
        if form:
            data['FormID'] = self.get_asset_form_by_name_id(form)['ID']
        if location_name:
            temp_location = self.get_location_by_name(location_name)
            data['LocationID'] = temp_location['ID']
            if room_name:
                data['LocationRoomID'] = self.get_room_by_name(temp_location, room_name)['ID']
        if asset_tag:
            data['Tag'] = asset_tag
        if parent:
            if type(parent) is int:
                data['ParentID'] = parent
            else:
                parent_asset = self.find_asset_by_sn(parent)
                if not parent_asset:
                    parent_asset = self.search_assets(parent, max_results=1)
                if parent_asset:
                    data['ParentID'] = parent_asset['ID']
        return data

    def create_asset(self, asset, check_duplicate=True):
        """
        Creates an asset

        :param asset: a dict of asset info (maybe from make_asset_json()) to use in creation
        :param check_duplicate: boolean of whether or not we should check to see if this is a duplicate asset

        :return: dict of created asset details

        """
        if check_duplicate:
            duplicate = None
            serial = asset['SerialNumber']
            try:
                duplicate = self.find_asset_by_sn(serial)
            except TdxApiObjectNotFoundError:
                pass  # Duplicate not found
            if duplicate:
                raise TdxApiDuplicateError(f"Asset with Serial Number {serial} already exists")
        created_asset = self.make_call('', 'post', asset)
        return created_asset

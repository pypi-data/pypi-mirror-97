# coding: utf-8
"""
    assetic.layertools  (layertools.py)
    Tools to assist with using arcgis integration with assetic
"""
import json
from typing import List

import assetic
from PyQt5.QtCore import QDate, QDateTime
from assetic.tools.shared.config_base import ConfigBase
from assetic.tools.shared.layer_tools_base import LayerToolsBase
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsFeature,
    QgsVectorLayer,
    QgsFeatureIterator,
    QgsFeatureRequest,
    QgsWkbTypes
)


class QGISLayerTools(LayerToolsBase):
    """
    Class to manage processes that relate to a GIS layer
    """

    def __init__(self, config: ConfigBase = None):
        super().__init__(config)

    def get_rows(self, lyr: QgsVectorLayer, fields: List[str], query: str = None
                 ) -> None:
        """
        This method is unnecessary in QGIS as features can be accessed
        as dict-like objects when iterating over lyr.getFeatures().

        This method is being left in the qgis_layertools file as
        it is a required abstract method.

        :param lyr:
        :param fields:
        :param query:
        :return:
        """
        pass

    def get_geom_wkt(self, *args, **kwargs):
        """
        As yet unused method.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def create_funclocs_from_layer(self, lyr: QgsVectorLayer, query: str = None
                                   ) -> (int, int):
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and creates functional locations defined in
        the data.

        Returns the number of successful and failed functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        if not self._is_valid_config:
            self.logger.error("Invalid or missing configuration file, "
                              "functional location creation aborted.")
            return

        lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(lyr, lyr.name(), "create")

        if (lyr_config is None) and (fields is None):
            self.messager.new_message(
                "Unable to process functional location layer '{0}' due to "
                "missing configuration".format(lyr.name()))
            # return indication that nothing was processed
            return 0, 0

        has_lyr_fl_type = 'functional_location_type' in fields

        fl_corefields = lyr_config['fl_corefields']
        fl_coredefaults = lyr_config['fl_coredefaults']

        attrs = lyr_config['fl_attributefields']
        def_attrs = lyr_config['fl_attributedefaults']

        success = 0
        fail = 0

        if query:
            req = QgsFeatureRequest().setFilterExpression(query)
        else:
            req = QgsFeatureRequest()

        for feat in lyr.getFeatures(req):
            if has_lyr_fl_type:
                # many fltypes in a single layer
                fltype = feat[fl_corefields['functional_location_type']]
            else:
                # single fltype per layer
                fltype = fl_coredefaults['functional_location_type']

            flid = feat[fl_corefields['functional_location_id']]

            if flid in ['', None]:
                # no FL ID defined. attempt to retrieve by name and type
                flrepr = self.fltools.get_functional_location_by_name_and_type(
                    feat[fl_corefields['functional_location_name']]
                    , fltype)
            else:
                # FL ID defined. attempt to retrieve by ID
                # if FL doesn't exist we assume that autoid generation
                # is off which is why the ID is already set in the layer
                flrepr = self.fltools.get_functional_location_by_id(flid)

            if flrepr is not None:
                # FL already exists!
                self.messager.new_message(
                    "Functional Location {0} already exists".format(
                        flrepr.functional_location_name
                    ))
                fail += 1
                continue

            # Doesn't appear to be an existing FL so create.
            flrepr = self._create_fl_from_row(
                feat, fl_corefields, fltype, attrs, def_attrs)

            if flrepr is None:
                # Error creating FL
                fail += 1
                continue

            # update row with new information - ID, GUID, etc.
            updfields = [fl_corefields[f] for f in [
                'functional_location_id', 'id'] if f in fl_corefields]
            rev = {v: k for k, v in fl_corefields.items()}
            for f in updfields:
                feat[fields.index(f)] = (flrepr.__getattribute__(rev[f]))

            lyr.updateFeature(feat)
            success += 1

        message = "Finished {0} Functional Location Creation, {1} Functional" \
                  " Locations created".format(lyr.name, str(success))

        if fail > 0:
            message = "{0}, {1} Functional Locations not created. (Check " \
                      "logfile {2})".format(
                message, str(fail), self.logfilename)

        self.messager.new_message(message)

        return success, fail

    def update_funclocs_from_layer(self, lyr: QgsVectorLayer, query: str = None
                                   ) -> (int, int):
        """
        Iterates over the rows in a passed in layer (narrowed down by
        optional query) and updates functional locations defined in
        the data.

        Returns the number of successful and failed updates of functional
        locations.

        :param lyr: passed in arcgis layerfile
        :param query: query to select certain attributes
        :return: number created, number failed
        """
        if not self._is_valid_config:
            self.logger.error("Invalid or missing configuration file, "
                              "Functional Location update aborted.")
            return

        lyr_config, fields, idfield = self.xmlconf.get_fl_layer_config(lyr, lyr.name(), "update")

        if lyr_config is None and fields is None:
            msg = "Unable to process functional location layer '{0}' due to " \
                  "missing configuration".format(lyr.name)
            self.messager.new_message(msg)
            self.logger.error(msg)
            # return indication that nothing was processed
            return 0, 0

        fl_corefields = lyr_config['fl_corefields']
        fl_coredefaults = lyr_config['fl_coredefaults']

        has_lyr_fl_type = False
        if 'functional_location_type' in fl_corefields:
            has_lyr_fl_type = True
        elif 'functional_location_type' not in fl_coredefaults:
            # need to have functional location type
            msg = "Unable to process functional location layer '{0}' due to " \
                  "missing functional location type".format(lyr.name)
            self.messager.new_message(msg)
            self.logger.error(msg)
            # return indication that nothing was processed
            return 0, 0

        attrs = lyr_config['fl_attributefields']
        def_attrs = lyr_config['fl_attributedefaults']
        all_attr_fields = attrs.keys() + def_attrs.keys()

        if query:
            req = QgsFeatureRequest().setFilterExpression(query)
        else:
            req = QgsFeatureRequest()

        success = 0
        fail = 0
        for feat in lyr.getFeatures(req):

            if has_lyr_fl_type:
                # many fltypes in a single layer
                fltype = feat[fl_corefields['functional_location_type']]
            else:
                # single fltype per layer defined in defaults
                fltype = fl_coredefaults['functional_location_type']

            flid = feat[fl_corefields['functional_location_id']]

            fl_guid = None
            if "id" in fl_corefields and fl_corefields['id'] in feat:
                fl_guid = feat[fl_corefields['id']]

            if flid in ['', None] and fl_guid in ['', None]:
                # no FL ID defined. attempt to retrieve by name and type
                flrepr = self.fltools.get_functional_location_by_name_and_type(
                    feat[fl_corefields['functional_location_name']]
                    , fltype, all_attr_fields)
            else:
                # FL ID defined. attempt to retrieve by ID
                if fl_guid:
                    flrepr = self.fltools.get_functional_location_by_id(
                        fl_guid, all_attr_fields)
                else:
                    flrepr = self.fltools.get_functional_location_by_id(
                        flid, all_attr_fields)
            if flrepr is None:
                # No FL found so move to next record
                self.messager.new_message(
                    "Unable to retrieve Functional Location {0} for "
                    "update".format(
                        feat[fl_corefields['functional_location_name']]
                    ))
                fail += 1
                continue

            # FL exists, check if the attributes are different
            # and then post if they are
            row_attrs = self._retrieve_fl_attrs_from_row(feat, attrs,
                                                         def_attrs)

            if row_attrs != flrepr.attributes or \
                    flrepr.functional_location_name != feat[
                fl_corefields['functional_location_name']]:
                # e.g. something has changed so update attributes with GIS
                # attributes, and name in case it changed (not allow
                # change to FL type or id)
                flrepr.attributes = row_attrs
                flrepr.functional_location_name = feat[
                    fl_corefields['functional_location_name']]
                flepr = self.fltools.update_functional_location(flrepr)
                if flepr:
                    success += 1
                else:
                    fail += 1
            else:
                # indicate success, just don't attempt update
                success += 1

        message = "Finished {0} Functional Location Update, {1} Functional " \
                  "Locations updated".format(lyr.name, str(success))

        if fail > 0:
            message = "{0}, {1} Functional Locations not updated. (Check " \
                      "logfile {2})".format(
                message, str(fail), self.logfilename)

        self.messager.new_message(message)

        return success, fail

    def individually_update_rows(self, rows: QgsFeatureIterator, total: int,
                                 lyr_config: dict, fields: List[str], lyr_crs) -> dict:
        """
        Iterates over the rows of the layerfile and updates each asset
        using API calls.

        :param rows: <List[dict]> a list of dicts where keys are the
        column names and values are cell contents
        :param total: <int> the number of features
        :param lyr_config: <dict> dict defining the relationship
        between xml nodes and the layer's column values
        :param fields: <List[str]> a list of column names from the layer
        :return:
        """

        lyrname = lyr_config['layer']

        # initialise counters for the log messages
        num_pass = 0
        num_fail = 0

        for i, row in enumerate(rows):
            success = self._update_asset(row, lyr_config, fields, lyr_crs)
            msg = ("Processing feature {1} of {2}".format(lyrname, i + 1, total))
            self.messager.new_message(msg)

            if success:
                num_pass = num_pass + 1
            else:
                num_fail = num_fail + 1

            message = "Finished {0} Asset Update, {1} assets updated".format(
                lyrname, str(num_pass))

            if num_fail > 0:
                message = "{0}, {1} assets not updated. (Check log file '{2}')" \
                          "".format(message, str(num_fail), self.logfilename)

            self.messager.new_message(message)

        return {"pass_cnt": num_pass, "fail_cnt": num_fail}

    def create_assets(self, lyr: QgsVectorLayer, query: str = None) -> dict:
        """
        For the given layer create new assets for the selected features only if
        features have no assetic guid.
        :param lyr: <QgsVectorLayer>is the layer to process (not layer name)
        :param query: <str>
        """
        results = {
            "pass_cnt": 0,
            "fail_cnt": 0,
            "ignore_cnt": 0,
            "partial_cnt": 0,
        }

        # get configuration for layer
        lyr_config, fields, idfield = self.xmlconf.get_layer_config(lyr, lyr.name(), "create")
        if lyr_config is None:
            self.messager.new_message("Layer configuration object not defined. "
                                      "Returning empty results")
            return results

        cnt = 1.0
        for feat in lyr.getSelectedFeatures():
            if self.messager.is_cancelled:  # noqa
                # user initiated cancel
                self.messager.new_message("Execution cancelled")
                return results
            self.messager.new_message(
                "Creating Assets for layer {0}.\nProcessing "
                "feature {1} of {2}".format(
                    lyr.name(), int(cnt), lyr.selectedFeatureCount()))

            # create new asset
            result = self._new_asset(feat, lyr_config, fields, lyr.crs(), lyr)
            if result == 0:
                results["pass_cnt"] += 1
            elif result == 1:
                results["fail_cnt"] += 1
            elif result == 2:
                results["ignore_cnt"] += 1
            elif result == 3:
                results["partial_cnt"] += 1
            cnt += 1

        self.messager.new_message("Processing complete")

        return results

    def update_assets(self, lyr: QgsVectorLayer, query: str = None):
        """
        For the given layer update assets for the selected features only
        where features have an assetic guid/asset id.
        :param lyr: is the layer to process (not layer name but ArcMap layer)
        :param query: optional attribute query to get selection
        """
        # get layer configuration from xml file
        lyr_config, fields, idfield = self.xmlconf.get_layer_config(lyr, lyr.name(), "update")

        if lyr_config is None:
            return

        if lyr.selectedFeatureCount() == 0:
            self.asseticsdk.logger.debug("No features selected - must pass in valid"
                                         " 'where clause'.")
            return

        feats = lyr.getSelectedFeatures()

        if lyr.selectedFeatureCount() > self._bulk_threshold:
            chk, valid_rows = self.bulk_update_rows(feats, lyr, lyr_config)
            results = None
        else:
            results = self.individually_update_rows(feats, lyr.selectedFeatureCount(), lyr_config, fields, lyr.crs())

        return results

    def _new_asset(self, row: QgsFeature, lyr_config: dict, fields, layer_crs, layer):
        """
        Create a new asset for the given search result row
        :param row: a layer search result row, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields
        :returns: 0 if success, 1 if error, 2 if skip (existing),
        3 if partial success such as asset created but component not
        """
        results = {
            "success": 0
            , "error": 1
            , "skip": 2
            , "partial": 3
        }
        complete_asset_obj = self.get_asset_obj_for_row(
            row, lyr_config, fields)
        # alias core fields for readability
        corefields = lyr_config["corefields"]

        # verify it actually needs to be created
        if "id" in corefields and corefields["id"] in fields:
            if not complete_asset_obj.asset_representation.id:
                # guid field exists in ArcMap and is empty
                newasset = True
            else:
                # guid id populated, must be existing asset
                newasset = False
        else:
            # guid not used, what about asset id?
            if "asset_id" in corefields and corefields["asset_id"] in fields:
                # asset id field exists in Arcmap
                if not complete_asset_obj.asset_representation.asset_id:
                    # asset id is null, must be new asset
                    newasset = True
                else:
                    # test assetic for the asset id.
                    # Perhaps user is not using guid
                    # and is manually assigning asset id.
                    chk = self.assettools.get_asset(
                        complete_asset_obj.asset_representation.asset_id)
                    if not chk:
                        newasset = True
                    else:
                        # asset id already exists.  Not a new asset
                        newasset = False
            else:
                # there is no field in ArcMap representing either GUID or
                # Asset ID, so can't proceed.
                self.messager.new_message(
                    "Asset not created because there is no configuration "
                    "setting for <id> or <asset_id> or the field is not in "
                    "the layer")
                return results["error"]
        if not newasset:
            self.messager.new_message(
                "Asset not created because it already has the following "
                "values: Asset ID={0},Asset GUID={1}".format(
                    complete_asset_obj.asset_representation.asset_id
                    , complete_asset_obj.asset_representation.id))
            return results["skip"]

        # set status
        complete_asset_obj.asset_representation.status = \
            lyr_config["creation_status"]
        # Create new asset
        response = self.assettools.create_complete_asset(complete_asset_obj)
        if response is None:
            msg = "Asset Not Created - Check log"
            self.messager.new_message(msg)
            return results["error"]
        # apply asset guid and/or assetid
        layer.startEditing()
        if "id" in corefields:
            if row.fieldNameIndex(corefields["id"]) >= 0:
                layer.changeAttributeValue(
                    row.id(), row.fieldNameIndex(corefields["id"])
                    , response.asset_representation.id)
        if "asset_id" in corefields:
            if row.fieldNameIndex(corefields["asset_id"]) >= 0:
                layer.changeAttributeValue(
                    row.id(), row.fieldNameIndex(corefields["asset_id"])
                    , response.asset_representation.asset_id)
        # apply component id
        for component_dim_obj in response.components:
            for component_config in lyr_config["components"]:
                component_type = None
                if "component_type" in component_config["attributes"]:
                    component_type = component_config["attributes"][
                        "component_type"]
                elif "component_type" in component_config["defaults"]:
                    component_type = component_config["defaults"][
                        "component_type"]

                if "id" in component_config["attributes"] and component_type \
                        == component_dim_obj.component_representation \
                        .component_type:
                    if row.fieldNameIndex(
                            component_config["attributes"]["id"]) >= 0:
                        layer.changeAttributeValue(
                            row.id(),
                            row.fieldNameIndex(
                                component_config["attributes"]["id"])
                            , component_dim_obj.component_representation.id)
        layer.commitChanges()

        # Now check config and update Assetic with spatial data and/or address
        addr = None
        geojson = None
        if len(lyr_config["addressfields"]) > 0 \
                or len(lyr_config["addressdefaults"]) > 0:
            # get address details
            addr = assetic.CustomAddress()
            # get address fields from the attribute fields of the feature
            for k, v in lyr_config["addressfields"].items():
                if k in addr.to_dict() and v in fields:
                    val = None
                    try:
                        val = self.sanitise_attribute(row[v])
                    except Exception:
                        pass
                    setattr(addr, k, val)
            # get address defaults
            for k, v in lyr_config["addressdefaults"].items():
                if k in addr.to_dict():
                    setattr(addr, k, v)
        if lyr_config["upload_feature"]:
            geojson = self.get_geom_geojson(layer_crs, row.geometry())
        if addr or geojson:
            chk = self.assettools.set_asset_address_spatial(
                response.asset_representation.id, geojson, addr)
            if chk > 0:
                return results["partial"]

        return results["success"]

    def _update_asset(self, row: QgsFeature, lyr_config, fields, layer_crs):
        """
        Update an existing asset for the given arcmap row
        :param row: a layer search result row, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields
        :param layer.crs()
        :returns: Boolean True if success, else False
        """

        complete_asset_obj = self.get_asset_obj_for_row(
            row, lyr_config, fields)

        # make sure we have an asset id to use
        if not complete_asset_obj.asset_representation.id:
            # guid not used, what about asset id?
            if complete_asset_obj.asset_representation.asset_id:
                # asset id is not null
                # test Assetic for the asset id.
                chk = self.assettools.get_asset(
                    complete_asset_obj.asset_representation.asset_id)
                if chk:
                    # asset_exists = True
                    # set the guid, need it later if doing spatial load
                    complete_asset_obj.asset_representation.id = chk["Id"]

        if not complete_asset_obj.asset_representation.id:
            self.asseticsdk.logger.debug(
                "Asset not updated because it is undefined or not in Assetic. "
                "Asset ID={0}".format(
                    complete_asset_obj.asset_representation.asset_id))
            return False

        if len(complete_asset_obj.components) > 0:
            # have components, assume network measure needed, also assume we
            # don't have Id's for the components which are needed for update
            current_complete_asset = self.assettools.get_complete_asset(
                complete_asset_obj.asset_representation.id, []
                , ["components", "dimensions"])

            for component in complete_asset_obj.components:
                # get the id from the current record, matching on
                # component type
                new_comp = component.component_representation
                for current_comp_rep in current_complete_asset.components:
                    current_comp = current_comp_rep.component_representation
                    if current_comp.component_type == new_comp.component_type \
                            or current_comp.id == new_comp.id:
                        # set the id and name in case they are undefined
                        new_comp.id = current_comp.id
                        new_comp.name = current_comp.name

                        # Look for dimensions and set dimension Id
                        for dimension in component.dimensions:
                            count_matches = 0
                            for current_dim in current_comp_rep.dimensions:
                                # match on id or (nm type and record
                                # type and shape name)
                                if not dimension.id and \
                                        dimension.network_measure_type == \
                                        current_dim.network_measure_type and \
                                        dimension.record_type == \
                                        current_dim.record_type and \
                                        dimension.shape_name == \
                                        current_dim.shape_name:
                                    # set dimension id and component id
                                    dimension.id = current_dim.id
                                    dimension.component_id = new_comp.id
                                    count_matches += 1
                            if not dimension.id or count_matches > 1:
                                # couldn't find unique id. remove
                                component.dimensions.remove(dimension)
                                self.asseticsdk.logger.warning(
                                    "Unable to update dimension for "
                                    "component {0} because new existing and "
                                    "distinct dimension record was "
                                    "found".format(
                                        new_comp.name))
                if not new_comp.id:
                    # couldn't find component - remove
                    complete_asset_obj.components.remove(component)
                    self.asseticsdk.logger.warning(
                        "Unable to update component for asset {0}".format(
                            complete_asset_obj.asset_representation.asset_id
                        ))

        # now execute the update
        chk = self.assettools.update_complete_asset(complete_asset_obj)
        if chk > 0:
            self.messager.new_message(
                "Error Updating Asset:{0}, Asset GUID={1}".format(
                    complete_asset_obj.asset_representation.asset_id
                    , complete_asset_obj.asset_representation.id))
            return False

        # Now check config and update Assetic with spatial data
        if lyr_config["upload_feature"]:
            # get address details
            addr = assetic.CustomAddress()
            # get address fields the attribute fields of the feature
            for k, v in lyr_config["addressfields"].items():
                if k in addr.to_dict() and v in fields:
                    setattr(addr, k, row[fields.index(v)])
            # get address defaults
            for k, v in lyr_config["addressdefaults"].items():
                if k in addr.to_dict():
                    setattr(addr, k, v)

            geojson = self.get_geom_geojson(layer_crs, row.geometry())

            chk = self.assettools.set_asset_address_spatial(
                complete_asset_obj.asset_representation.id, geojson, addr)
            if chk > 0:
                self.messager.new_message(
                    "Error Updating Asset Address/Location:{0}, Asset GUID={1}"
                    "".format(
                        complete_asset_obj.asset_representation.asset_id
                        , complete_asset_obj.asset_representation.id))
                return False
        return True

    def get_asset_obj_for_row(self, feat: QgsFeature, lyr_config: dict, fields: List[str]
                              ) -> assetic.AssetToolsCompleteAssetRepresentation:
        """
        Prepare a complete asset for the given feature
        :param feat: a layer search result row, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields in the layer
        :returns: assetic.AssetToolsCompleteAssetRepresentation() or None
        """
        # instantiate the complete asset representation to return
        complete_asset_obj = assetic.AssetToolsCompleteAssetRepresentation()

        # create an instance of the complex asset object
        asset = assetic.models.ComplexAssetRepresentation()

        asset.asset_category = lyr_config["asset_category"]

        # build a dict of fields and their value and append dimensions
        atts = dict()
        for fld in fields:
            val = None
            try:
                if feat[fld] and str(feat[fld]).strip() != "":
                    val = self.sanitise_attribute(feat[fld])
            except Exception:
                pass
            atts[fld] = val

        atts["_geometry_length_"] = feat.geometry().length()
        atts["_geometry_area_"] = feat.geometry().area()

        # set core field values from qgis fields
        for k, v in lyr_config["corefields"].items():
            if k in asset.to_dict() and v in atts:
                setattr(asset, k, atts[v])

        # set core field values from defaults
        for k, v in lyr_config["coredefaults"].items():
            if k in asset.to_dict() and str(v).strip() != "":
                setattr(asset, k, v)

        attributes = {}
        # set attributes values from arcmap fields
        if "attributefields" in lyr_config:
            for k, v in lyr_config["attributefields"].items():
                if v in atts:
                    attributes[k] = atts[v]

        # set attribute values from defaults
        for k, v in lyr_config["attributedefaults"].items():
            if str(v).strip() != "":
                attributes[k] = v
        # add the attributes to the asset and the asset to the complete object
        asset.attributes = attributes
        complete_asset_obj.asset_representation = asset

        # create component representations
        for component in lyr_config["components"]:
            comp_tool_rep = assetic.AssetToolsComponentRepresentation()
            comp_tool_rep.component_representation = \
                assetic.ComponentRepresentation()
            for k, v in component["attributes"].items():
                if v in atts:
                    setattr(comp_tool_rep.component_representation, k
                            , atts[v])
            for k, v in component["defaults"].items():
                if k in comp_tool_rep.component_representation.to_dict():
                    setattr(comp_tool_rep.component_representation, k, v)

            # add dimensions to component
            if component["dimensions"] and len(component["dimensions"]) > 0:
                # create an array for the dimensions to be added
                # to the component
                dimlist = list()
                for dimension in component["dimensions"]:
                    # Create an instance of the dimension and
                    # set minimum fields
                    dim = assetic.ComponentDimensionRepresentation()
                    for k, v in dimension["attributes"].items():
                        if v in atts:
                            setattr(dim, k, atts[v])
                    for k, v in dimension["defaults"].items():
                        if k in dim.to_dict():
                            setattr(dim, k, v)
                    dimlist.append(dim)

                # Add the dimension array to the component
                comp_tool_rep.dimensions = dimlist

            # add the component array
            complete_asset_obj.components.append(comp_tool_rep)
        return complete_asset_obj

    @staticmethod
    def sanitise_attribute(attribute):
        """
        Some of the attribute field types from a qgis table are not standard
        python types, so convert to standard types
        :param attribute: The attribute from the QGIS table
        :return: a standard python type - e.g datetime, date, string
        """
        if isinstance(attribute, QDate):
            return attribute.toPyDate()
        elif isinstance(attribute, QDateTime):
            return attribute.toPyDateTime()
        else:
            return attribute

    def get_geom_geojson(self, layer_crs, geometry):
        """
        Get the geojson for a geometry in 4326 projection
        :param layer_crs: layer crs object
        :param geometry: The input geometry
        :returns: wkt string of geometry in the specified projection
        """

        crs_dest = QgsCoordinateReferenceSystem("EPSG:4326")
        crs_transform = QgsCoordinateTransform(layer_crs, crs_dest, QgsProject.instance())

        # Get midpoint/centroid to use later
        midpoint = geometry.centroid()

        # transform the geometry and convert to geojson
        if geometry.transform(crs_transform) == 0:
            geojsonstr = geometry.asJson()
            geojson = json.loads(geojsonstr)
        else:
            # unable to transform
            self.messager.new_message("Unable to apply transformation to "
                                      "geometry")
            return None

        # transform midpoint and get json
        centroid_geojson = None
        if midpoint.transform(crs_transform) == 0:
            centroid_geojsonstr = midpoint.asJson()
            centroid_geojson = json.loads(centroid_geojsonstr)

        if "GeometryCollection" not in geojson:

            # todo is this the most explicit flow throw different geometry types?
            if geometry.wkbType() in [QgsWkbTypes.Point,
                                      QgsWkbTypes.MultiPoint]:
                fullgeojson = {
                    "geometries": [geojson]
                    , "type": "GeometryCollection"}

            # Geojson is expected to include collection, but QGIS
            # does not include it
            elif centroid_geojson:
                fullgeojson = {
                    "geometries": [geojson, centroid_geojson]
                    , "type": "GeometryCollection"}
            else:
                fullgeojson = {
                    "geometries": [geojson]
                    , "type": "GeometryCollection"}
        else:
            # not try to include centroid, too messy.  Am not expecting to hit
            # this case unless QGIS changes
            fullgeojson = geojson

        return fullgeojson

    def get_layer_asset_guid(self, assetid: str, lyr_config: dict):
        """
        Get the asset guid for an asset.  Used where "id" is not in the
        configuration.  If it is then it is assumed the assetid is a guid
        :param assetid: The assetid - may be guid or friendly
        :param lyr_config: the layer
        :returns: guid or none
        """
        # alias core fields object for readability
        corefields = lyr_config["corefields"]
        if "id" not in corefields:
            # must be using asset_id (friendly).  Need to get guid
            asset = self.assettools.get_asset(assetid)
            if asset is not None:
                assetid = asset["Id"]
            else:
                msg = "Asset with ID [{0}] not found in Assetic".format(
                    assetid)
                self.messager.new_message(msg)
                return None
        return assetid

    def set_asset_address_spatial(self, assetid, lyr_config, geojson,
                                  addr=None):
        """
        Set the address and/or spatial definition for an asset
        :param assetid: The asset GUID (TODO support friendly ID)
        :param lyr_config: The settings defined for the layer
        :param geojson: The geoJson representation of the feature
        :param addr: Address representation.  Optional.
        assetic.CustomAddress
        :returns: 0=no error, >0 = error
        """
        if addr is not None and \
                not isinstance(addr, assetic.CustomAddress):
            msg = "Format of address incorrect,expecting " \
                  "assetic.CustomAddress"
            self.asseticsdk.logger.debug(msg)
            return 1
        else:
            addr = assetic.CustomAddress()

        # get guid
        assetguid = self.get_layer_asset_guid(assetid, lyr_config)
        if assetguid is None:
            msg = "Unable to obtain asset GUID for assetid={0}".format(assetid)
            self.messager.new_message(msg)
            return 1
        chk = self.assettools.set_asset_address_spatial(assetguid, geojson,
                                                        addr)
        return 0

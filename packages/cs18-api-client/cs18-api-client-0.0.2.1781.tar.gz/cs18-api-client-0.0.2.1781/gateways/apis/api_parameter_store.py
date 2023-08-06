from gateways.apis.api_base_class import ApiBase


class ParameterStore(ApiBase):
    def add_parameter(self):
        return self.build_route("settings/parameters/")

    def get_all_parameters(self):
        return self.build_route("settings/parameters/")

    def get_parameter(self, parameter_name: str):
        return self.build_route(
            "settings/parameters/{parameter_name}".format(**locals()))

    def delete_parameter(self, parameter_name: str):
        return self.build_route(
            "settings/parameters/{parameter_name}".format(**locals()))

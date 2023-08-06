from confyml import confyml

config = confyml.get_config()


class SampleClass:

    @config.apply
    def __init__(self, kwarg1=None):
        self._kwarg1 = kwarg1

    @config.apply
    def sample_method(self, kwarg1=1):
        return kwarg1, self._kwarg1


@config.apply
def sample_function(kwarg1=None):
    return kwarg1


@config.apply
def sample_function_2(kwarg1=None):
    return kwarg1


@config.apply
def sample_function_3(kwarg1=None):
    return kwarg1
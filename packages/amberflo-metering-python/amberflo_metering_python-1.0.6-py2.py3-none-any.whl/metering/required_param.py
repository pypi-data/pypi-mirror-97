class RequiredParam(object):
    @staticmethod
    def require_string_dictionary(name, field, allow_none=True):
        RequiredParam.require(name, field, dict, allow_none)

        # If we reached here and the field is none we can return.
        if field is None:
            return

        key_name = name + ".key"
        value_name = name + ".value"
        for key, value in field.items():
            RequiredParam.require_string_value(key_name, key)
            RequiredParam.require_string_value(value_name, value)

    @staticmethod
    def require_string_value(name, field):
        RequiredParam.require(name, field, str, allow_none = False)

        if RequiredParam.__is_blank(field):
            raise AssertionError('String must have a none whitespace value')


    @staticmethod
    def require(name, field, data_type, allow_none=True):
        if field is None:
            if allow_none:
                return None
            
            msg = '{0} must have a value'.format(name)
            raise AssertionError(msg)

        """Require that the named `field` has the right `data_type`"""
        if not isinstance(field, data_type):
            msg = '{0} must have {1}, got: {2}'.format(name, data_type, field)
            raise AssertionError(msg)


    @staticmethod
    def __is_blank(string_value):
        return not (string_value and string_value.strip())
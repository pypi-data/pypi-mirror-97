# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool


class WebSite(metaclass=PoolMeta):
    __name__ = "nereid.website"

    def add_custom_url_rules(self, app, url_rules):
        # Add the static-file-transform URL also as custom URL to provide it
        # as unprefixed route, too.
        url_rules = super(WebSite, self).add_custom_url_rules(app, url_rules)
        pool = Pool()
        ns = pool.get('nereid.static.file')
        url_rules.append(app.url_rule_class(
                '/static-file-transform/<int:active_id>/<path:commands>.<extension>',
                endpoint='nereid.static.file.transform_static_file'))
        return url_rules

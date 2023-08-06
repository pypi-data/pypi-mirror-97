import logging
import pkg_resources


logger = logging.getLogger(__name__)


def static_path(package):
    logger.debug('resolving path: %s' % package)

    # TODO: support zip format (ie. extract resources in egg cache)
    # see http://peak.telecommunity.com/DevCenter/PkgResources
    return pkg_resources.resource_filename(package, 'static')

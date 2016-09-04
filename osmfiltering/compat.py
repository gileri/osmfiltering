import logging

try:
    from lxml import etree
    logging.debug("Using lxml")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        logging.debug("Using cElementTree")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                logging.debug("Using cElementTree")
            except ImportError:
                # normal ElementTree install
                import elementtree.ElementTree as etree

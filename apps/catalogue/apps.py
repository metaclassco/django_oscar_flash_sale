import oscar.apps.catalogue.apps as apps


class CatalogueConfig(apps.CatalogueConfig):
    label = 'catalogue'
    name = 'apps.catalogue'
    verbose_name = 'Catalogue'

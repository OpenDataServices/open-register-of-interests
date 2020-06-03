from django_elasticsearch_dsl_drf.filter_backends import FacetedSearchFilterBackend


class SizedFacetedSearchFilterBackend(FacetedSearchFilterBackend):
    def prepare_faceted_search_fields(self, view):
        """ Adds a "facet_size_all" query param to standard FacetedSearchFilterBackend

        Usage: ?facet_size_all=<facet_name>&facet_size_all=<facet_name>...

        """
        prepared_facet = super().prepare_faceted_search_fields(view)

        facets_to_show_all = view.request.GET.getlist("facet_size_all")

        for facet_to_show_all in facets_to_show_all:
            try:
                # 99,999 determined as "sensible" maximum size before these
                # facets get too large
                prepared_facet[facet_to_show_all]["options"]["size"] = 99999
            except KeyError:
                continue

        return prepared_facet

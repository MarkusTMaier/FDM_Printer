from octorest import OctoRest
import requests

class MyOctoRest(OctoRest):
    def selections(self):
        """Retrieve information regarding the selected spools
        http://mk3sdigitaltwin.ethz.ch/plugin/filamentmanager/selections
        """
        return self._get('/plugin/filamentmanager/selections')

    def spools(self):
        """Retrieve information about all available spools
        http://mk3sdigitaltwin.ethz.ch/plugin/filamentmanager/spools
        """
        return self._get('/plugin/filamentmanager/spools')

    def profiles(self):
        """Retrieve information about stored filament profiles
        http://mk3sdigitaltwin.ethz.ch/plugin/filamentmanager/profiles
        """
        return self._get('/plugin/filamentmanager/profiles')

    #def update_selection(self, identifier):
        #return self._patch(f'/plugin/filamentmanager/spools/{identifier}')
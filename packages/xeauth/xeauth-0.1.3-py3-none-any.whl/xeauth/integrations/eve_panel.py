
import param
import panel as pn

from ..oauth import NotebookSession
try:
    from eve_panel.auth import EveAuthBase
except ImportError:
    pass

class XenonEveAuth(NotebookSession, EveAuthBase):
    # session = param.ClassSelector(NotebookSession, default=NotebookSession())

    def get_headers(self):
        """Generate auth headers for HTTP requests.

        Returns:
            dict: Auth related headers to be included in all requests.
        """
        if self.logged_in:
            return {"Authorization": f"Bearer {self.access_token}"}
        else:
            return {}

    def login(self):
        """perform any actions required to aquire credentials.

        Returns:
            bool: whether login was successful
        """
        self.login_requested(None)


    def set_credentials(self, **credentials):
        """Set the access credentials manually.
        """
        for k,v in credentials.items():
            if k in ['access_token', "id_token", "refresh_token", "expires"]:
                setattr(self.token, k, v)
            else:
                setattr(self, k, v)
                
    def credentials_view(self):
        return self.gui

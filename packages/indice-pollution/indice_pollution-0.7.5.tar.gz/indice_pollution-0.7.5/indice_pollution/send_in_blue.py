import sib_api_v3_sdk
from flask import _app_ctx_stack

class SendInBlue(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration['apikey'] = app.config['SIB_APIKEY']
        app.teardown_context(self.teardown)

    def teardown(self):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'sendinblue'):
            ctx.sqlite3_db.close()

    @property
    def api(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'sendinblue'):
                apiclient = sib_api_v3_sdk.ApiClient(self.configuration)
                ctx.sendinblue = sib_api_v3_sdk.AccountApi(apiclient)
            return ctx.sendinblue


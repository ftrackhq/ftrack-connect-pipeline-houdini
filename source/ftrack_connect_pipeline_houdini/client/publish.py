# # :coding: utf-8
# # :copyright: Copyright (c) 2019 ftrack

from ftrack_connect_pipeline_qt.client.publish import QtPublisherClient
import ftrack_connect_pipeline.constants as constants
import ftrack_connect_pipeline_qt.constants as qt_constants
import ftrack_connect_pipeline_houdini.constants as houdini_constants

class HoudiniPublisherClient(QtPublisherClient):
    ui_types = [constants.UI_TYPE, qt_constants.UI_TYPE, houdini_constants.UI_TYPE]

    '''Dockable houdini load widget'''
    def __init__(self, event_manager, parent=None):
        super(HoudiniPublisherClient, self).__init__(
            event_manager=event_manager, parent=parent
        )
        self.setWindowTitle('Houdini Pipeline Publisher')

    def change_host(self, host_connection):
        ''' Triggered when host_changed is called from the host_selector.'''
        super(HoudiniPublisherClient, self).change_host(host_connection)

        if False:
            import threading

            def t():
                def f():
                    super(HoudiniPublisherClient, self).change_host(host_connection)
                hdefereval.executeInMainThreadWithResult(f)
            threading.Thread(target=t).start()

    def change_definition(self, schema, definition):
        super(HoudiniPublisherClient, self).change_definition(schema, definition)

        if False:
            import hdefereval
            import threading
            def t():
                def f():
                    super(HoudiniPublisherClient, self).change_definition(schema, definition)
                #hdefereval.executeDeferred(f)
                hdefereval.executeInMainThreadWithResult(f)

            threading.Thread(target=t).start()

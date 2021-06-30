# :coding: utf-8
# :copyright: Copyright (c) 2014-2021 ftrack

import functools
import sys
import os
import logging

import ftrack_api

NAME = 'ftrack-connect-pipeline-houdini'
logger = logging.getLogger('{}.hook'.format(NAME.replace('-','_')))

plugin_base_dir = os.path.normpath(
    os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ),
        '..'
    )
)

python_dependencies = os.path.join(
    plugin_base_dir, 'dependencies'
)
sys.path.append(python_dependencies)

def on_discover_pipeline_houdini(session, event):

    from ftrack_connect_pipeline_houdini import __version__ as integration_version

    data = {
        'integration': {
            'name': NAME,
            'version': integration_version
        }
    }

    return data


def on_launch_pipeline_houdini(session, event):
    pipeline_houdini_base_data = on_discover_pipeline_houdini(session, event)

    houdini_path = os.path.join(plugin_base_dir, 'resource', 'houdini_path')

    houdini_path_append = (
        os.path.pathsep.join([houdini_path, '&']) if
        os.environ.get('HOUDINI_PATH','').find('&') == -1 else 
        houdini_path
    )


    definitions_plugin_hook = os.getenv('FTRACK_DEFINITION_PLUGIN_PATH')
    plugin_hook = os.path.join(definitions_plugin_hook, 'houdini', 'python')

    pipeline_houdini_base_data['integration']['env'] = {
        'FTRACK_EVENT_PLUGIN_PATH.prepend': plugin_hook,
        'PYTHONPATH.prepend': python_dependencies,
        'HOUDINI_PATH.append': houdini_path_append
    }

    
    selection = event['data'].get('context', {}).get('selection', [])

    if selection:
        task = session.get('Context', selection[0]['entityId'])
        pipeline_houdini_base_data['integration']['env']['FTRACK_CONTEXTID.set'] =  task['id']
        pipeline_houdini_base_data['integration']['env']['FS.set'] = task['parent']['custom_attributes'].get('fstart', '1.0')
        pipeline_houdini_base_data['integration']['env']['FE.set'] = task['parent']['custom_attributes'].get('fend', '100.0')
        pipeline_houdini_base_data['integration']['env']['FPS.set'] = task['parent']['custom_attributes'].get('fps', '24.0')


    return pipeline_houdini_base_data


def register(session):
    '''Subscribe to application launch events on *registry*.'''
    if not isinstance(session, ftrack_api.session.Session):
        return    
    
    handle_discovery_event = functools.partial(
        on_discover_pipeline_houdini,
        session
    )
    
    session.event_hub.subscribe(
        'topic=ftrack.connect.application.discover'
        ' and data.application.identifier=houdini*',
        handle_discovery_event, priority=40
    )

    handle_launch_event = functools.partial(
        on_launch_pipeline_houdini,
        session
    )   

    session.event_hub.subscribe(
        'topic=ftrack.connect.application.launch'
        ' and data.application.identifier=houdini*',
        handle_launch_event, priority=40
    )